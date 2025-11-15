/**
 * RequirementRally Game Logic - FIXED VERSION
 * Independent game for requirement type identification
 * Connects to main server on port 8000
 */

// Translations for internationalization
const translations = {
    es: {
        title: "RequirementRally",
        subtitle: "Aprende a identificar tipos de requisitos de software",
        welcome: "¡Bienvenido a RequirementRally!",
        description: "Identifica tipos de requisitos en situaciones reales de desarrollo",
        gameDescription: "En este juego analizarás diferentes declaraciones de requisitos y determinarás si son Funcionales, No-Funcionales o Restricciones.",
        requirementTypes: "Tipos de Requisitos",
        functional: "Funcional",
        nonFunctional: "No-Funcional", 
        constraint: "Restricción",
        functionalDesc: "Describe QUÉ debe hacer el sistema. Funciones y características específicas.",
        nonFunctionalDesc: "Describe CÓMO debe funcionar. Calidad, rendimiento, seguridad.",
        constraintDesc: "Limitaciones y restricciones del proyecto o sistema.",
        functionalExample: 'Ej: "El sistema debe enviar emails"',
        nonFunctionalExample: 'Ej: "El sistema debe responder en 2 segundos"',
        constraintExample: 'Ej: "Debe usar tecnología Java"',
        step1: "Lee cada declaración de requisito cuidadosamente",
        step2: "Clasifica el requisito como Funcional, No-Funcional o Restricción",
        step3: "Envía tu respuesta y aprende de la explicación",
        step4: "Gana puntos por respuestas correctas",
        howToPlay: "Cómo Jugar",
        gameSettings: "Configuración del Juego",
        playerName: "Nombre del Jugador",
        player: "Jugador",
        playerNamePlaceholder: "Tu nombre",
        category: "Categoría",
        allTypes: "Todos los tipos",
        onlyFunctional: "Solo Funcionales",
        onlyNonFunctional: "Solo No-Funcionales",
        onlyConstraints: "Solo Restricciones",
        startGame: "Comenzar Juego",
        requirement: "Requisito",
        points: "Puntos",
        points: "Puntos",
        questionType: "¿Qué tipo de requisito es?",
        loading: "Cargando requisito...",
        submit: "Enviar Respuesta",
        continue: "Continuar",
        correct: "¡Correcto!",
        incorrect: "Incorrecto",
        correctAnswer: "Respuesta correcta:",
        finalScore: "Puntuación Final",
        playAgain: "Jugar de Nuevo",
        gameCompleted: "¡Juego Completado!",
        score: "Puntuación",
        knowledge: "Conocimiento",
        knowledgeDesc: "Comprensión de tipos de requisitos",
        application: "Aplicación",
        applicationDesc: "Capacidad para clasificar requisitos",
        speed: "Velocidad",
        speedDesc: "Eficiencia en la toma de decisiones",
        excellent: "¡Excelente! Dominas la clasificación de requisitos",
        veryGood: "Muy bien. Tienes buen entendimiento",
        good: "Bien. Sigue practicando para mejorar",
        needsPractice: "Necesitas más práctica. ¡Inténtalo de nuevo!",
        selectOption: "Por favor selecciona una opción",
        connectionError: "No se puede conectar al servidor. Asegúrate de que el servidor principal esté ejecutándose en 127.0.0.1:8001.",
        gameStartError: "Error al iniciar el juego: ",
        submitError: "Error al enviar respuesta: "
    },
    en: {
        title: "RequirementRally",
        subtitle: "Learn to identify software requirement types",
        welcome: "Welcome to RequirementRally!",
        description: "Identify requirement types in real development situations",
        gameDescription: "In this game you will analyze different requirement statements and determine if they are Functional, Non-Functional, or Constraints.",
        requirementTypes: "Requirement Types",
        functional: "Functional",
        nonFunctional: "Non-Functional",
        constraint: "Constraint",
        functionalDesc: "Describes WHAT the system must do. Specific functions and features.",
        nonFunctionalDesc: "Describes HOW the system must perform. Quality, performance, security.",
        constraintDesc: "Limitations and restrictions on the project or system.",
        functionalExample: 'Ex: "The system must send emails"',
        nonFunctionalExample: 'Ex: "The system must respond in 2 seconds"',
        constraintExample: 'Ex: "Must use Java technology"',
        step1: "Read each requirement statement carefully",
        step2: "Classify the requirement as Functional, Non-Functional or Constraint",
        step3: "Submit your answer and learn from the explanation",
        step4: "Earn points for correct answers",
        howToPlay: "How to Play",
        gameSettings: "Game Settings",
        playerName: "Player Name",
        player: "Player",
        playerNamePlaceholder: "Your name",
        category: "Category",
        allTypes: "All types",
        onlyFunctional: "Only Functional",
        onlyNonFunctional: "Only Non-Functional",
        onlyConstraints: "Only Constraints",
        startGame: "Start Game",
        requirement: "Requirement",
        points: "Points",
        points: "Points",
        questionType: "What type of requirement is this?",
        loading: "Loading requirement...",
        submit: "Submit Answer",
        continue: "Continue",
        correct: "Correct!",
        incorrect: "Incorrect",
        correctAnswer: "Correct answer:",
        finalScore: "Final Score",
        playAgain: "Play Again",
        gameCompleted: "Game Completed!",
        score: "Score",
        knowledge: "Knowledge",
        knowledgeDesc: "Understanding of requirement types",
        application: "Application",
        applicationDesc: "Ability to classify requirements",
        speed: "Speed",
        speedDesc: "Decision-making efficiency",
        excellent: "Excellent! You master requirement classification",
        veryGood: "Very good! You have good understanding",
        good: "Good. Keep practicing to improve",
        needsPractice: "You need more practice. Try again!",
        selectOption: "Please select an option",
        connectionError: "Cannot connect to server. Make sure the main server is running on 127.0.0.1:8001.",
        gameStartError: "Error starting game: ",
        submitError: "Error submitting answer: "
    }
};

class RequirementRallyGame {
    constructor() {
        this.apiUrl = 'http://127.0.0.1:8001';
        this.sessionId = null;
        this.currentScenario = null;
        this.score = 0;
        this.scenarioNumber = 1;
        this.totalScenarios = 5; // Default, will be updated by server
        this.selectedOption = null;
        this.language = 'en'; // INGLÉS por defecto como solicitado
        
        this.init();
    }

    init() {
        console.log('🎯 Initializing RequirementRally Game');
        console.log('🌐 Default language set to:', this.language);
        this.bindEvents();
        this.setupLanguageSelector();
        this.updateUI();
        // Temporarily disable server check to isolate the issue
        // this.checkServerConnection();
    }

    // Get translated text for current language
    t(key) {
        return translations[this.language] && translations[this.language][key] 
            ? translations[this.language][key] 
            : translations['es'][key] || key;
    }

    // Update all UI text based on current language
    updateUI() {
        console.log(`🌐 Updating UI to ${this.language}`);
        
        // Simple element translation map
        const elementsToTranslate = {
            'subtitle': 'subtitle',
            'header-functional': 'functional',
            'header-nonfunctional': 'nonFunctional',
            'header-constraint': 'constraint',
            'welcome-title': 'welcome',
            'welcome-description': 'description',
            'game-settings-title': 'gameSettings',
            'player-name-label': 'playerName',
            'category-label': 'category',
            'loading-text': 'loading',
            'step-1': 'step1',
            'step-2': 'step2',
            'step-3': 'step3',
            'step-4': 'step4'
        };
        
        // Translate elements using data-translate attribute
        document.querySelectorAll('[data-translate]').forEach(element => {
            const key = element.getAttribute('data-translate');
            const translatedText = this.t(key);
            if (translatedText !== key) { // Only update if translation found
                element.textContent = translatedText;
            }
        });
        
        // Translate simple elements
        Object.entries(elementsToTranslate).forEach(([elementId, translationKey]) => {
            const element = document.getElementById(elementId);
            if (element) {
                const translatedText = this.t(translationKey);
                element.textContent = translatedText;
                console.log(`✅ Translated ${elementId}: "${translatedText}"`);
            } else {
                console.warn(`⚠️ Element not found: ${elementId}`);
            }
        });
        
        this.updateSpecialElements();
        console.log('🌐 UI update complete');
    }
    
    updateSpecialElements() {
        // Update category select options
        const select = document.getElementById('category-filter');
        if (select) {
            select.innerHTML = `
                <option value="">${this.t('allTypes')}</option>
                <option value="Functional">${this.t('onlyFunctional')}</option>
                <option value="Non-Functional">${this.t('onlyNonFunctional')}</option>
                <option value="Constraint">${this.t('onlyConstraints')}</option>
            `;
        }
        
        // Update player name placeholder
        const playerInput = document.getElementById('player-name');
        if (playerInput) {
            playerInput.placeholder = this.t('playerNamePlaceholder');
        }
    }

    async checkServerConnection() {
        try {
            console.log('🔗 Checking server connection...');
            const response = await fetch(`${this.apiUrl}/rally/stats`);
            if (response.ok) {
                console.log('✅ Server connection successful');
            } else {
                throw new Error(`Server responded with ${response.status}`);
            }
        } catch (error) {
            console.error('❌ Server connection failed:', error);
            this.showError(this.t('connectionError'));
        }
    }

    bindEvents() {
        console.log('🔗 Binding events...');
        
        // Start game button
        const startBtn = document.getElementById('start-game-btn');
        if (startBtn) {
            startBtn.addEventListener('click', () => {
                console.log('🎯 Start game button clicked');
                this.startGame();
            });
            console.log('✅ Start game button event bound');
        } else {
            console.error('❌ Start game button not found');
        }

        // Option clicks
        document.querySelectorAll('.option').forEach(option => {
            option.addEventListener('click', (e) => {
                this.selectOption(e.currentTarget);
            });
        });

        // Submit button
        const submitBtn = document.getElementById('submit-btn');
        if (submitBtn) {
            submitBtn.addEventListener('click', () => {
                this.submitAnswer();
            });
        }

        // Continue button
        const continueBtn = document.getElementById('continue-btn');
        if (continueBtn) {
            continueBtn.addEventListener('click', () => {
                const action = continueBtn.getAttribute('data-action');
                if (action === 'show-results') {
                    this.showResults();
                } else if (action === 'next-question') {
                    this.nextQuestion();
                }
            });
        }

        // Play again button
        const playAgainBtn = document.getElementById('play-again-btn');
        if (playAgainBtn) {
            playAgainBtn.addEventListener('click', () => {
                this.resetGame();
            });
        }

        // Language selectors
        const langButtons = document.querySelectorAll('.language-selector');
        console.log(`🌐 Found ${langButtons.length} language buttons`);
        
        langButtons.forEach((btn, index) => {
            console.log(`🌐 Setting up language button ${index + 1}: ${btn.id}`);
            btn.addEventListener('click', (e) => {
                console.log(`🌐 Language button clicked: ${e.currentTarget.id}`);
                const lang = e.currentTarget.id.split('-')[1];
                console.log(`🌐 Extracted language: ${lang}`);
                this.changeLanguage(lang);
            });
        });
        
        console.log('✅ All events bound');
    }

    setupLanguageSelector() {
        console.log(`🌐 Setting up language selector for: ${this.language}`);
        
        // Remove active state from all buttons
        document.querySelectorAll('.language-selector').forEach(btn => {
            btn.classList.remove('bg-opacity-30');
            btn.classList.add('bg-opacity-20');
            console.log(`🔄 Reset button: ${btn.id}`);
        });
        
        // Highlight current language
        const currentLangBtn = document.getElementById(`lang-${this.language}`);
        if (currentLangBtn) {
            currentLangBtn.classList.remove('bg-opacity-20');
            currentLangBtn.classList.add('bg-opacity-30');
            console.log(`✅ Activated language button: lang-${this.language}`);
        } else {
            console.error(`❌ Language button not found: lang-${this.language}`);
        }
    }

    changeLanguage(lang) {
        console.log(`🌐 Changing language from ${this.language} to ${lang}`);
        this.language = lang;
        this.setupLanguageSelector();
        this.updateUI();
        
        // If we have an active session, we need to restart to get scenarios in the new language
        if (this.sessionId) {
            console.log('🔄 Restarting session for new language');
            this.resetGame();
        }
        
        // Update current scenario display if we're in game
        if (this.currentScenario) {
            this.translateResultScreen();
        }
    }

    async startGame() {
        try {
            console.log('🎯 Starting RequirementRally game...');
            console.log('🔍 Current language before starting:', this.language);
            
            const playerNameInput = document.getElementById('player-name');
            const categoryFilter = document.getElementById('category-filter');
            
            if (!playerNameInput || !categoryFilter) {
                throw new Error('Required form elements not found');
            }
            
            const playerName = playerNameInput.value.trim() || 'Jugador';
            const category = categoryFilter.value || null;
            
            console.log(`🎯 Starting game for: ${playerName}`);
            console.log(`   Category: ${category || 'all'}`);
            console.log(`   Language: ${this.language}`);

            const requestBody = {
                name: playerName,
                category: category,
                language: this.language
            };
            
            console.log('📤 Sending request:', JSON.stringify(requestBody));

            const response = await fetch(`${this.apiUrl}/rally/session`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody)
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP ${response.status}: ${errorText}`);
            }

            const data = await response.json();
            console.log('✅ Game session created:', data);

            if (!data.session_id || !data.current_scenario) {
                throw new Error('Invalid response from server');
            }

            this.sessionId = data.session_id;
            this.currentScenario = data.current_scenario;
            
            // Update total scenarios if provided by server
            if (data.total_scenarios) {
                this.totalScenarios = data.total_scenarios;
                console.log(`📊 Total scenarios set to: ${this.totalScenarios}`);
            }
            
            this.showGameScreen();
            this.loadScenario(this.currentScenario);

        } catch (error) {
            console.error('❌ Error starting game:', error);
            this.showError(this.t('gameStartError') + error.message);
        }
    }

    showGameScreen() {
        document.getElementById('intro-screen').classList.add('hidden');
        document.getElementById('game-screen').classList.remove('hidden');
        document.getElementById('result-screen').classList.add('hidden');
        
        // Update player name display
        const playerNameInput = document.getElementById('player-name');
        const currentPlayerNameEl = document.getElementById('current-player-name');
        if (playerNameInput && currentPlayerNameEl) {
            const playerName = playerNameInput.value.trim() || 'Guest Player';
            currentPlayerNameEl.textContent = playerName;
        }
    }

    showResultScreen() {
        document.getElementById('intro-screen').classList.add('hidden');
        document.getElementById('game-screen').classList.add('hidden');
        document.getElementById('result-screen').classList.remove('hidden');
    }

    showIntroScreen() {
        document.getElementById('intro-screen').classList.remove('hidden');
        document.getElementById('game-screen').classList.add('hidden');
        document.getElementById('result-screen').classList.add('hidden');
    }

    loadScenario(scenario) {
        console.log('📄 Loading scenario:', scenario.id);
        
        // Update scenario content
        document.getElementById('scenario').innerHTML = `
            <div class="flex items-start">
                <div class="bg-green-600 text-white p-2 rounded-lg mr-4 flex-shrink-0">
                    <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                </div>
                <div>
                    <div class="text-sm text-gray-500 mb-2">ID: ${scenario.id} | Dificultad: ${scenario.difficulty || 'N/A'}</div>
                    <p class="text-lg text-gray-800">${scenario.content}</p>
                </div>
            </div>
        `;

        // Load options
        const options = document.querySelectorAll('.option');
        console.log(`📝 Loading ${scenario.options.length} options`);
        
        scenario.options.forEach((option, index) => {
            if (index < options.length) {
                const optionDiv = options[index];
                const textDiv = optionDiv.querySelector('.font-medium');
                
                if (textDiv) {
                    textDiv.textContent = option;
                    console.log(`✅ Option ${index + 1}: "${option}"`);
                } else {
                    console.error(`❌ Could not find .font-medium in option ${index + 1}`);
                }
            }
        });

        // Update scenario number
        const scenarioNumberEl = document.getElementById('scenario-number');
        if (scenarioNumberEl) {
            scenarioNumberEl.textContent = this.scenarioNumber;
        }
        
        // Update total scenarios in the requirement label
        const requirementLabel = document.getElementById('requirement-label');
        if (requirementLabel) {
            const currentText = requirementLabel.innerHTML;
            const updatedText = currentText.replace(/\/\d+/, `/${this.totalScenarios}`);
            requirementLabel.innerHTML = updatedText;
            console.log(`📊 Updated counter: ${this.scenarioNumber}/${this.totalScenarios}`);
        }
        
        // Reset state
        this.selectedOption = null;
        this.clearSelections();
        const submitBtn = document.getElementById('submit-btn');
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.textContent = this.t('submit');
        }
        
        const feedback = document.getElementById('feedback');
        if (feedback) feedback.classList.add('hidden');
        
        const continueBtn = document.getElementById('continue-btn');
        if (continueBtn) continueBtn.classList.add('hidden');
    }

    selectOption(optionElement) {
        this.clearSelections();
        optionElement.classList.add('border-green-500', 'bg-green-50');
        this.selectedOption = optionElement.dataset.option;
        
        const submitBtn = document.getElementById('submit-btn');
        if (submitBtn) {
            submitBtn.disabled = false;
        }
    }

    clearSelections() {
        document.querySelectorAll('.option').forEach(option => {
            option.classList.remove('border-green-500', 'bg-green-50');
        });
    }

    async submitAnswer() {
        if (!this.selectedOption) {
            alert(this.t('selectOption'));
            return;
        }

        try {
            const response = await fetch(`${this.apiUrl}/rally/session/${this.sessionId}/submit`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    selected_option: this.selectedOption
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const result = await response.json();
            this.handleAnswerResult(result);

        } catch (error) {
            console.error('❌ Error submitting answer:', error);
            this.showError(this.t('submitError') + error.message);
        }
    }

    handleAnswerResult(result) {
        const feedback = document.getElementById('feedback');
        const continueBtn = document.getElementById('continue-btn');
        const submitBtn = document.getElementById('submit-btn');
        
        if (feedback && continueBtn && submitBtn) {
            submitBtn.disabled = true;
            
            feedback.innerHTML = `
                <div class="p-4 rounded-lg ${result.is_correct ? 'bg-green-100 border-green-400' : 'bg-red-100 border-red-400'} border">
                    <h4 class="font-bold ${result.is_correct ? 'text-green-800' : 'text-red-800'}">${result.is_correct ? this.t('correct') : this.t('incorrect')}</h4>
                    <p class="text-gray-700 mt-2">${this.t('correctAnswer')} ${result.correct_answer}</p>
                    <p class="text-gray-600 mt-1">${result.explanation}</p>
                </div>
            `;
            
            feedback.classList.remove('hidden');
            
            this.score = result.score;
            const scoreEl = document.getElementById('score');
            if (scoreEl) scoreEl.textContent = this.score;
            
            if (result.game_completed) {
                continueBtn.textContent = this.t('viewResults');
                // Don't assign onclick, let the existing event listener handle it
                continueBtn.setAttribute('data-action', 'show-results');
            } else {
                this.currentScenario = result.next_scenario;
                continueBtn.textContent = this.t('continue');
                // Don't assign onclick, let the existing event listener handle it  
                continueBtn.setAttribute('data-action', 'next-question');
            }
            
            continueBtn.classList.remove('hidden');
        }
    }

    nextQuestion() {
        console.log(`🔄 nextQuestion() called - current scenarioNumber: ${this.scenarioNumber}`);
        this.scenarioNumber++;
        console.log(`🔄 scenarioNumber incremented to: ${this.scenarioNumber}`);
        this.loadScenario(this.currentScenario);
    }

    showResults() {
        this.showResultScreen();
        
        // Force translation of result screen elements
        this.translateResultScreen();
        
        const finalScore = document.getElementById('final-score');
        if (finalScore) finalScore.textContent = this.score;
        
        const percentage = (this.score / 50) * 100;
        let message = '';
        
        if (percentage >= 90) {
            message = this.t('excellent');
        } else if (percentage >= 75) {
            message = this.t('veryGood');
        } else if (percentage >= 60) {
            message = this.t('good');
        } else {
            message = this.t('needsPractice');
        }
        
        const resultMessage = document.getElementById('result-message');
        if (resultMessage) resultMessage.textContent = message;
        
        const scoreBar = document.getElementById('score-bar');
        if (scoreBar) {
            setTimeout(() => {
                scoreBar.style.width = `${percentage}%`;
            }, 500);
        }
    }

    translateResultScreen() {
        console.log(`🎯 Translating result screen to: ${this.language}`);
        
        const elements = [
            { id: 'game-completed-title', text: this.t('gameCompleted') },
            { id: 'score-label', text: this.t('score') },
            { id: 'knowledge-title', text: this.t('knowledge') },
            { id: 'knowledge-desc', text: this.t('knowledgeDesc') },
            { id: 'application-title', text: this.t('application') },
            { id: 'application-desc', text: this.t('applicationDesc') },
            { id: 'speed-title', text: this.t('speed') },
            { id: 'speed-desc', text: this.t('speedDesc') },
            { id: 'play-again-text', text: this.t('playAgain') }
        ];
        
        elements.forEach(({ id, text }) => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = text;
                console.log(`✅ Translated ${id}`);
            }
        });
    }

    resetGame() {
        this.sessionId = null;
        this.currentScenario = null;
        this.score = 0;
        this.scenarioNumber = 1;
        this.totalScenarios = 5; // Reset to default
        this.selectedOption = null;
        
        const scoreEl = document.getElementById('score');
        if (scoreEl) scoreEl.textContent = '0';
        
        this.showIntroScreen();
        
        // Clear form
        const playerInput = document.getElementById('player-name');
        if (playerInput) playerInput.value = '';
        
        const categoryFilter = document.getElementById('category-filter');
        if (categoryFilter) categoryFilter.value = '';
    }

    showError(message) {
        alert(message);
    }
}

// Initialize game when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    try {
        console.log('🚀 DOM loaded, initializing RequirementRally...');
        window.game = new RequirementRallyGame();
        console.log('✅ RequirementRally initialized successfully');
    } catch (error) {
        console.error('❌ Error initializing RequirementRally:', error);
    }
});