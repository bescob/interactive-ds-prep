// Quiz progress tracking and STAR timer

// Update progress bar on HTMX swap
document.body.addEventListener('htmx:afterSwap', function(e) {
    var card = document.querySelector('.question-card');
    if (!card) return;

    var idx = parseInt(card.getAttribute('data-idx') || '0');
    var total = parseInt(card.getAttribute('data-total') || '1');

    var progressBar = document.getElementById('quiz-progress');
    var counter = document.getElementById('quiz-counter');

    if (progressBar) progressBar.style.width = ((idx + 1) / total * 100) + '%';
    if (counter) counter.textContent = (idx + 1) + ' / ' + total;

    // Re-highlight code blocks
    document.querySelectorAll('pre code').forEach(function(block) {
        hljs.highlightElement(block);
    });
});

// Multiple choice keyboard shortcuts (1-4)
document.addEventListener('keydown', function(e) {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') return;

    var num = parseInt(e.key);
    if (num >= 1 && num <= 4) {
        var options = document.querySelectorAll('.mc-option input[type="radio"]');
        if (options.length >= num) {
            options[num - 1].checked = true;
            options[num - 1].dispatchEvent(new Event('change'));
        }
    }
});

// STAR timer
var starTimers = {};

function startStarTimer(idx) {
    var duration = 120; // 2 minutes
    var remaining = duration;
    var circle = document.getElementById('timer-circle-' + idx);
    var text = document.getElementById('timer-text-' + idx);
    var circumference = 2 * Math.PI * 45; // r=45

    if (!circle || !text) return;

    circle.style.strokeDasharray = circumference;
    circle.style.strokeDashoffset = 0;

    if (starTimers[idx]) clearInterval(starTimers[idx]);

    starTimers[idx] = setInterval(function() {
        remaining--;
        var minutes = Math.floor(remaining / 60);
        var seconds = remaining % 60;
        text.textContent = minutes + ':' + (seconds < 10 ? '0' : '') + seconds;

        var offset = circumference * (1 - remaining / duration);
        circle.style.strokeDashoffset = offset;

        if (remaining <= 30) {
            circle.style.stroke = '#ef4444';
        } else if (remaining <= 60) {
            circle.style.stroke = '#f59e0b';
        }

        if (remaining <= 0) {
            clearInterval(starTimers[idx]);
            text.textContent = 'Time!';
            circle.style.stroke = '#ef4444';
        }
    }, 1000);
}
