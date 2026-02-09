// Code editor enhancements for textareas: tab handling, auto-indent

document.addEventListener('keydown', function(e) {
    var target = e.target;
    if (!target.classList.contains('code-editor')) return;

    // Tab key: insert 2 spaces instead of changing focus
    if (e.key === 'Tab') {
        e.preventDefault();
        var start = target.selectionStart;
        var end = target.selectionEnd;
        var value = target.value;

        if (e.shiftKey) {
            // Unindent: remove up to 2 spaces at line start
            var lineStart = value.lastIndexOf('\n', start - 1) + 1;
            var line = value.substring(lineStart, end);
            if (line.startsWith('  ')) {
                target.value = value.substring(0, lineStart) + line.substring(2);
                target.selectionStart = Math.max(start - 2, lineStart);
                target.selectionEnd = Math.max(end - 2, lineStart);
            }
        } else {
            target.value = value.substring(0, start) + '  ' + value.substring(end);
            target.selectionStart = target.selectionEnd = start + 2;
        }
    }

    // Enter: auto-indent to match previous line
    if (e.key === 'Enter') {
        e.preventDefault();
        var start = target.selectionStart;
        var value = target.value;
        var lineStart = value.lastIndexOf('\n', start - 1) + 1;
        var line = value.substring(lineStart, start);
        var indent = line.match(/^\s*/)[0];

        target.value = value.substring(0, start) + '\n' + indent + value.substring(target.selectionEnd);
        target.selectionStart = target.selectionEnd = start + 1 + indent.length;
    }
});
