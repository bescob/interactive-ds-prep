"""
Extract typed Question objects from parsed Module sections.

Mapping rules:
- Quick Quiz with code answer -> code_practice
- Quick Quiz with prose answer -> free_text
- Self-Test numbered questions -> free_text
- Module 14 SQL round -> code_practice
- Module 14 definition round -> flashcard
- Behavioral homework/STAR prompts -> star_practice
- Comparison tables -> flashcard (one per row)
"""

import re
from app.models.module import Module, Section, ContentBlock
from app.models.question import Question


def extract_questions(module: Module) -> list:
    questions = []

    for section in module.sections:
        section_questions = extract_from_section(module.id, section)
        questions.extend(section_questions)

    return questions


def extract_from_section(module_id: str, section: Section) -> list:
    questions = []
    title_lower = section.title.lower()

    # Self-Test sections
    if 'self-test' in title_lower or 'self test' in title_lower:
        questions.extend(extract_self_test(module_id, section))
        return questions

    # Module 14 round-based sections
    if re.match(r'round\s+\d+', title_lower):
        questions.extend(extract_round_questions(module_id, section))
        return questions

    # Behavioral / STAR sections
    if 'behavioral' in title_lower or 'star' in title_lower.split(':')[-1] if ':' in title_lower else title_lower:
        questions.extend(extract_behavioral(module_id, section))

    # Regular sections: look for Quick Quiz / Answer pairs
    questions.extend(extract_quick_quizzes(module_id, section))

    return questions


def extract_quick_quizzes(module_id: str, section: Section) -> list:
    """Extract Quick Quiz + Answer pairs from section blocks."""
    questions = []
    blocks = section.blocks

    for i, block in enumerate(blocks):
        if block.type != 'text':
            continue

        text = block.content

        # Find Quick Quiz patterns
        quiz_matches = list(re.finditer(
            r'\*\*Quick quiz[^*]*\*\*[:\s]*(.+?)(?=\n\n|\n\*\*Answer)',
            text, re.DOTALL | re.IGNORECASE
        ))

        if not quiz_matches:
            # Try alternate pattern: the quiz and answer on separate lines
            lines = text.split('\n')
            quiz_start = None
            quiz_text = ''
            answer_text = ''

            for j, line in enumerate(lines):
                if re.match(r'\*\*Quick quiz', line, re.IGNORECASE):
                    # Extract question part after the bold marker
                    q_match = re.match(r'\*\*Quick quiz[^*]*\*\*[:\s]*(.*)', line, re.IGNORECASE)
                    if q_match:
                        quiz_text = q_match.group(1).strip()
                        quiz_start = j
                elif quiz_start is not None and re.match(r'\*\*Answer:?\*\*', line, re.IGNORECASE):
                    a_match = re.match(r'\*\*Answer:?\*\*[:\s]*(.*)', line, re.IGNORECASE)
                    if a_match:
                        answer_text = a_match.group(1).strip()
                        # Collect continuation lines
                        for k in range(j + 1, len(lines)):
                            if lines[k].strip() == '' or lines[k].startswith('**'):
                                break
                            answer_text += '\n' + lines[k]

                    # Check if the answer includes code (look at next block)
                    has_code = False
                    code_content = ''
                    code_lang = None
                    if i + 1 < len(blocks) and blocks[i + 1].type == 'code':
                        # The answer is actually a code block
                        has_code = True
                        code_content = blocks[i + 1].content
                        code_lang = blocks[i + 1].language

                    # Also check if answer block following this text block is code
                    answer_has_code = bool(re.search(r'```', answer_text))

                    if has_code or _answer_is_code(answer_text, section.category):
                        q_type = 'code_practice'
                        lang = code_lang or ('sql' if section.category == 'sql' else 'python')
                        full_answer = (answer_text + '\n' + code_content).strip() if code_content else answer_text
                        questions.append(Question.create(
                            module_id=module_id,
                            section_title=section.title,
                            category=section.category,
                            question_type=q_type,
                            prompt=quiz_text,
                            answer=full_answer,
                            code_language=lang,
                        ))
                    else:
                        questions.append(Question.create(
                            module_id=module_id,
                            section_title=section.title,
                            category=section.category,
                            question_type='free_text',
                            prompt=quiz_text,
                            answer=answer_text,
                        ))

                    quiz_start = None
                    quiz_text = ''
                    answer_text = ''

        # Also check for answer in the NEXT text block if quiz found but no answer in same block
        for match in quiz_matches:
            quiz_text = match.group(1).strip()
            # Find the answer
            after_quiz = text[match.end():]
            a_match = re.search(r'\*\*Answer:?\*\*[:\s]*(.*?)(?:\n\n|$)', after_quiz, re.DOTALL | re.IGNORECASE)
            if a_match:
                answer_text = a_match.group(1).strip()

                if _answer_is_code(answer_text, section.category):
                    lang = 'sql' if section.category == 'sql' else 'python'
                    questions.append(Question.create(
                        module_id=module_id,
                        section_title=section.title,
                        category=section.category,
                        question_type='code_practice',
                        prompt=quiz_text,
                        answer=answer_text,
                        code_language=lang,
                    ))
                else:
                    questions.append(Question.create(
                        module_id=module_id,
                        section_title=section.title,
                        category=section.category,
                        question_type='free_text',
                        prompt=quiz_text,
                        answer=answer_text,
                    ))

    # Also look for code blocks that follow quiz text patterns
    for i, block in enumerate(blocks):
        if block.type == 'text' and i + 2 < len(blocks):
            text = block.content
            if re.search(r'\*\*Quick quiz', text, re.IGNORECASE):
                # Check if we have text -> code (answer) pattern
                next_block = blocks[i + 1]
                if next_block.type == 'code':
                    # Already handled above in most cases
                    pass

    return questions


def extract_self_test(module_id: str, section: Section) -> list:
    """Extract numbered Q&A from Self-Test sections."""
    questions = []
    all_text = '\n'.join(
        block.content for block in section.blocks if block.type == 'text'
    )

    # Split on **Answers:** marker
    parts = re.split(r'\*\*Answers?:?\*\*', all_text, maxsplit=1)
    if len(parts) < 2:
        return questions

    q_text = parts[0]
    a_text = parts[1]

    # Extract numbered questions
    q_matches = re.findall(r'(\d+)\.\s+(.+?)(?=\n\d+\.|\n*$)', q_text, re.DOTALL)
    a_matches = re.findall(r'(\d+)\.\s+(.+?)(?=\n\d+\.|\n*$)', a_text, re.DOTALL)

    answer_map = {int(n): a.strip() for n, a in a_matches}

    for num_str, q in q_matches:
        num = int(num_str)
        answer = answer_map.get(num, '')
        questions.append(Question.create(
            module_id=module_id,
            section_title=section.title,
            category=section.category if section.category != 'review' else 'general',
            question_type='free_text',
            prompt=q.strip(),
            answer=answer,
        ))

    return questions


def extract_round_questions(module_id: str, section: Section) -> list:
    """Extract questions from Module 14's round-based format."""
    questions = []
    title_lower = section.title.lower()

    # Determine question type from round title
    if 'definition' in title_lower:
        q_type = 'flashcard'
    elif 'sql' in title_lower:
        q_type = 'code_practice'
    elif 'python' in title_lower or 'pandas' in title_lower:
        q_type = 'code_practice'
    elif 'behavioral' in title_lower:
        q_type = 'star_practice'
    else:
        q_type = 'free_text'

    # Detect category from round title
    category = section.category
    if category == 'mixed':
        if 'sql' in title_lower:
            category = 'sql'
        elif 'python' in title_lower or 'pandas' in title_lower:
            category = 'python'
        elif 'stats' in title_lower or 'probability' in title_lower:
            category = 'stats'
        elif 'ml' in title_lower:
            category = 'ml'
        elif 'product' in title_lower:
            category = 'product'
        elif 'behavioral' in title_lower:
            category = 'behavioral'
        elif 'definition' in title_lower:
            category = 'terminology'

    # Parse numbered questions with inline or block answers
    blocks = section.blocks
    current_question = None
    current_answer_lines = []

    for bi, block in enumerate(blocks):
        if block.type == 'text':
            lines = block.content.split('\n')
            for line in lines:
                # Numbered question: **N. question** or **N.** question
                q_match = re.match(r'\*\*(\d+)\.?\*\*\s*(.*)', line)
                if not q_match:
                    q_match = re.match(r'\*\*(\d+)\.\s+(.*?)\*\*', line)

                if q_match:
                    # Save previous question
                    if current_question:
                        answer = '\n'.join(current_answer_lines).strip()
                        questions.append(Question.create(
                            module_id=module_id,
                            section_title=section.title,
                            category=category,
                            question_type=q_type,
                            prompt=current_question,
                            answer=answer,
                            code_language='sql' if q_type == 'code_practice' and category == 'sql' else
                                          'python' if q_type == 'code_practice' else None,
                        ))
                        current_answer_lines = []

                    current_question = q_match.group(2).strip().rstrip('*')
                elif current_question:
                    # This is part of the answer
                    if line.strip():
                        current_answer_lines.append(line)

        elif block.type == 'code' and current_question:
            # For code_practice, store raw code; for others, wrap in fences for markdown
            if q_type == 'code_practice':
                current_answer_lines.append(block.content)
            else:
                current_answer_lines.append(f'```{block.language or ""}\n{block.content}\n```')

    # Flush last question
    if current_question:
        answer = '\n'.join(current_answer_lines).strip()
        questions.append(Question.create(
            module_id=module_id,
            section_title=section.title,
            category=category,
            question_type=q_type,
            prompt=current_question,
            answer=answer,
            code_language='sql' if q_type == 'code_practice' and category == 'sql' else
                          'python' if q_type == 'code_practice' else None,
        ))

    return questions


def extract_behavioral(module_id: str, section: Section) -> list:
    """Extract behavioral/STAR practice prompts."""
    questions = []

    for block in section.blocks:
        if block.type != 'text':
            continue

        text = block.content

        # Look for homework prompts
        if 'homework' in text.lower() or 'practice' in text.lower():
            # Extract the prompt
            lines = text.split('\n')
            for line in lines:
                if ('homework' in line.lower() or 'practice saying' in line.lower()) and ':' in line:
                    prompt = line.split(':', 1)[-1].strip().strip('*')
                    if len(prompt) > 20:
                        questions.append(Question.create(
                            module_id=module_id,
                            section_title=section.title,
                            category='behavioral',
                            question_type='star_practice',
                            prompt=prompt,
                            answer='Use the STAR framework: Situation, Task, Action, Result. Keep under 2 minutes.',
                            rubric=[
                                'Used "I" not "we"',
                                'Quantified the result',
                                'Kept under 2 minutes',
                                'Clear situation/context',
                                'Specific actions taken',
                            ],
                        ))

        # Look for quoted behavioral prompts like **"Tell me about..."**
        beh_matches = re.findall(r'\*\*(?:\d+\.\s*)?"([^"]+)"\*\*(?:\s*\((\d+\s*min)\))?', text)
        for prompt, time_limit in beh_matches:
            if any(kw in prompt.lower() for kw in ['tell me', 'describe', 'how do you', 'give me an example']):
                questions.append(Question.create(
                    module_id=module_id,
                    section_title=section.title,
                    category='behavioral',
                    question_type='star_practice',
                    prompt=prompt,
                    answer='Use the STAR framework: Situation, Task, Action, Result.',
                    rubric=[
                        'Used "I" not "we"',
                        'Quantified the result',
                        'Kept under 2 minutes',
                        'Clear situation/context',
                        'Specific actions taken',
                    ],
                ))

    return questions


def _answer_is_code(answer_text: str, category: str) -> bool:
    """Heuristic: does this answer look like code?"""
    if category in ('sql', 'python'):
        return True
    code_indicators = ['SELECT', 'FROM', 'WHERE', 'GROUP BY', 'def ', 'import ',
                       'pd.', 'df.', 'df[', '.loc[', '.groupby(']
    return any(kw in answer_text for kw in code_indicators)
