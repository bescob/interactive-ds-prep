// Flashcard flip animation and keyboard navigation
var currentCardIndex = 0;
var isFlipped = false;

function initFlashcards() {
    if (typeof flashcardData === 'undefined' || !flashcardData.length) return;
    currentCardIndex = 0;
    isFlipped = false;
    showCard(0);
}

function showCard(index) {
    if (typeof flashcardData === 'undefined') return;
    if (index < 0 || index >= flashcardData.length) return;

    currentCardIndex = index;
    isFlipped = false;

    var card = flashcardData[index];
    var inner = document.getElementById('flashcard-inner');
    if (inner) inner.classList.remove('flipped');

    var front = document.getElementById('card-front');
    var back = document.getElementById('card-back');
    var catEl = document.getElementById('card-category');
    var counter = document.getElementById('card-counter');
    var progressBar = document.getElementById('card-progress-bar');

    if (front) front.innerHTML = card.front;
    if (back) back.innerHTML = card.back;
    // Re-highlight any code blocks
    document.querySelectorAll('#flashcard pre code').forEach(function(block) {
        hljs.highlightElement(block);
    });
    if (catEl) {
        catEl.textContent = card.category;
        catEl.className = 'category-tag cat-' + card.category;
    }
    if (counter) counter.textContent = (index + 1) + ' / ' + flashcardData.length;
    if (progressBar) progressBar.style.width = ((index + 1) / flashcardData.length * 100) + '%';
}

function flipCard() {
    var inner = document.getElementById('flashcard-inner');
    if (!inner) return;
    inner.classList.toggle('flipped');
    isFlipped = !isFlipped;
}

function nextCard() {
    if (typeof flashcardData === 'undefined') return;
    if (currentCardIndex < flashcardData.length - 1) {
        showCard(currentCardIndex + 1);
    }
}

function prevCard() {
    if (currentCardIndex > 0) {
        showCard(currentCardIndex - 1);
    }
}

// Keyboard navigation
document.addEventListener('keydown', function(e) {
    if (typeof flashcardData === 'undefined') return;
    // Don't intercept when typing in inputs
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') return;

    if (e.code === 'Space') {
        e.preventDefault();
        flipCard();
    } else if (e.code === 'ArrowRight') {
        e.preventDefault();
        nextCard();
    } else if (e.code === 'ArrowLeft') {
        e.preventDefault();
        prevCard();
    }
});

document.addEventListener('DOMContentLoaded', initFlashcards);
