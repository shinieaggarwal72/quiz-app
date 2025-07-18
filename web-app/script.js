let questions = [];
let currentIndex = 0;
let score = 0;
let timerId = null;
const TIME_PER_Q = 15; // secs


async function loadQuestions() {
  const res = await fetch('questions.json');
  questions = await res.json();
  document.getElementById('total').textContent = questions.length;
  showQuestion();
}

function showQuestion() {
  if (currentIndex >= questions.length) {
    return showResult();
  }
  const q = questions[currentIndex];


  document.getElementById('questionText').textContent = q.question;


  const optsEl = document.getElementById('options');
  optsEl.innerHTML = '';
  q.options.forEach((optText, idx) => {
    const btn = document.createElement('button');
    btn.textContent = optText;
    btn.onclick = () => selectOption(idx, btn);
    optsEl.appendChild(btn);
  });


  const nextBtn = document.getElementById('nextBtn');
  nextBtn.disabled = true;

  startTimer();
}

function startTimer() {
  clearInterval(timerId);
  let t = TIME_PER_Q;
  document.getElementById('countdown').textContent = t;
  timerId = setInterval(() => {
    t--;
    document.getElementById('countdown').textContent = t;
    if (t <= 0) {
      clearInterval(timerId);
      document.getElementById('beep').play();
      enableNext();
    }
  }, 1000);
}

function selectOption(idx, btn) {
  document.querySelectorAll('#options button').forEach(b => b.disabled = true);
  btn.classList.add('selected');

  clearInterval(timerId);

  if (questions[currentIndex].answer === idx) {
    score++;
  }

  enableNext();
}

function enableNext() {
  document.getElementById('nextBtn').disabled = false;
}

function nextQuestion() {
  currentIndex++;
  showQuestion();
}

function showResult() {
  document.getElementById('quiz-card').classList.add('hidden');
  const resEl = document.getElementById('result');
  resEl.classList.remove('hidden');
  document.getElementById('score').textContent = score;
}

loadQuestions();
