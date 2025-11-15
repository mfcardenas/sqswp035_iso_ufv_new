// QualityQuest game logic
document.addEventListener('DOMContentLoaded', function() {
  // API Configuration - use centralized config
  const API_BASE_URL = window.CONFIG ? window.CONFIG.API.BASE_URL : '';
  
  // Current language - declare early to avoid reference errors
  let currentLanguage = localStorage.getItem('iso-games-language') || 'en';
  
  // Translation dictionary for server responses
  const serverTranslations = {
    en: {
      'Aptitud Funcional': 'Functional Suitability',
      'Eficiencia de Rendimiento': 'Performance Efficiency', 
      'Compatibilidad': 'Compatibility',
      'Usabilidad': 'Usability',
      'Fiabilidad': 'Reliability',
      'Seguridad': 'Security',
      'Mantenibilidad': 'Maintainability',
      'Portabilidad': 'Portability'
    },
    es: {
      'Aptitud Funcional': 'Aptitud Funcional',
      'Eficiencia de Rendimiento': 'Eficiencia de Rendimiento',
      'Compatibilidad': 'Compatibilidad', 
      'Usabilidad': 'Usabilidad',
      'Fiabilidad': 'Fiabilidad',
      'Seguridad': 'Seguridad',
      'Mantenibilidad': 'Mantenibilidad',
      'Portabilidad': 'Portabilidad'
    }
  };
  
  // Function to translate server options
  function translateOptions(options) {
    const translations = serverTranslations[currentLanguage] || serverTranslations['en'];
    const translatedOptions = {};
    
    for (const [key, value] of Object.entries(options)) {
      translatedOptions[key] = translations[value] || value;
    }
    
    return translatedOptions;
  }
  
  // Game elements
  const introScreen = document.getElementById('intro-screen');
  const gameScreen = document.getElementById('game-screen');
  const resultScreen = document.getElementById('result-screen');
  const startGameBtn = document.getElementById('start-game-btn');
  const submitBtn = document.getElementById('submit-btn');
  const continueBtn = document.getElementById('continue-btn');
  const playAgainBtn = document.getElementById('play-again-btn');
  const scenarioElement = document.getElementById('scenario');
  const scenarioNumber = document.getElementById('scenario-number');
  const scoreElement = document.getElementById('score');
  const finalScoreElement = document.getElementById('final-score');
  const resultMessage = document.getElementById('result-message');
  const feedbackElement = document.getElementById('feedback');
  const optionsContainer = document.getElementById('options');
  const badgesContainer = document.getElementById('badges-container');
  
  // Game state
  let gameState = {
    currentScenario: 0,
    totalScenarios: 5,
    score: 0,
    selectedOption: null,
    scenarios: [],
    sessionId: null,
    gameId: 'quality_quest',
    badges: []
  };
  
  // NO hardcoded scenarios - everything comes from the database via API
  
  // Start game button click handler
  if (startGameBtn) {
    console.log("Adding click event to start game button");
    startGameBtn.addEventListener('click', function(event) {
      event.preventDefault();
      startGame();
    });
  } else {
    console.error("Start game button not found!");
  }
  
  // Submit answer button click handler
  submitBtn.addEventListener('click', submitAnswer);
  
  // Continue button click handler
  if (continueBtn) {
    continueBtn.addEventListener('click', nextScenario);
  }
  
  // Play again button click handler
  playAgainBtn.addEventListener('click', resetGame);
  
  // Option selection handler
  optionsContainer.addEventListener('click', function(event) {
    const option = event.target.closest('.option');
    if (!option) return;
    
    // Clear previous selection
    document.querySelectorAll('.option').forEach(opt => {
      opt.classList.remove('selected');
    });
    
    // Set new selection
    option.classList.add('selected');
    gameState.selectedOption = option.dataset.option;
    
    // Enable submit button
    submitBtn.disabled = false;
  });
  
  // Function to start the game
  async function startGame() {
    console.log("Starting game...");
    
    // Show loading indicator
    if (scenarioElement) {
      scenarioElement.innerHTML = `
        <div class="text-center">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mb-3"></div>
          <p class="text-lg text-gray-600">🤖 AI is generating your scenario...</p>
        </div>
      `;
    }
    
    // Show game screen
    introScreen.classList.add('hidden');
    gameScreen.classList.remove('hidden');
    resultScreen.classList.add('hidden');
    
    // Block options until scenario is loaded
    document.querySelectorAll('.option').forEach(opt => {
      opt.style.pointerEvents = 'none';
      opt.style.opacity = '0.5';
      opt.style.cursor = 'not-allowed';
      opt.classList.add('disabled');
    });
    
    // Reset game state completely
    gameState = {
      currentScenario: 0,
      totalScenarios: 5,
      score: 0,
      selectedOption: null,
      scenarios: [],
      sessionId: null,
      gameId: 'quality_quest',
      badges: [],
      currentScenarioData: null,
      currentAnswerSubmitted: false,
      allScenariosData: null,
      nextScenarioData: null
    };
    
    // Update UI
    updateScoreDisplay();
    
    // Force creation of a new session every time to ensure fresh scenarios
    try {
      console.log('🚀 Creating new session to ensure fresh scenarios');
      
      // Always create a new session with fresh scenarios
      // Add timestamp to prevent any caching
      const timestamp = Date.now();
      const response = await fetch(`${API_BASE_URL}/api/create-session?t=${timestamp}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Cache-Control': 'no-cache, no-store, must-revalidate',
          'Pragma': 'no-cache'
        },
        body: JSON.stringify({
          name: `Player_${timestamp}`, // Different name each time
          quality_attribute: 'Todos',
          language: currentLanguage
        })
      });
      
      console.log(`🕐 Created session request at ${new Date(timestamp).toLocaleTimeString()}`);
      
      console.log('📡 API Response status:', response.status);
      console.log('📡 API Response ok:', response.ok);
      
      if (response.ok) {
        const data = await response.json();
        console.log('✅ API SUCCESS! Received data:', data);
        gameState.sessionId = data.id;
        
        // Store all scenarios data to prevent changes during gameplay
        if (data.all_scenarios) {
          gameState.allScenariosData = data.all_scenarios;
          console.log('📦 Stored all scenarios data:', gameState.allScenariosData.length);
        }
        
        loadScenario(data.current_scenario);
        return; // Exit if API call succeeds
      } else {
        console.log('❌ API Response not OK. Status:', response.status);
        const errorText = await response.text();
        console.log('❌ Error response:', errorText);
      }
      
    } catch (error) {
      console.error('💥 Error starting game:', error);
    }
    
    // If we reach here without success, use fallback scenarios
    if (!gameState.sessionId) {
      console.log('⚠️ LLM not available, using fallback scenarios');
      
      // Create fallback scenarios
      const fallbackScenarios = [
        {
          content: "A banking application allows users to view account balances and transaction history. The system needs to ensure that unauthorized access is prevented and user data remains confidential.",
          options: {
            A: "Performance",
            B: "Security", 
            C: "Usability",
            D: "Reliability"
          },
          correct_answer: "B",
          feedback: "Security is the primary concern when protecting user data and preventing unauthorized access to financial information."
        },
        {
          content: "A mobile messaging app frequently crashes when users try to send photos or videos. Users report that the app becomes unresponsive and they lose their messages.",
          options: {
            A: "Reliability",
            B: "Performance",
            C: "Usability", 
            D: "Maintainability"
          },
          correct_answer: "A",
          feedback: "Reliability is about the system's ability to perform consistently without crashing or losing data."
        },
        {
          content: "An e-commerce website takes 15 seconds to load product pages. Customers are abandoning their shopping carts because the site is too slow.",
          options: {
            A: "Security",
            B: "Usability",
            C: "Performance",
            D: "Compatibility"
          },
          correct_answer: "C", 
          feedback: "Performance issues directly impact how quickly the system responds to user requests."
        },
        {
          content: "A software application has a complex interface with many buttons and menus. New users find it difficult to complete basic tasks without extensive training.",
          options: {
            A: "Performance",
            B: "Security",
            C: "Usability",
            D: "Reliability"
          },
          correct_answer: "C",
          feedback: "Usability focuses on how easily and effectively users can interact with the system."
        },
        {
          content: "A legacy system needs to be updated regularly, but making changes takes weeks and often introduces new bugs. The development team struggles to add new features.",
          options: {
            A: "Maintainability",
            B: "Performance", 
            C: "Security",
            D: "Compatibility"
          },
          correct_answer: "A",
          feedback: "Maintainability is about how easily software can be modified, updated, and enhanced."
        }
      ];
      
      // Set up fallback game state
      gameState.sessionId = 'fallback_session';
      gameState.allScenariosData = fallbackScenarios;
      gameState.scenarios = fallbackScenarios;
      
      // Load first fallback scenario
      loadScenario(fallbackScenarios[0]);
    }
  }
  
  // Function to load a scenario
  function loadScenario(scenario) {
    console.log('🔄 Loading scenario:', gameState.currentScenario + 1, scenario);
    
    // Store the current scenario data to prevent changes during gameplay
    gameState.currentScenarioData = JSON.parse(JSON.stringify(scenario)); // Deep copy
    gameState.currentAnswerSubmitted = false; // Reset submission flag
    
    // Update scenario number
    scenarioNumber.textContent = gameState.currentScenario + 1;
    
    // Update scenario content
    scenarioElement.innerHTML = `<p class="text-lg text-gray-800">${scenario.content}</p>`;
    
    // Update options if scenario has them (from server)
    if (scenario.options) {
      console.log('📋 Loading options:', scenario.options);
      const translatedOptions = translateOptions(scenario.options);
      const optionElements = document.querySelectorAll('.option');
      
      ['A', 'B', 'C', 'D'].forEach((letter, index) => {
        if (optionElements[index] && translatedOptions[letter]) {
          const textDiv = optionElements[index].querySelector('.font-medium.text-gray-800');
          if (textDiv) {
            textDiv.textContent = translatedOptions[letter];
            // Make sure the option is visible and enabled
            optionElements[index].style.display = 'flex';
            optionElements[index].style.pointerEvents = 'auto';
            optionElements[index].style.opacity = '1';
            optionElements[index].style.cursor = 'pointer';
            optionElements[index].classList.remove('disabled');
          }
        } else if (optionElements[index]) {
          // Hide options that don't have content
          optionElements[index].style.display = 'none';
        }
      });
      
      console.log('✅ Options loaded successfully');
    } else {
      console.log('⚠️ No options found in scenario data');
    }
    
    // Clear selected option and reset UI state
    gameState.selectedOption = null;
    document.querySelectorAll('.option').forEach(opt => {
      opt.classList.remove('selected');
      opt.style.pointerEvents = 'auto';
      opt.classList.remove('disabled');
      opt.style.transform = '';
    });
    
    // Reset and disable submit button
    submitBtn.disabled = true;
    submitBtn.textContent = translations[currentLanguage].submitAnswer || 'Submit Answer';
    
    // Hide feedback and continue button
    feedbackElement.classList.add('hidden');
    if (continueBtn) {
      continueBtn.classList.add('hidden');
    }
    
    console.log('✅ Scenario loaded successfully');
  }
  
  // Function to handle API response
  function handleAPIResponse(data) {
    console.log('🔄 Processing API response:', data);
    
    // DO NOT restore submit button - keep it disabled to prevent resubmission
    console.log('🔒 Keeping submit button disabled to prevent multiple submissions');
    
    // Update score (use the score from the response if available)
    if (data.score !== undefined) {
      gameState.score = data.score;
    }
    updateScoreDisplay();
    
    // Prepare feedback content based on correctness
    const correctMessage = translations[currentLanguage].correct || '✓ Correct!';
    const incorrectMessage = translations[currentLanguage].incorrect || '✗ Incorrect';
    
    // Show feedback with enhanced styling
    if (data.is_correct) {
      feedbackElement.className = 'feedback correct bg-green-50 border-l-4 border-green-500 p-4 rounded-lg';
      feedbackElement.innerHTML = `
        <div class="flex items-center mb-2">
          <div class="bg-green-100 text-green-800 rounded-full p-1 mr-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <div class="font-bold text-lg text-green-800">${correctMessage}</div>
        </div>
        <p class="text-green-700">${data.explanation || 'Well done!'}</p>
      `;
    } else {
      feedbackElement.className = 'feedback incorrect bg-red-50 border-l-4 border-red-500 p-4 rounded-lg';
      feedbackElement.innerHTML = `
        <div class="flex items-center mb-2">
          <div class="bg-red-100 text-red-800 rounded-full p-1 mr-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </div>
          <div class="font-bold text-lg text-red-800">${incorrectMessage}</div>
        </div>
        <p class="text-red-700">The correct answer is ${data.correct_answer}. ${data.explanation || 'Try again!'}</p>
      `;
    }
    
    // Show feedback
    feedbackElement.classList.remove('hidden');
    
    // Store next scenario data for later use
    gameState.nextScenarioData = data;
    
    // Find and verify continue button exists
    const continueButton = document.getElementById('continue-btn');
    console.log('🔍 Looking for continue button:', continueButton);
    
    // Make sure we have a continue button
    if (continueButton) {
      console.log('✅ Continue button found');
      
      // Set appropriate text based on game state
      if (data.game_completed) {
        continueButton.innerHTML = `
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 00-2-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
          </svg>
          ${translations[currentLanguage].viewResults || 'View Results'}
        `;
        console.log('🏁 Game completed - showing View Results button');
      } else {
        continueButton.innerHTML = `
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
          </svg>
          ${translations[currentLanguage].continue || 'Continue'}
        `;
        console.log('➡️ Next scenario available - showing Continue button');
      }
      
      // Make sure the continue button is visible
      continueButton.classList.remove('hidden');
      
      // Ensure it has the correct event handler
      if (!continueButton.getAttribute('data-has-listener')) {
        continueButton.addEventListener('click', nextScenario);
        continueButton.setAttribute('data-has-listener', 'true');
        console.log('� Added event listener to continue button');
      }
      
      console.log('�👀 Continue button should now be visible and working');
    } else {
      console.error('❌ Continue button not found in the DOM!');
      
      // Create a fallback continue button and add it to the feedback element
      const fallbackButton = document.createElement('button');
      fallbackButton.id = 'fallback-continue-btn';
      fallbackButton.className = 'w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-xl transition duration-300 shadow-lg mt-4 flex items-center justify-center';
      fallbackButton.innerHTML = data.game_completed ? 'View Results' : 'Continue';
      fallbackButton.addEventListener('click', nextScenario);
      
      feedbackElement.appendChild(fallbackButton);
      console.log('⚠️ Created fallback continue button');
    }
  }
  
  // Function to submit an answer
  async function submitAnswer() {
    if (!gameState.selectedOption) return;
    
    // Prevent multiple submissions for the same scenario
    if (gameState.currentAnswerSubmitted) {
      console.log('⚠️ Answer already submitted for this scenario, ignoring');
      return;
    }
    
    console.log('🚀 Submitting answer:', gameState.selectedOption, 'for scenario:', gameState.currentScenario);
    
    // Mark this scenario as answered to prevent multiple submissions
    gameState.currentAnswerSubmitted = true;
    
    // Show loading state and disable all interaction
    submitBtn.disabled = true;
    submitBtn.textContent = translations[currentLanguage].submitting || 'Submitting...';
    
    // Disable all option selections
    document.querySelectorAll('.option').forEach(opt => {
      opt.style.pointerEvents = 'none';
      opt.classList.add('disabled');
    });
    
    // Store the current scenario data to prevent changes
    const currentScenarioData = gameState.currentScenarioData;
    if (!currentScenarioData) {
      console.error('❌ No current scenario data available');
      return;
    }
    
    console.log('📊 Using scenario data:', currentScenarioData);
    
    // Try to use API for response evaluation
    try {
      if (gameState.sessionId) {
        console.log(`📤 Calling API: ${API_BASE_URL}/api/v1/games/${gameState.gameId}/sessions/${gameState.sessionId}/response`);
        
        const response = await fetch(`${API_BASE_URL}/api/v1/games/${gameState.gameId}/sessions/${gameState.sessionId}/response`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            selected_option: gameState.selectedOption,
            scenario_id: gameState.currentScenario.toString()
          }),
        });
        
        console.log('📡 API Response status:', response.status);
        
        if (response.ok) {
          const data = await response.json();
          console.log('✅ API response successful:', data);
          
          // Process API response and update UI
          handleAPIResponse(data);
          return; // Exit if API call succeeds
        } else {
          console.error('❌ API response not ok:', response.status, response.statusText);
          const errorText = await response.text();
          console.error('Error details:', errorText);
        }
      } else {
        console.error('❌ No session ID available for API call');
      }
    } catch (error) {
      console.error('💥 Error submitting answer:', error);
    }
    
    // Fallback to local handling if API not available
    console.log('⚠️ Using local evaluation fallback');
    
    // Use the stored scenario data to ensure consistency
    const isCorrect = gameState.selectedOption === currentScenarioData.correctOption;
    console.log(`🔍 Checking answer: selected=${gameState.selectedOption}, correct=${currentScenarioData.correctOption}, isCorrect=${isCorrect}`);
    
    // Update score only if correct
    if (isCorrect) {
      gameState.score += 10;
      updateScoreDisplay();
    }
    
    // Create consistent response data
    const mockData = {
      is_correct: isCorrect,
      correct_answer: currentScenarioData.correctOption,
      explanation: currentScenarioData.explanation || `This scenario demonstrates ${currentScenarioData.qualityAttribute || currentScenarioData.category}.`,
      score: gameState.score,
      game_completed: gameState.currentScenario >= gameState.totalScenarios - 1,
    };
    
    // If there are more scenarios in the stored data, include the next one
    if (!mockData.game_completed && gameState.allScenariosData && gameState.allScenariosData[gameState.currentScenario + 1]) {
      mockData.next_scenario = gameState.allScenariosData[gameState.currentScenario + 1];
    }
    
    console.log('📝 Processing response with data:', mockData);
    
    // Store the response data and handle it
    gameState.nextScenarioData = mockData;
    handleAPIResponse(mockData);
  }
  
  // Function to go to the next scenario
  function nextScenario() {
    console.log("⏩ Next scenario function called for scenario:", gameState.currentScenario);
    
    // Hide feedback and continue button
    if (feedbackElement) feedbackElement.classList.add('hidden');
    if (continueBtn) continueBtn.classList.add('hidden');
    
    const data = gameState.nextScenarioData;
    console.log("📊 Next scenario data:", data);
    
    // Check if game is completed based on scenario count, not server response
    const nextScenarioIndex = gameState.currentScenario + 1;
    console.log(`🔢 Next scenario index: ${nextScenarioIndex}, Total scenarios: ${gameState.totalScenarios}`);
    
    if (nextScenarioIndex >= gameState.totalScenarios) {
      // End of game - we've completed all scenarios
      console.log("🏁 Game completed based on scenario count, showing results");
      showResults();
      return;
    }
    
    // Show loading for next scenario
    if (scenarioElement) {
      scenarioElement.innerHTML = `
        <div class="text-center">
          <div class="inline-block animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600 mb-2"></div>
          <p class="text-gray-600">🤖 Loading next scenario...</p>
        </div>
      `;
    }
    
    // Increment scenario counter
    gameState.currentScenario = nextScenarioIndex;
    console.log(`➡️ Moving to scenario ${gameState.currentScenario + 1}`);
    
    // Try to get next scenario from stored data first
    let nextScenarioData = null;
    
    if (gameState.allScenariosData && gameState.allScenariosData[gameState.currentScenario]) {
      nextScenarioData = gameState.allScenariosData[gameState.currentScenario];
      console.log("📦 Using stored scenario data");
    } else if (data && data.next_scenario) {
      nextScenarioData = data.next_scenario;
      console.log("📡 Using scenario from API response");
    } else if (gameState.scenarios && gameState.scenarios[gameState.currentScenario]) {
      nextScenarioData = gameState.scenarios[gameState.currentScenario];
      console.log("📚 Using fallback scenario data");
    }
    
    if (nextScenarioData) {
      console.log("✅ Loading next scenario:", nextScenarioData);
      loadScenario(nextScenarioData);
    } else {
      // If we don't have data for the next scenario, show error
      console.error("❌ No next scenario data available");
      scenarioElement.innerHTML = `
        <div class="text-center">
          <p class="text-lg text-red-600">❌ Error: Unable to load next scenario</p>
          <p class="text-sm text-gray-600">Please try starting a new game</p>
          <button onclick="location.reload()" class="mt-4 bg-blue-600 text-white px-4 py-2 rounded">Restart Game</button>
        </div>
      `;
    }
  }
  
  // Function to show results
  function showResults() {
    // Hide other screens
    introScreen.classList.add('hidden');
    gameScreen.classList.add('hidden');
    resultScreen.classList.remove('hidden');
    
    // Update final score
    finalScoreElement.textContent = gameState.score;
    
    // Determine result message based on score and language
    let message = '';
    const lang = currentLanguage || 'en';
    
    if (gameState.score >= 60) { // Updated threshold for 8 scenarios (max 80 points)
      message = translations[lang].excellentResult;
      addBadge(translations[lang].qualityExpert);
    } else if (gameState.score >= 40) {
      message = translations[lang].goodResult;
      addBadge(translations[lang].qualityApprentice);
    } else {
      message = translations[lang].improvementNeeded;
      addBadge(translations[lang].qualityNovice);
    }
    resultMessage.textContent = message;
  }
  
  // Function to add a badge
  function addBadge(badgeName) {
    const badge = document.createElement('div');
    badge.className = 'badge-earned bg-blue-100 border-2 border-blue-500 rounded-full p-3 text-center';
    badge.innerHTML = `
      <div class="text-3xl mb-1">🏆</div>
      <div class="font-bold">${badgeName}</div>
    `;
    badgesContainer.appendChild(badge);
    gameState.badges.push(badgeName);
  }
  
  // Function to update the score display
  function updateScoreDisplay() {
    scoreElement.textContent = gameState.score;
  }
  
  // Function to reset the game
  function resetGame() {
    console.log('🔄 RESETTING GAME - clearing all state');
    
    // Clear badges
    badgesContainer.innerHTML = '';
    
    // Completely clear game state
    gameState = {
      currentScenario: 0,
      totalScenarios: 5,
      score: 0,
      selectedOption: null,
      scenarios: [],
      sessionId: null,
      gameId: 'quality_quest',
      badges: [],
      currentScenarioData: null,
      currentAnswerSubmitted: false,
      allScenariosData: null,
      nextScenarioData: null
    };
    
    // Clear any cached data
    if (window.sessionStorage) {
      window.sessionStorage.clear();
    }
    
    console.log('🆕 Starting completely fresh game');
    // Start new game
    startGame();
  }
  
  // Language translations
  const translations = {
    en: {
      welcome: "Welcome to QualityQuest!",
      introduction: "In this game, you'll analyze different software development scenarios and identify which of the 8 quality attributes from ISO/IEC 25010 is most relevant in each case.",
      qualityAttributes: "ISO/IEC 25010 Quality Attributes:",
      functionalSuitability: "Functional Suitability",
      performanceEfficiency: "Performance Efficiency",
      compatibility: "Compatibility",
      usability: "Usability",
      reliability: "Reliability",
      security: "Security",
      maintainability: "Maintainability",
      portability: "Portability",
      howToPlay: "How to Play:",
      howToPlayStep1: "Read each scenario carefully",
      howToPlayStep2: "Choose the quality attribute that is most relevant to the scenario",
      howToPlayStep3: "Submit your answer to see if you're correct",
      howToPlayStep4: "Learn from the explanation provided",
      howToPlayStep5: "Earn points for correct answers and complete all scenarios to win!",
      startGame: "Start Game",
      submitAnswer: "Submit Answer",
      submitting: "Submitting...",
      continue: "Continue",
      viewResults: "View Results",
      playAgain: "Play Again",
      scenario: "Scenario:",
      score: "Score:",
      whichAttribute: "Which quality attribute is most relevant?",
      correct: "✓ Correct!",
      incorrect: "✗ Incorrect",
      continue: "Continue",
      gameCompleted: "Game Completed!",
      finalScore: "Score:",
      badgesEarned: "Badges Earned:",
      returnToGames: "Return to Games List",
      qualityExpert: "Quality Expert",
      qualityApprentice: "Quality Apprentice",
      qualityNovice: "Quality Novice",
      excellentResult: "Excellent! You have a great understanding of ISO/IEC 25010 quality attributes!",
      goodResult: "Good job! You have a solid grasp of ISO/IEC 25010 quality attributes.",
      improvementNeeded: "Keep practicing! You'll improve your understanding of ISO/IEC 25010 quality attributes."
    },
    es: {
      welcome: "¡Bienvenido a QualityQuest!",
      introduction: "En este juego, analizarás diferentes escenarios de desarrollo de software e identificarás cuál de los 8 atributos de calidad de ISO/IEC 25010 es más relevante en cada caso.",
      qualityAttributes: "Atributos de Calidad ISO/IEC 25010:",
      functionalSuitability: "Adecuación Funcional",
      performanceEfficiency: "Eficiencia de Desempeño",
      compatibility: "Compatibilidad",
      usability: "Usabilidad",
      reliability: "Fiabilidad",
      security: "Seguridad",
      maintainability: "Mantenibilidad",
      portability: "Portabilidad",
      howToPlay: "Cómo Jugar:",
      howToPlayStep1: "Lee cada escenario cuidadosamente",
      howToPlayStep2: "Elige el atributo de calidad que sea más relevante para el escenario",
      howToPlayStep3: "Envía tu respuesta para ver si es correcta",
      howToPlayStep4: "Aprende de la explicación proporcionada",
      howToPlayStep5: "¡Gana puntos por respuestas correctas y completa todos los escenarios para ganar!",
      startGame: "Iniciar Juego",
      submitAnswer: "Enviar Respuesta",
      submitting: "Enviando...",
      continue: "Continuar",
      viewResults: "Ver Resultados",
      playAgain: "Jugar de Nuevo",
      scenario: "Escenario:",
      score: "Puntuación:",
      whichAttribute: "¿Qué atributo de calidad es más relevante?",
      correct: "✓ ¡Correcto!",
      incorrect: "✗ Incorrecto",
      continue: "Continuar",
      gameCompleted: "¡Juego Completado!",
      finalScore: "Puntuación:",
      badgesEarned: "Insignias Ganadas:",
      returnToGames: "Volver a la Lista de Juegos",
      qualityExpert: "Experto en Calidad",
      qualityApprentice: "Aprendiz de Calidad",
      qualityNovice: "Novato en Calidad",
      excellentResult: "¡Excelente! ¡Tienes un gran entendimiento de los atributos de calidad de ISO/IEC 25010!",
      goodResult: "¡Buen trabajo! Tienes una comprensión sólida de los atributos de calidad de ISO/IEC 25010.",
      improvementNeeded: "¡Sigue practicando! Mejorarás tu comprensión de los atributos de calidad de ISO/IEC 25010."
    }
  };
  
  // Function to update UI language
  function updateLanguage(lang) {
    // Update current language
    currentLanguage = lang;
    
    // Update intro screen
    const welcomeEl = document.querySelector('#intro-screen h3');
    if (welcomeEl) welcomeEl.textContent = translations[lang].welcome;
    
    const introEl = document.querySelector('#intro-screen > div:nth-child(2) p');
    if (introEl) introEl.textContent = translations[lang].introduction;
    
    const qualityAttrEl = document.querySelector('.bg-primary-50 h4');
    if (qualityAttrEl) qualityAttrEl.textContent = translations[lang].qualityAttributes;
    
    // Update quality attributes
    const qualityAttributeOptions = [
      { selector: '.option[data-option="A"] div:nth-child(2)', key: 'functionalSuitability' },
      { selector: '.option[data-option="B"] div:nth-child(2)', key: 'performanceEfficiency' },
      { selector: '.option[data-option="C"] div:nth-child(2)', key: 'compatibility' },
      { selector: '.option[data-option="D"] div:nth-child(2)', key: 'usability' },
      { selector: '.option[data-option="E"] div:nth-child(2)', key: 'reliability' },
      { selector: '.option[data-option="F"] div:nth-child(2)', key: 'security' },
      { selector: '.option[data-option="G"] div:nth-child(2)', key: 'maintainability' },
      { selector: '.option[data-option="H"] div:nth-child(2)', key: 'portability' }
    ];
    
    qualityAttributeOptions.forEach(attr => {
      const elem = document.querySelector(attr.selector);
      if (elem) elem.textContent = translations[lang][attr.key];
    });
    
    // Update how to play section
    const howToPlayEl = document.querySelector('.bg-secondary-50 h4');
    if (howToPlayEl) howToPlayEl.textContent = translations[lang].howToPlay;
    
    const howToPlaySteps = document.querySelectorAll('.bg-secondary-50 .space-y-3 p');
    if (howToPlaySteps.length >= 5) {
      howToPlaySteps[0].innerHTML = translations[lang].howToPlayStep1;
      howToPlaySteps[1].innerHTML = translations[lang].howToPlayStep2;
      howToPlaySteps[2].innerHTML = translations[lang].howToPlayStep3;
      howToPlaySteps[3].innerHTML = translations[lang].howToPlayStep4;
      howToPlaySteps[4].innerHTML = translations[lang].howToPlayStep5;
    }
    
    // Update buttons
    if (startGameBtn) startGameBtn.textContent = translations[lang].startGame;
    if (submitBtn) submitBtn.textContent = translations[lang].submitAnswer;
    if (continueBtn) continueBtn.textContent = translations[lang].continue;
    if (playAgainBtn) playAgainBtn.textContent = translations[lang].playAgain;
    
    // Update game screen labels
    const scenarioLabelEl = document.querySelector('.font-bold.text-xl.text-primary-800');
    if (scenarioLabelEl) scenarioLabelEl.textContent = translations[lang].scenario + " ";
    
    const scoreLabelEl = document.querySelector('.bg-accent-600.text-white');
    if (scoreLabelEl && scoreLabelEl.childNodes[0]) {
      scoreLabelEl.childNodes[0].textContent = translations[lang].score + " ";
    }
    document.querySelector('h3.font-bold.text-xl.mb-4').textContent = 
      translations[lang].whichAttribute;
    
    // Update result screen
    document.querySelector('#result-screen h3').textContent = translations[lang].gameCompleted;
    document.querySelector('.text-5xl.font-bold').childNodes[0].textContent = 
      translations[lang].finalScore + " ";
    document.querySelector('h4.font-bold.text-xl.mb-4').textContent = translations[lang].badgesEarned;
    document.querySelector('a[href="/"].bg-white').textContent = translations[lang].returnToGames;
    
    // Update any visible feedback
    if (!feedbackElement.classList.contains('hidden')) {
      const correctText = feedbackElement.querySelector('.font-bold');
      if (correctText) {
        if (feedbackElement.classList.contains('correct')) {
          correctText.textContent = translations[lang].correct;
        } else {
          correctText.textContent = translations[lang].incorrect;
        }
      }
      
      const continueBtn = feedbackElement.querySelector('button');
      if (continueBtn) {
        continueBtn.textContent = translations[lang].continue;
      }
    }
    
    // Language changes during game require restarting the session
    // since scenarios come from the database, not hardcoded
  }
  
  // Function to handle language changes from main.js
  function handleLanguageChange(event) {
    const lang = event.detail ? event.detail.language : (localStorage.getItem('iso-games-language') || 'en');
    updateLanguage(lang);
  }
  
  // Create custom event listener for language changes
  window.addEventListener('language-changed', handleLanguageChange);
  
  // Also listen for storage changes in case language is changed in another tab
  window.addEventListener('storage', function(e) {
    if (e.key === 'iso-games-language') {
      updateLanguage(e.newValue || 'en');
    }
  });
  
  // Initialize with current language
  updateLanguage(currentLanguage);
  
  // Create a MutationObserver to detect changes in the document's lang attribute
  const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
      if (mutation.attributeName === 'lang') {
        const newLang = document.documentElement.getAttribute('lang');
        if (newLang && (newLang === 'en' || newLang === 'es')) {
          updateLanguage(newLang);
        }
      }
    });
  });
  
  // Start observing changes to document.documentElement
  observer.observe(document.documentElement, { attributes: true });
});