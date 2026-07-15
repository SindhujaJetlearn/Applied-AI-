// 1. Background Stars Generation
function generateStars() {
    const starfield = document.getElementById('starfield');
    for (let i = 0; i < 180; i++) {
        let star = document.createElement('div');
        star.classList.add('star');
        star.style.width = Math.random() * 3 + 'px';
        star.style.height = star.style.width;
        star.style.left = Math.random() * 100 + 'vw';
        star.style.top = Math.random() * 100 + 'vh';
        star.style.animationDelay = Math.random() * 3 + 's';
        starfield.appendChild(star);
    }

    // Shooting stars
    for (let i = 0; i < 3; i++) {
        let shootingStar = document.createElement('div');
        shootingStar.classList.add('shooting-star');
        shootingStar.style.left = Math.random() * 100 + 'vw';
        shootingStar.style.top = Math.random() * 50 + 'vh';
        shootingStar.style.animationDelay = Math.random() * 10 + 's';
        starfield.appendChild(shootingStar);
    }
}

generateStars();

// 2. 3D Tilt Effect for Archive Cards
const cards = document.querySelectorAll('[data-tilt]');
cards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        
        const rotateX = ((y - centerY) / centerY) * -10; // Max rotation 10deg
        const rotateY = ((x - centerX) / centerX) * 10;
        
        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
    });
    
    card.addEventListener('mouseleave', () => {
        card.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg)`;
        card.style.transition = 'transform 0.5s ease';
        setTimeout(() => card.style.transition = 'transform 0.1s', 500);
    });
});

// 3. Quiz Logic
const quizData = [
    {
        question: "Which mission first returned samples from the lunar far side?",
        options: ["Apollo 11", "Chang'e 6", "Luna 16", "Artemis I"],
        correct: 1
    },
    {
        question: "Who was the first person to walk on the Moon?",
        options: ["Buzz Aldrin", "Yuri Gagarin", "Neil Armstrong", "Michael Collins"],
        correct: 2
    },
    {
        question: "Which space agency launched Chandrayaan-3?",
        options: ["NASA", "ESA", "CNSA", "ISRO"],
        correct: 3
    },
    {
        question: "What is the primary goal of the Artemis program?",
        options: ["Mine helium-3", "Establish sustainable lunar presence", "Find alien life", "Test nuclear rockets"],
        correct: 1
    },
    {
        question: "In what year did the first human-made object (Luna 2) impact the moon?",
        options: ["1957", "1959", "1962", "1969"],
        correct: 1
    },
    {
        question: "How many humans have walked on the moon?",
        options: ["8", "10", "12", "14"],
        correct: 2
    }
];

let currentQuestion = 0;
let score = 0;

const questionEl = document.getElementById('question-text');
const optionsEl = document.getElementById('options-container');
const progressFill = document.querySelector('.progress-fill');

function loadQuiz() {
    if (currentQuestion >= quizData.length) {
        showResults();
        return;
    }
    
    const currentQ = quizData[currentQuestion];
    questionEl.innerText = currentQ.question;
    optionsEl.innerHTML = '';
    
    progressFill.style.width = `${(currentQuestion / quizData.length) * 100}%`;
    
    currentQ.options.forEach((opt, index) => {
        const btn = document.createElement('button');
        btn.classList.add('quiz-btn');
        btn.innerText = opt;
        btn.onclick = () => checkAnswer(index, btn);
        optionsEl.appendChild(btn);
    });
}

function checkAnswer(selectedIndex, btn) {
    const correctIndex = quizData[currentQuestion].correct;
    
    // Disable all buttons
    Array.from(optionsEl.children).forEach(b => b.style.pointerEvents = 'none');
    
    if (selectedIndex === correctIndex) {
        btn.classList.add('correct');
        score++;
    } else {
        btn.classList.add('incorrect');
        optionsEl.children[correctIndex].classList.add('correct');
    }
    
    setTimeout(() => {
        currentQuestion++;
        loadQuiz();
    }, 1500);
}

function showResults() {
    progressFill.style.width = '100%';
    optionsEl.innerHTML = '';
    if (score === quizData.length) {
        questionEl.innerHTML = `Mission Accomplished! Perfect Score. <span class="teal">${score}/${quizData.length}</span>`;
        triggerConfetti();
    } else {
        questionEl.innerHTML = `Simulation Complete. Score: <span class="gold">${score}/${quizData.length}</span>`;
        const retryBtn = document.createElement('button');
        retryBtn.classList.add('btn-glow');
        retryBtn.style.margin = '20px auto';
        retryBtn.style.display = 'block';
        retryBtn.innerText = 'RESTART SIMULATION';
        retryBtn.onclick = () => {
            currentQuestion = 0;
            score = 0;
            loadQuiz();
        };
        optionsEl.appendChild(retryBtn);
    }
}

function triggerConfetti() {
    const container = document.getElementById('confetti-container');
    for (let i = 0; i < 50; i++) {
        let conf = document.createElement('div');
        conf.style.position = 'absolute';
        conf.style.width = '10px';
        conf.style.height = '10px';
        conf.style.backgroundColor = ['#ffd54f', '#5bb8ff', '#4eff9a', '#d8aaff'][Math.floor(Math.random()*4)];
        conf.style.left = '50%';
        conf.style.bottom = '50%';
        conf.style.borderRadius = Math.random() > 0.5 ? '50%' : '0';
        conf.style.transform = `translate(-50%, -50%)`;
        
        let tx = (Math.random() - 0.5) * 500;
        let ty = (Math.random() - 0.5) * 500;
        
        conf.animate([
            { transform: `translate(0,0) scale(1)`, opacity: 1 },
            { transform: `translate(${tx}px, ${ty}px) scale(0)`, opacity: 0 }
        ], {
            duration: 1000 + Math.random() * 1000,
            easing: 'cubic-bezier(0, .9, .57, 1)'
        });
        
        container.appendChild(conf);
        setTimeout(() => conf.remove(), 2000);
    }
}

loadQuiz();

// 4. L.U.N.A Assistant (Voice Engine)
const lunaBtn = document.getElementById('luna-btn');
const lunaTerminal = document.getElementById('luna-terminal');
const lunaOutput = document.getElementById('luna-output');

let isListening = false;
let synthesis = window.speechSynthesis;
let recognition = null;
let hasGreeted = false;

// Lunar Knowledge Base
const moonKnowledge = {
    "apollo 11": "Apollo 11 was the first spaceflight that landed humans on the Moon in 1969.",
    "artemis": "The Artemis program aims to return humans to the Moon and establish a sustainable presence.",
    "chandrayaan": "Chandrayaan-3 is an ISRO mission that successfully landed near the lunar south pole in 2023.",
    "chang'e": "Chang'e missions are Chinese lunar exploration missions. Chang'e 6 recently returned samples from the far side.",
    "luna 2": "Luna 2 was a Soviet spacecraft that became the first human-made object to reach the Moon in 1959.",
    "water": "Recent missions have confirmed the presence of water ice in permanently shadowed craters at the lunar poles.",
    "distance": "The Moon is approximately 384,400 kilometers away from Earth.",
    "gravity": "The Moon's surface gravity is about one-sixth of Earth's gravity."
};

function speak(text) {
    if(synthesis.speaking) synthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    
    // Select premium voice
    let voices = synthesis.getVoices();
    let selectedVoice = voices.find(v => v.name.includes('Samantha') || v.name.includes('Google UK English Female') || v.name.includes('Female'));
    if (selectedVoice) {
        utterance.voice = selectedVoice;
    }
    
    utterance.pitch = 1.1; // Crisp digital feel
    utterance.rate = 1.0;
    
    lunaOutput.innerHTML = `<span class="teal">></span> ${text}`;
    synthesis.speak(utterance);
}

// Initialize Speech Recognition
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    
    recognition.onstart = () => {
        isListening = true;
        lunaBtn.classList.add('listening');
        lunaBtn.style.background = 'rgba(78, 255, 154, 0.2)';
        lunaOutput.innerHTML = `<span class="gold">></span> Listening...`;
    };
    
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript.toLowerCase();
        lunaOutput.innerHTML = `<span class="gold">></span> You asked: "${transcript}"`;
        
        let found = false;
        for (let key in moonKnowledge) {
            if (transcript.includes(key)) {
                setTimeout(() => speak(moonKnowledge[key]), 1000);
                found = true;
                break;
            }
        }
        
        if (!found) {
            setTimeout(() => speak("I do not have data on that query. Try asking about Apollo, Artemis, or Chandrayaan."), 1000);
        }
    };
    
    recognition.onerror = (event) => {
        lunaOutput.innerHTML = `<span class="coral">></span> Error: ${event.error}`;
        isListening = false;
        lunaBtn.style.background = 'transparent';
    };
    
    recognition.onend = () => {
        isListening = false;
        lunaBtn.style.background = 'transparent';
    };
} else {
    lunaOutput.innerHTML = "Voice recognition not supported in this browser.";
}

lunaBtn.addEventListener('click', () => {
    lunaTerminal.classList.toggle('hidden');
    
    if (!lunaTerminal.classList.contains('hidden') && !hasGreeted) {
        speak("Hello, I am L.U.N.A, the Lunar Universal Navigation Assistant. How can I help you explore?");
        hasGreeted = true;
    } else if (recognition && !isListening) {
        try {
            recognition.start();
        } catch(e) {
            console.error(e);
        }
    }
});

// Ensure voices load
speechSynthesis.onvoiceschanged = () => {
    synthesis.getVoices();
};
