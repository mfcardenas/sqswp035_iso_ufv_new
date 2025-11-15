/**
 * UsabilityUniverse Game Logic - Based on RequirementRally pattern
 * Independent game for usability principle identification
 * Connects to main server on port 8001
 */

// Translations for internationalization
const translations = {
    es: {
        title: "UsabilityUniverse",
        subtitle: "Aprende a identificar principios de usabilidad",
        welcome: "¡Bienvenido a UsabilityUniverse!",
        description: "Identifica principios de usabilidad en escenarios reales de interfaces",
        gameDescription: "En este juego analizarás diferentes escenarios de interfaces y determinarás qué principio de usabilidad es más relevante.",
        usabilityPrinciples: "Principios de Usabilidad",
        learnability: "Facilidad de Aprendizaje",
        efficiency: "Eficiencia",
        memorability: "Memorabilidad",
        errorPrevention: "Prevención de Errores",
        userSatisfaction: "Satisfacción del Usuario",
        playerName: "Nombre del Jugador",
        category: "Categoría (Opcional)",
        difficulty: "Dificultad (Opcional)",
        allCategories: "Todas las categorías",
        allDifficulties: "Todas las dificultades",
        easy: "Fácil",
        medium: "Medio",
        hard: "Difícil",
        startGame: "Iniciar Juego",
        score: "Puntuación",
        scenario: "Escenario",
        submitAnswer: "Enviar Respuesta",
        continue: "Continuar",
        playAgain: "Jugar de Nuevo",
        correct: "¡Correcto!",
        incorrect: "Incorrecto",
        loading: "Cargando...",
        submitError: "Error al enviar respuesta: ",
        connectionError: "Error de conexión al servidor",
        finalScore: "Puntuación Final",
        gameComplete: "¡Juego Completado!",
        congratulations: "¡Felicidades!",
        results: "Resultados"
    },
    en: {
        title: "UsabilityUniverse",
        subtitle: "Learn to identify usability principles",
        welcome: "Welcome to UsabilityUniverse!",
        description: "Identify usability principles in real interface scenarios",
        gameDescription: "In this game you will analyze different interface scenarios and determine which usability principle is most relevant.",
        usabilityPrinciples: "Usability Principles",
        learnability: "Learnability",
        efficiency: "Efficiency", 
        memorability: "Memorability",
        errorPrevention: "Error Prevention",
        userSatisfaction: "User Satisfaction",
        playerName: "Player Name",
        category: "Category (Optional)",
        difficulty: "Difficulty (Optional)",
        allCategories: "All categories",
        allDifficulties: "All difficulties",
        easy: "Easy",
        medium: "Medium",
        hard: "Hard",
        startGame: "Start Game",
        score: "Score",
        scenario: "Scenario",
        submitAnswer: "Submit Answer",
        continue: "Continue",
        playAgain: "Play Again",
        correct: "Correct!",
        incorrect: "Incorrect",
        loading: "Loading...",
        submitError: "Error submitting answer: ",
        connectionError: "Server connection error",
        finalScore: "Final Score",
        gameComplete: "Game Complete!",
        congratulations: "Congratulations!",
        results: "Results"
    }
};

// Configuration
const API_BASE_URL = window.CONFIG ? window.CONFIG.API.BASE_URL : '';

// Game state
let gameState = {
    score: 0,
    currentScenario: 0,
    totalScenarios: 5,
    scenarios: [],
    isGameActive: false
};

// UI Elements
const introScreen = document.getElementById('intro-screen');
const gameScreen = document.getElementById('game-screen');
const resultsScreen = document.getElementById('results-screen');
const playerInfo = document.getElementById('player-info');

const titleElement = document.querySelector('[data-translate="title"]');
const subtitleElement = document.querySelector('[data-translate="subtitle"]');
const welcomeElement = document.querySelector('[data-translate="welcome"]');
const descriptionElement = document.querySelector('[data-translate="description"]');
const gameDescriptionElement = document.querySelector('[data-translate="gameDescription"]');
const usabilityPrinciplesElement = document.querySelector('[data-translate="usabilityPrinciples"]');

const playerNameInput = document.getElementById('player-name');
const categorySelect = document.getElementById('category-select');
const difficultySelect = document.getElementById('difficulty-select');
const startGameBtn = document.getElementById('start-game');

const scenarioNumber = document.getElementById('scenario-number');
const scenarioText = document.getElementById('scenario-text');
const scoreDisplay = document.getElementById('score');
const displayPlayerName = document.getElementById('display-player-name');
const displayScore = document.getElementById('display-score');

const optionButtons = document.querySelectorAll('.option-button');
const submitAnswerBtn = document.getElementById('submit-answer');
const continueGameBtn = document.getElementById('continue-game');
const feedbackSection = document.getElementById('feedback');
const feedbackText = document.getElementById('feedback-content');

const finalScoreDisplay = document.getElementById('final-score');
const playAgainBtn = document.getElementById('play-again');

// Language and game state
let currentLanguage = 'en';
let currentSession = null;
let selectedOption = null;

// Initialize game
document.addEventListener('DOMContentLoaded', function() {
    console.log('UsabilityUniverse game loaded');
    
    // Set up event listeners
    setupEventListeners();
    
    // Apply initial translations
    updateLanguage(currentLanguage);
    
    // Initialize game state
    resetGame();
});

function setupEventListeners() {
    // Language selection 
    const langEn = document.getElementById('lang-en');
    const langEs = document.getElementById('lang-es');
    
    if (langEn) langEn.addEventListener('click', () => updateLanguage('en'));
    if (langEs) langEs.addEventListener('click', () => updateLanguage('es'));
    
    // Game controls
    if (startGameBtn) startGameBtn.addEventListener('click', startGame);
    if (submitAnswerBtn) submitAnswerBtn.addEventListener('click', submitAnswer);
    if (playAgainBtn) playAgainBtn.addEventListener('click', resetGame);
    
    // Option buttons
    if (optionButtons) {
        optionButtons.forEach(button => {
            button.addEventListener('click', () => {
                const option = button.getAttribute('data-option');
                selectOption(option);
            });
        });
    }
}

function updateLanguage(language) {
    currentLanguage = language;
    
    // Update language buttons
    document.querySelectorAll('.language-selector').forEach(btn => {
        btn.classList.remove('bg-indigo-100', 'border-indigo-300');
        btn.classList.add('bg-white', 'border-gray-300');
    });
    
    const activeBtn = document.getElementById(`lang-${language}`);
    if (activeBtn) {
        activeBtn.classList.remove('bg-white', 'border-gray-300');
        activeBtn.classList.add('bg-indigo-100', 'border-indigo-300');
    }
    
    // Update text content
    const t = translations[language];
    
    titleElement.textContent = t.title;
    subtitleElement.textContent = t.subtitle;
    welcomeElement.textContent = t.welcome;
    descriptionElement.textContent = t.description;
    gameDescriptionElement.textContent = t.gameDescription;
    usabilityPrinciplesElement.textContent = t.usabilityPrinciples;
    
    // Update form labels
    document.querySelector('label[for="player-name"]').textContent = t.playerName;
    document.querySelector('label[for="category"]').textContent = t.category;
    document.querySelector('label[for="difficulty"]').textContent = t.difficulty;
    
    // Update option labels
    document.querySelector('[data-option="Learnability"]').textContent = t.learnability;
    document.querySelector('[data-option="Efficiency"]').textContent = t.efficiency;
    document.querySelector('[data-option="Memorability"]').textContent = t.memorability;
    document.querySelector('[data-option="Error_Prevention"]').textContent = t.errorPrevention;
    document.querySelector('[data-option="User_Satisfaction"]').textContent = t.userSatisfaction;
    
    // Update buttons
    startGameBtn.textContent = t.startGame;
    submitAnswerBtn.textContent = t.submitAnswer;
    playAgainBtn.textContent = t.playAgain;
    
    // Update select options
    categorySelect.innerHTML = `
        <option value="">${t.allCategories}</option>
        <option value="Learnability">${t.learnability}</option>
        <option value="Efficiency">${t.efficiency}</option>
        <option value="Memorability">${t.memorability}</option>
        <option value="Error_Prevention">${t.errorPrevention}</option>
        <option value="User_Satisfaction">${t.userSatisfaction}</option>
    `;
    
    difficultySelect.innerHTML = `
        <option value="">${t.allDifficulties}</option>
        <option value="easy">${t.easy}</option>
        <option value="medium">${t.medium}</option>
        <option value="hard">${t.hard}</option>
    `;
}

async function startGame() {
    try {
        console.log('Starting UsabilityUniverse game');
        
        // Get game settings
        const playerName = playerNameInput.value.trim() || 'Player1';
        const category = categorySelect.value || null;
        const difficulty = difficultySelect.value || null;
        
        console.log(`Player: ${playerName}, Category: ${category}, Difficulty: ${difficulty}, Language: ${currentLanguage}`);
        
        // Show loading
        scenarioText.textContent = translations[currentLanguage].loading;
        
        // Create session
        const response = await fetch(`${API_BASE_URL}/universe/session`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: playerName,
                category: category,
                difficulty: difficulty,
                language: currentLanguage
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const sessionData = await response.json();
        console.log('Session created:', sessionData);
        
        currentSession = sessionData;
        gameState.score = sessionData.score;
        gameState.currentScenario = 0;
        gameState.isGameActive = true;
        
        // Update player info
        displayPlayerName.textContent = playerName;
        displayScore.textContent = gameState.score;
        playerInfo.classList.remove('hidden');
        
        // Switch to game screen
        introScreen.classList.add('hidden');
        gameScreen.classList.remove('hidden');
        
        // Load first scenario
        loadScenario(sessionData.current_scenario);
        
    } catch (error) {
        console.error('Error starting game:', error);
        alert(translations[currentLanguage].connectionError + ': ' + error.message);
    }
}

function loadScenario(scenario) {
    console.log('Loading scenario:', scenario);
    
    // Update scenario number
    scenarioNumber.textContent = gameState.currentScenario + 1;
    
    // Update scenario content
    scenarioText.textContent = scenario.content;
    
    // Reset options
    selectedOption = null;
    document.querySelectorAll('.option-button').forEach(button => {
        button.classList.remove('border-violet-500', 'bg-violet-50');
        button.classList.add('border-gray-200');
    });
    
    // Enable submit button when option is selected
    submitAnswerBtn.disabled = true;
    submitAnswerBtn.classList.add('disabled:bg-gray-400', 'disabled:cursor-not-allowed');
    
    // Hide feedback
    feedbackSection.classList.add('hidden');
    
    // Update score display
    scoreDisplay.textContent = gameState.score;
    displayScore.textContent = gameState.score;
}

function selectOption(option) {
    console.log('Selected option:', option);
    selectedOption = option;
    
    // Update UI
    document.querySelectorAll('.option-button').forEach(button => {
        button.classList.remove('border-violet-500', 'bg-violet-50');
        button.classList.add('border-gray-200');
    });
    
    const selectedButton = document.querySelector(`[data-option="${option}"]`);
    if (selectedButton) {
        selectedButton.classList.remove('border-gray-200');
        selectedButton.classList.add('border-violet-500', 'bg-violet-50');
    }
    
    // Enable submit button
    submitAnswerBtn.disabled = false;
    submitAnswerBtn.classList.remove('disabled:bg-gray-400', 'disabled:cursor-not-allowed');
}

async function submitAnswer() {
    if (!selectedOption || !currentSession) {
        return;
    }
    
    try {
        console.log('Submitting answer:', selectedOption);
        
        const response = await fetch(`${API_BASE_URL}/universe/session/${currentSession.id}/submit`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                selected_option: selectedOption
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const result = await response.json();
        console.log('Answer result:', result);
        
        // Update game state
        gameState.score = result.score;
        scoreDisplay.textContent = gameState.score;
        displayScore.textContent = gameState.score;
        
        // Update current session with next scenario
        if (result.next_scenario) {
            currentSession.current_scenario = result.next_scenario;
            console.log('Updated to next scenario:', result.next_scenario.id);
        } else {
            currentSession.current_scenario = null;
            console.log('No more scenarios - game completed');
        }
        
        // Show feedback
        showFeedback(result);
        
        // Disable submit button
        submitAnswerBtn.disabled = true;
        
        // Check if game completed
        if (result.game_completed) {
            continueGameBtn.textContent = translations[currentLanguage].playAgain;
            continueGameBtn.onclick = showResults;
        } else {
            continueGameBtn.textContent = translations[currentLanguage].continue;
            continueGameBtn.onclick = nextScenario;
        }
        
    } catch (error) {
        console.error('Error submitting answer:', error);
        alert(translations[currentLanguage].submitError + error.message);
    }
}

function showFeedback(result) {
    const isCorrect = result.is_correct;
    const correctAnswer = result.correct_answer;
    const explanation = result.explanation;
    
    // Create feedback content
    const feedbackHtml = `
        <div class="${isCorrect ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'} border rounded-lg p-4">
            <div class="flex items-center mb-2">
                <div class="${isCorrect ? 'bg-green-500' : 'bg-red-500'} text-white rounded-full w-6 h-6 flex items-center justify-center mr-2">
                    ${isCorrect ? '✓' : '✗'}
                </div>
                <span class="font-bold ${isCorrect ? 'text-green-800' : 'text-red-800'}">
                    ${isCorrect ? translations[currentLanguage].correct : translations[currentLanguage].incorrect}
                </span>
            </div>
            ${!isCorrect ? `<p class="text-sm text-gray-700 mb-2">Correct answer: <strong>${translations[currentLanguage][correctAnswer.toLowerCase()]}</strong></p>` : ''}
            <p class="text-sm text-gray-700">${explanation}</p>
        </div>
    `;
    
    feedbackText.innerHTML = feedbackHtml;
    feedbackSection.classList.remove('hidden');
}

function nextScenario() {
    gameState.currentScenario++;
    
    // Get next scenario from session or complete game
    if (currentSession && currentSession.current_scenario) {
        loadScenario(currentSession.current_scenario);
    } else {
        showResults();
    }
}

function showResults() {
    console.log('Showing results');
    
    // Update final score
    finalScoreDisplay.textContent = gameState.score;
    
    // Switch to results screen
    introScreen.classList.add('hidden');
    gameScreen.classList.add('hidden');
    resultsScreen.classList.remove('hidden');
    
    gameState.isGameActive = false;
}

function resetGame() {
    console.log('Resetting game');
    
    // Reset game state
    gameState = {
        score: 0,
        currentScenario: 0,
        totalScenarios: 5,
        scenarios: [],
        isGameActive: false
    };
    
    currentSession = null;
    selectedOption = null;
    
    // Reset UI
    scoreDisplay.textContent = '0';
    displayScore.textContent = '0';
    scenarioNumber.textContent = '1';
    scenarioText.textContent = '';
    feedbackSection.classList.add('hidden');
    playerInfo.classList.add('hidden');
    
    // Reset form
    playerNameInput.value = 'Player1';
    categorySelect.value = '';
    difficultySelect.value = '';
    
    // Switch to intro screen
    introScreen.classList.remove('hidden');
    gameScreen.classList.add('hidden');
    resultsScreen.classList.add('hidden');
}

// Debug function
function debugGameState() {
    return {
        currentSession,
        gameState,
        selectedOption,
        currentLanguage
    };
}

console.log('UsabilityUniverse module loaded successfully');