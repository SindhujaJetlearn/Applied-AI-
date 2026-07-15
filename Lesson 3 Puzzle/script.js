document.addEventListener('DOMContentLoaded', () => {
    // UI Elements
    const mainMenu = document.getElementById('main-menu');
    const startGameBtn = document.getElementById('start-game-btn');
    const appContainer = document.getElementById('app-container');
    const terminalDisplay = document.getElementById('terminal-display');
    const commandInput = document.getElementById('command-input');
    const inventoryList = document.getElementById('inventory-list');
    const puzzleOptions = document.getElementById('puzzle-options');
    
    let currentLevel = 0;
    const inventory = [];

    // Puzzle Data
    const levels = [
        {
            title: "LEVEL 1: INITIALIZATION",
            narrative: "SYSTEM: Sector 1 firewall engaged. Access requires resolving a basic loop.",
            question: "What is the final value of 'x' in this Python code?\n\nx = 0\nfor i in range(3):\n    x += i",
            options: [
                { text: "3", correct: true },
                { text: "2", correct: false },
                { text: "6", correct: false },
                { text: "Error", correct: false }
            ],
            reward: { name: "Basic Bypass Module", icon: "🔌" }
        },
        {
            title: "LEVEL 2: MEMORY LEAK",
            narrative: "SYSTEM: Proceeding to Sector 2. A memory allocation error blocks the path.",
            question: "Which JavaScript keyword is used to declare a block-scoped variable that CANNOT be reassigned?",
            options: [
                { text: "var", correct: false },
                { text: "let", correct: false },
                { text: "const", correct: true },
                { text: "static", correct: false }
            ],
            reward: { name: "RAM Upgrade", icon: "💾" }
        },
        {
            title: "LEVEL 3: STYLING THE MATRIX",
            narrative: "SYSTEM: Visual processors misaligned. Recalibration needed.",
            question: "In CSS Flexbox, which property is used to center items horizontally across the main axis?",
            options: [
                { text: "align-items", correct: false },
                { text: "justify-content", correct: true },
                { text: "text-align", correct: false },
                { text: "place-content", correct: false }
            ],
            reward: { name: "Optic Visor", icon: "👓" }
        },
        {
            title: "LEVEL 4: DATA EXTRACTION",
            narrative: "SYSTEM: Querying mainframe... Authentication required for database access.",
            question: "Which SQL command is used to retrieve data from a database?",
            options: [
                { text: "GET", correct: false },
                { text: "EXTRACT", correct: false },
                { text: "SELECT", correct: true },
                { text: "PULL", correct: false }
            ],
            reward: { name: "Master Key", icon: "🔑" }
        },
        {
            title: "LEVEL 5: CORE OVERRIDE",
            narrative: "SYSTEM: Warning! Core destabilizing. Final override sequence required.",
            question: "What does the command 'git commit -m \"fix\"' do?",
            options: [
                { text: "Pushes changes to remote", correct: false },
                { text: "Saves changes to local repository", correct: true },
                { text: "Adds files to staging area", correct: false },
                { text: "Creates a new branch", correct: false }
            ],
            reward: { name: "Root Access Token", icon: "👑" }
        }
    ];

    // Initialize Game
    startGameBtn.addEventListener('click', () => {
        mainMenu.style.opacity = '0';
        setTimeout(() => {
            mainMenu.style.display = 'none';
            appContainer.style.display = 'flex';
            loadLevel(currentLevel);
        }, 500);
    });

    // Focus input on click anywhere except buttons
    document.addEventListener('click', (e) => {
        if (e.target.tagName !== 'BUTTON' && !e.target.classList.contains('puzzle-btn')) {
            commandInput.focus();
        }
    });

    // Command line logic (kept for flavor, though puzzles use buttons)
    commandInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            const val = commandInput.value.trim();
            if (val) {
                processCommand(val);
                commandInput.value = '';
            }
        }
    });

    function processCommand(cmd) {
        appendMessage(`> ${cmd}`, 'player');
        const action = cmd.toLowerCase();

        setTimeout(() => {
            if (action === 'clear') {
                terminalDisplay.innerHTML = '';
            } else if (action === 'help') {
                appendMessage('SYSTEM: Use the interactive buttons to solve the current puzzle. Commands: clear, help, status', 'system');
            } else if (action === 'status') {
                appendMessage(`SYSTEM: Current Level ${currentLevel + 1}/${levels.length}.`, 'system');
            } else {
                appendMessage(`COMMAND NOT RECOGNIZED: ${action}. The current terminal requires puzzle resolution via visual interface.`, 'error');
            }
        }, 400);
    }

    function loadLevel(index) {
        terminalDisplay.innerHTML = ''; // Clear terminal for new level
        puzzleOptions.innerHTML = ''; // Clear options
        
        if (index >= levels.length) {
            // Game Over / Victory
            puzzleOptions.style.display = 'none';
            appendMessage('SYSTEM: ALL OVERRIDES ACCEPTED.', 'system');
            appendMessage('SYSTEM: FULL ROOT ACCESS GRANTED. WELCOME, ADMIN.', 'system');
            const winMsg = document.createElement('div');
            winMsg.className = 'message puzzle';
            winMsg.innerHTML = '<span class="puzzle-title" style="font-size:2rem; text-align:center;">YOU WIN</span>';
            terminalDisplay.appendChild(winMsg);
            return;
        }

        const level = levels[index];
        puzzleOptions.style.display = 'flex';

        // Render narrative and question
        appendMessage(level.narrative, 'system');
        
        const puzzleMsg = document.createElement('div');
        puzzleMsg.className = 'message puzzle';
        
        const titleSpan = document.createElement('span');
        titleSpan.className = 'puzzle-title';
        titleSpan.textContent = level.title;
        
        const qText = document.createElement('pre');
        qText.style.fontFamily = 'var(--font-mono)';
        qText.style.whiteSpace = 'pre-wrap';
        qText.textContent = level.question;

        puzzleMsg.appendChild(titleSpan);
        puzzleMsg.appendChild(qText);
        terminalDisplay.appendChild(puzzleMsg);

        // Render buttons
        level.options.forEach(opt => {
            const btn = document.createElement('button');
            btn.className = 'puzzle-btn';
            btn.textContent = opt.text;
            btn.addEventListener('click', () => handleAnswer(opt.correct, level.reward));
            puzzleOptions.appendChild(btn);
        });

        terminalDisplay.scrollTop = terminalDisplay.scrollHeight;
    }

    function handleAnswer(isCorrect, reward) {
        if (isCorrect) {
            appendMessage(`> Correct. Security bypassed.`, 'player');
            appendMessage(`SYSTEM: Access granted. Reward acquired: [${reward.name}]`, 'system');
            addItemToInventory(reward.name, reward.icon);
            
            // Disable buttons temporarily
            Array.from(puzzleOptions.children).forEach(b => b.disabled = true);
            
            setTimeout(() => {
                currentLevel++;
                loadLevel(currentLevel);
            }, 2000);
        } else {
            appendMessage(`> Analyzing answer...`, 'player');
            appendMessage(`SYSTEM: INCORRECT RESPONSE. ACCESS DENIED. Try again.`, 'error');
        }
        terminalDisplay.scrollTop = terminalDisplay.scrollHeight;
    }

    function appendMessage(text, type) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${type}`;
        msgDiv.textContent = text;
        terminalDisplay.appendChild(msgDiv);
        terminalDisplay.scrollTop = terminalDisplay.scrollHeight;
    }

    function addItemToInventory(name, iconChar) {
        if (!inventory.includes(name)) {
            inventory.push(name);
            const li = document.createElement('li');
            li.className = 'inventory-item';
            li.innerHTML = `
                <div class="item-icon">${iconChar}</div>
                <span class="item-label">${name}</span>
            `;
            inventoryList.appendChild(li);
        }
    }
});
