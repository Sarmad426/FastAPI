const quizContainer = document.getElementById('quiz-container');
const questionContainer = document.getElementById('question-container');
const questionElement = document.getElementById('question');
const optionsContainer = document.getElementById('options');
const nextButton = document.getElementById('next-btn');
const resultContainer = document.getElementById('result-container');
const scoreElement = document.getElementById('score');

let quizData = [];
let currentQuestionIndex = 0;
let score = 0;

async function fetchQuizData() {
    const response = await fetch('http://127.0.0.1:8000/');
    quizData = await response.json();
    showQuestion();
}

function showQuestion() {
    if (currentQuestionIndex >= quizData.length) {
        showResults();
        return;
    }

    questionContainer.classList.remove('hidden');
    resultContainer.classList.add('hidden');
    
    const questionData = quizData[currentQuestionIndex];
    questionElement.innerText = questionData.question;
    optionsContainer.innerHTML = '';

    questionData.options.forEach((option, index) => {
        const button = document.createElement('button');
        button.innerText = option;
        button.className = 'block w-full bg-gray-200 text-left py-2 px-4 rounded transition-all duration-300';
        button.onclick = (e) => {
            e.preventDefault()
            button.classList.remove('bg-gray-200')
            button.className +=' bg-[#8f94fb] text-white'
            selectOption(index);
        }
        optionsContainer.appendChild(button);
    });
}

async function selectOption(selectedIndex) {
    console.log('New data here')
    const questionData = quizData[currentQuestionIndex];
    if (selectedIndex === questionData.correct_option) {
        const url = 'http://127.0.0.1:8000/points/add';
        await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
    });
        score++;
    }
    currentQuestionIndex++;
    nextButton.classList.remove('hidden');
    optionsContainer.querySelectorAll('button').forEach(button => button.disabled = true);
}

async function showResults() {
    questionContainer.classList.add('hidden');
    resultContainer.classList.remove('hidden');
    scoreElement.innerText = `Your score is ${score} out of ${quizData.length}`;
}

function restartQuiz() {
    score = 0;
    currentQuestionIndex = 0;
    fetchQuizData();
}

nextButton.onclick = () => {
    nextButton.classList.add('hidden');
    showQuestion();
};

fetchQuizData();
