const quizContainer = document.getElementById('quiz-container');
const questionContainer = document.getElementById('question-container');
const questionElement = document.getElementById('question');
const optionsContainer = document.getElementById('options');
const resultContainer = document.getElementById('result-container');
const scoreElement = document.getElementById('score');

let quizData = [];
let currentQuestionIndex = 0;
let points = 0;

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
        button.onmouseover = () =>{
            button.classList.remove('bg-gray-200')
            button.className +=' bg-[#8f94fb] text-white'
        }
        button.onmouseleave = () =>{
            button.classList.remove('bg-[#8f94fb]','text-white')
            button.className +=' bg-gray-200'
        }
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
    const questionData = quizData[currentQuestionIndex];
    if (selectedIndex === questionData.correct_option) {
        points++;
    }
    currentQuestionIndex++;
    showQuestion()
}

async function showResults() {
//     const url = `http://127.0.0.1:8000/points/update/?points=${points}`;
//     await fetch(url, {
//         method: 'PATCH',
//         headers: {
//             'Content-Type': 'application/json'
//         },
// });
    questionContainer.classList.add('hidden');
    resultContainer.classList.remove('hidden');
    scoreElement.innerText = `Your points is ${points} out of ${quizData.length}`;
}

function restartQuiz() {
    points = 0;
    currentQuestionIndex = 0;
    fetchQuizData();
}

fetchQuizData();
