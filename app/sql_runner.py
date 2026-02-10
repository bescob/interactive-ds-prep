import sqlite3
import signal
import re


class TimeoutError(Exception):
    pass


def _timeout_handler(signum, frame):
    raise TimeoutError("Query execution timed out")


def _is_select_only(sql):
    """Reject anything that isn't a SELECT statement."""
    cleaned = re.sub(r'--.*$', '', sql, flags=re.MULTILINE)
    cleaned = re.sub(r'/\*.*?\*/', '', cleaned, flags=re.DOTALL)
    cleaned = cleaned.strip().rstrip(';').strip()

    dangerous = re.compile(
        r'\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|ATTACH|DETACH|PRAGMA|VACUUM|REINDEX)\b',
        re.IGNORECASE
    )
    if dangerous.search(cleaned):
        return False
    return True


def execute_and_compare(setup_sql, user_sql, reference_sql, expected_rows=None, expected_columns=None):
    """
    Run user SQL against an in-memory SQLite DB set up with setup_sql.
    Compare results against reference_sql output (or expected_rows).

    Returns dict with user results, expected results, and comparison info.
    """
    result = {
        'user_columns': [],
        'user_rows': [],
        'expected_columns': expected_columns or [],
        'expected_rows': expected_rows or [],
        'is_correct': False,
        'error': None,
        'row_count_match': False,
        'column_match': False,
    }

    user_sql = user_sql.strip()
    if not user_sql:
        result['error'] = 'No SQL provided'
        return result

    if not _is_select_only(user_sql):
        result['error'] = 'Only SELECT statements are allowed'
        return result

    conn = None
    try:
        conn = sqlite3.connect(':memory:')
        conn.execute("PRAGMA journal_mode=OFF")

        # run setup
        conn.executescript(setup_sql)

        # run reference query to get expected output if we have one
        if reference_sql:
            try:
                cursor = conn.execute(reference_sql)
                ref_columns = [desc[0] for desc in cursor.description]
                ref_rows = cursor.fetchall()
                result['expected_columns'] = ref_columns
                result['expected_rows'] = [list(row) for row in ref_rows]
            except Exception as e:
                result['error'] = f'Reference query error: {str(e)}'
                return result

        # set timeout for user query
        old_handler = None
        try:
            old_handler = signal.signal(signal.SIGALRM, _timeout_handler)
            signal.alarm(2)
        except (ValueError, AttributeError):
            pass

        try:
            cursor = conn.execute(user_sql)
            user_columns = [desc[0] for desc in cursor.description]
            user_rows = cursor.fetchmany(1001)

            if len(user_rows) > 1000:
                result['error'] = 'Query returned more than 1000 rows. Add a LIMIT clause.'
                user_rows = user_rows[:1000]

            result['user_columns'] = user_columns
            result['user_rows'] = [list(row) for row in user_rows]
        except TimeoutError:
            result['error'] = 'Query timed out (2 second limit)'
            return result
        except Exception as e:
            result['error'] = str(e)
            return result
        finally:
            try:
                signal.alarm(0)
                if old_handler is not None:
                    signal.signal(signal.SIGALRM, old_handler)
            except (ValueError, AttributeError):
                pass

        # compare results
        exp_cols = [c.lower() for c in result['expected_columns']]
        usr_cols = [c.lower() for c in result['user_columns']]
        result['column_match'] = exp_cols == usr_cols

        exp_rows_normalized = _normalize_rows(result['expected_rows'])
        usr_rows_normalized = _normalize_rows(result['user_rows'])

        result['row_count_match'] = len(exp_rows_normalized) == len(usr_rows_normalized)
        result['is_correct'] = result['column_match'] and _rows_match(exp_rows_normalized, usr_rows_normalized)

    except Exception as e:
        result['error'] = str(e)
    finally:
        if conn:
            conn.close()

    return result


def _normalize_rows(rows):
    """Normalize row values for comparison: round floats, stringify."""
    normalized = []
    for row in rows:
        norm_row = []
        for val in row:
            if isinstance(val, float):
                norm_row.append(round(val, 2))
            elif val is None:
                norm_row.append(None)
            else:
                norm_row.append(val)
        normalized.append(tuple(norm_row))
    return normalized


def _rows_match(expected, actual):
    """Compare rows, trying both ordered and unordered comparison."""
    if expected == actual:
        return True
    if sorted(expected) == sorted(actual):
        return True
    return False
