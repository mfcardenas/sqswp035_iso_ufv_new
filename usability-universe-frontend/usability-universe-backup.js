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
        welco        // Update game state
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
        showFeedback(result);ienvenido a UsabilityUniverse!",
        description: "Identifica principios de usabilidad en escenarios reales de interfaces",
        gameDescription: "En este juego analizarás diferentes escenarios de interfaces y determinarás qué principio de usabilidad es más relevante.",
        usabilityPrinciples: "Principios de Usabilidad",
        learnability: "Facilidad de Aprendizaje",
        efficiency: "Eficiencia",
        memorability: "Memorabilidad",
        errorPrevention: "Prevención de Errores",
        userSatisfaction: "Satisfacción del Usuario",
        learnabilityDesc: "Qué tan fácil es para los usuarios aprender a usar la interfaz",
        efficiencyDesc: "Qué tan rápido pueden los usuarios realizar tareas una vez que aprenden",
        memorabilityDesc: "Qué tan fácil es para los usuarios recordar cómo usar la interfaz",
        errorPreventionDesc: "Qué tan bien la interfaz previene errores del usuario",
        userSatisfactionDesc: "Qué tan agradable y satisfactoria es la interfaz de usar",
        step1: "Lee cada escenario de interfaz cuidadosamente",
        step2: "Identifica qué principio de usabilidad es más relevante",
        step3: "Envía tu respuesta y aprende de la explicación",
        step4: "Gana puntos por respuestas correctas",
        howToPlay: "Cómo Jugar",
        gameSettings: "Configuración del Juego",
        playerName: "Nombre del Jugador",
        player: "Jugador",
        playerNamePlaceholder: "Tu nombre",
        category: "Categoría",
        difficulty: "Dificultad",
        allPrinciples: "Todos los Principios",
        onlyLearnability: "Solo Facilidad de Aprendizaje",
        onlyEfficiency: "Solo Eficiencia",
        onlyMemorability: "Solo Memorabilidad",
        onlyErrorPrevention: "Solo Prevención de Errores",
        onlyUserSatisfaction: "Solo Satisfacción del Usuario",
        allLevels: "Todos los Niveles",
        easy: "Fácil",
        medium: "Medio",
        hard: "Difícil",
        startGame: "Comenzar Juego",
        scenario: "Escenario",
        points: "Puntos",
        questionType: "¿Qué principio de usabilidad es más relevante?",
        loading: "Cargando escenario...",
        submit: "Enviar Respuesta",
        continue: "Continuar",
        correct: "¡Correcto!",
        incorrect: "Incorrecto",
        correctAnswer: "Respuesta correcta:",
        finalScore: "Puntuación Final",
        playAgain: "Jugar de Nuevo",
        gameCompleted: "¡Juego Completado!",
        score: "Puntuación",
        selectOption: "Por favor selecciona una opción",
        connectionError: "No se puede conectar al servidor. Asegúrate de que el servidor principal esté ejecutándose en 127.0.0.1:8001.",
        gameStartError: "Error al iniciar el juego: ",
        submitError: "Error al enviar respuesta: ",
        backToGames: "Volver a Juegos"
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
        learnabilityDesc: "How easily users can learn to use the interface",
        efficiencyDesc: "How quickly users can perform tasks once they learn",
        memorabilityDesc: "How easily users can remember how to use the interface",
        errorPreventionDesc: "How well the interface prevents user errors",
        userSatisfactionDesc: "How pleasant and satisfying the interface is to use",
        step1: "Read each interface scenario carefully",
        step2: "Identify which usability principle is most relevant",
        step3: "Submit your answer and learn from the explanation",
        step4: "Gain points for correct answers",
        howToPlay: "How to Play",
        gameSettings: "Game Settings",
        playerName: "Player Name",
        player: "Player",
        playerNamePlaceholder: "Your name",
        category: "Category",
        difficulty: "Difficulty",
        allPrinciples: "All Principles",
        onlyLearnability: "Only Learnability",
        onlyEfficiency: "Only Efficiency",
        onlyMemorability: "Only Memorability",
        onlyErrorPrevention: "Only Error Prevention",
        onlyUserSatisfaction: "Only User Satisfaction",
        allLevels: "All Levels",
        easy: "Easy",
        medium: "Medium",
        hard: "Hard",
        startGame: "Start Game",
        scenario: "Scenario",
        points: "Points",
        questionType: "Which usability principle is most relevant?",
        loading: "Loading scenario...",
        submit: "Submit Answer",
        continue: "Continue",
        correct: "Correct!",
        incorrect: "Incorrect",
        correctAnswer: "Correct answer:",
        finalScore: "Final Score",
        playAgain: "Play Again",
        gameCompleted: "Game Completed!",
        score: "Score",
        selectOption: "Please select an option",
        connectionError: "Cannot connect to server. Make sure the main server is running on 127.0.0.1:8001.",
        gameStartError: "Error starting game: ",
        submitError: "Error submitting answer: ",
        backToGames: "Back to Games"
    }
};

// Game configuration
const API_BASE_URL = 'http://127.0.0.1:8001';
let currentLanguage = 'en'; // Default to English
let currentSession = null;
let selectedOption = null;

// Game state
let gameState = {
    score: 0,
    currentScenario: 0,
    totalScenarios: 5,
    scenarios: [],
    isGameActive: false
};

// DOM Elements
const introScreen = document.getElementById('intro-screen');
const gameScreen = document.getElementById('game-screen');
const resultsScreen = document.getElementById('results-screen');
const startGameBtn = document.getElementById('start-game');
const playerNameInput = document.getElementById('player-name');
const categorySelect = document.getElementById('category-select');
const difficultySelect = document.getElementById('difficulty-select');
const submitAnswerBtn = document.getElementById('submit-answer');
const continueGameBtn = document.getElementById('continue-game');
const playAgainBtn = document.getElementById('play-again');
const scenarioNumber = document.getElementById('scenario-number');
const scenarioText = document.getElementById('scenario-text');
const scoreDisplay = document.getElementById('score');
const finalScoreDisplay = document.getElementById('final-score');
const feedbackSection = document.getElementById('feedback');
const feedbackContent = document.getElementById('feedback-content');
const playerInfo = document.getElementById('player-info');
const displayPlayerName = document.getElementById('display-player-name');
const displayScore = document.getElementById('display-score');

// Initialize the game
document.addEventListener('DOMContentLoaded', function() {
    console.log('UsabilityUniverse game loaded');
    
    // Set default language to English
    currentLanguage = 'en';
    updateLanguageButtons();
    translatePage();
    
    // Add event listeners
    setupEventListeners();
    
    // Set default player name
    playerNameInput.value = 'Player1';
});

function setupEventListeners() {
    // Language switchers
    document.getElementById('lang-en').addEventListener('click', () => switchLanguage('en'));
    document.getElementById('lang-es').addEventListener('click', () => switchLanguage('es'));
    
    // Game buttons
    startGameBtn.addEventListener('click', startGame);
    submitAnswerBtn.addEventListener('click', submitAnswer);
    continueGameBtn.addEventListener('click', nextScenario);
    playAgainBtn.addEventListener('click', resetGame);
    
    // Option buttons
    document.querySelectorAll('.option-button').forEach(button => {
        button.addEventListener('click', function() {
            selectOption(this.dataset.option);
        });
    });
    
    // Player name input
    playerNameInput.addEventListener('input', function() {
        displayPlayerName.textContent = this.value || 'Player1';
    });
}

function switchLanguage(lang) {
    console.log(`Switching to language: ${lang}`);
    currentLanguage = lang;
    updateLanguageButtons();
    translatePage();
}

function updateLanguageButtons() {
    const enBtn = document.getElementById('lang-en');
    const esBtn = document.getElementById('lang-es');
    
    if (currentLanguage === 'en') {
        enBtn.classList.add('bg-opacity-30');
        enBtn.classList.remove('bg-opacity-20');
        esBtn.classList.add('bg-opacity-20');
        esBtn.classList.remove('bg-opacity-30');
    } else {
        esBtn.classList.add('bg-opacity-30');
        esBtn.classList.remove('bg-opacity-20');
        enBtn.classList.add('bg-opacity-20');
        enBtn.classList.remove('bg-opacity-30');
    }
}

function translatePage() {
    const elements = document.querySelectorAll('[data-translate]');
    elements.forEach(element => {
        const key = element.getAttribute('data-translate');
        if (translations[currentLanguage] && translations[currentLanguage][key]) {
            element.textContent = translations[currentLanguage][key];
        }
    });
    
    // Translate placeholders
    const placeholderElements = document.querySelectorAll('[data-translate-placeholder]');
    placeholderElements.forEach(element => {
        const key = element.getAttribute('data-translate-placeholder');
        if (translations[currentLanguage] && translations[currentLanguage][key]) {
            element.placeholder = translations[currentLanguage][key];
        }
    });
}

async function startGame() {
    try {
        console.log('Starting UsabilityUniverse game...');
        
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
        
        // Load first scenario
        loadScenario(sessionData.current_scenario);
        
        // Switch to game screen
        introScreen.classList.add('hidden');
        gameScreen.classList.remove('hidden');
        resultsScreen.classList.add('hidden');
        
    } catch (error) {
        console.error('Error starting game:', error);
        alert(translations[currentLanguage].gameStartError + error.message);
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
    
    // Visual feedback
    document.querySelectorAll('.option-button').forEach(button => {
        if (button.dataset.option === option) {
            button.classList.remove('border-gray-200');
            button.classList.add('border-violet-500', 'bg-violet-50');
        } else {
            button.classList.remove('border-violet-500', 'bg-violet-50');
            button.classList.add('border-gray-200');
        }
    });
    
    // Enable submit button
    submitAnswerBtn.disabled = false;
    submitAnswerBtn.classList.remove('disabled:bg-gray-400', 'disabled:cursor-not-allowed');
}

async function submitAnswer() {
    if (!selectedOption) {
        alert(translations[currentLanguage].selectOption);
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
        
        // Update score
        gameState.score = result.score;
        scoreDisplay.textContent = gameState.score;
        displayScore.textContent = gameState.score;
        
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
            ${!isCorrect ? `<p class="text-gray-700 mb-2"><strong>${translations[currentLanguage].correctAnswer}</strong> ${correctAnswer}</p>` : ''}
            <p class="text-gray-700">${explanation}</p>
        </div>
    `;
    
    feedbackContent.innerHTML = feedbackHtml;
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

// Handle connection errors gracefully
window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
    if (event.reason.message && event.reason.message.includes('fetch')) {
        alert(translations[currentLanguage].connectionError);
    }
});

// Export for debugging
window.UsabilityUniverse = {
    gameState,
    currentSession,
    currentLanguage,
    translations,
    startGame,
    submitAnswer,
    switchLanguage
};

console.log('UsabilityUniverse game script loaded successfully');