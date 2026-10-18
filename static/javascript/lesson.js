const submitForm = document.getElementById('submitForm');
const bodyDataset = document.getElementById('page-body').dataset;
const answer = bodyDataset.answer.trim().toLowerCase();
const id = bodyDataset.id;
const answerInput = document.getElementById('lesson-answer');
const correctCard = document.getElementById('correctCard');
const wrongCard = document.getElementById('wrongCard');


submitForm.addEventListener('submit', function(event) {
    const userInput = new FormData(submitForm).get('answer');

    event.preventDefault();
    const isCorrect = typeof userInput === 'string' && userInput.trim().toLowerCase() === answer;
    const activeCard = isCorrect ? correctCard : wrongCard;
    activeCard.hidden = false;
    activeCard.classList.add('active');
});


document.querySelectorAll('[data-continue]').forEach((button) => {
    button.addEventListener('click', () => {
        window.location.assign(`/lesson/${id}/submit`);
    });
});

document.querySelectorAll('[data-retry]').forEach((button) => {
    button.addEventListener('click', () => {
        wrongCard.classList.remove('active');
        wrongCard.hidden = true;
        answerInput.focus();
    });
});