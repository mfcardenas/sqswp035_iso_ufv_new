// Main JavaScript for ISO Standards Games

document.addEventListener('DOMContentLoaded', function() {
  // API Configuration - use centralized config
  const API_BASE_URL = window.CONFIG ? window.CONFIG.API.BASE_URL : '';
  // Language switching functionality
  const languageModal = document.getElementById('language-modal');
  const langButtons = document.querySelectorAll('.language-selector');
  const closeLangModal = document.getElementById('close-lang-modal');
  const langOptions = document.querySelectorAll('.lang-option');
  
  // Default language is English or from localStorage
  let currentLanguage = localStorage.getItem('iso-games-language') || 'en';
  
  // UI text translations
  const translations = {
    en: {
      welcome: "Welcome to ISO Standards Games",
      subtitle: "Interactive learning of ISO/IEC standards through gamification",
      learn: "Learn about important software quality standards through engaging, interactive games:",
      standard1: "ISO/IEC 25010 - Software Quality",
      standard2: "ISO/IEC/IEEE 29148 - Requirements Engineering",
      standard3: "ISO 9241 - Ergonomics of Human-System Interaction",
      quote: "Standards are the foundation of quality software development. Through gamification, we make learning these essential standards engaging and effective.",
      startGame: "Start Game",
      submitAnswer: "Submit Answer",
      comingSoon: "Coming Soon",
      difficulty: "Difficulty:",
      progress: "Your Progress",
      gamesCompleted: "Games Completed",
      totalPoints: "Total Points",
      startPlaying: "Start playing to track your progress!",
      viewDashboard: "View Dashboard",
      about: "About",
      help: "Help",
      privacy: "Privacy",
      contact: "Contact",
      footerText: "This project is designed for educational purposes to help students learn about ISO/IEC standards.",
      selectLanguage: "Select Language",
      english: "English",
      englishDesc: "English language version",
      spanish: "Español",
      spanishDesc: "Versión en español",
      // Game specific translations
      qualityQuest: "QualityQuest",
      qualityQuestDesc: "Identify the 8 quality attributes from ISO/IEC 25010 in various software scenarios.",
      requirementRally: "RequirementRally",
      requirementRallyDesc: "Learn requirements specification principles from ISO/IEC/IEEE 29148.",
      usabilityUniverse: "UsabilityUniverse",
      usabilityUniverseDesc: "Explore usability principles from ISO 9241 and improve user interfaces.",
      standardSafari: "StandardSafari",
      standardSafariDesc: "Explore multiple standards and their relationships in real-world scenarios.",
      finalChallenge: "FinalChallenge",
      finalChallengeDesc: "Test your comprehensive knowledge of all ISO standards covered in previous games."
    },
    es: {
      welcome: "Bienvenido a Juegos de Estándares ISO",
      subtitle: "Aprendizaje interactivo de estándares ISO/IEC a través de la gamificación",
      learn: "Aprende sobre importantes estándares de calidad de software a través de juegos interactivos y atractivos:",
      standard1: "ISO/IEC 25010 - Calidad de Software",
      standard2: "ISO/IEC/IEEE 29148 - Ingeniería de Requisitos",
      standard3: "ISO 9241 - Ergonomía de la Interacción Humano-Sistema",
      quote: "Los estándares son la base del desarrollo de software de calidad. A través de la gamificación, hacemos que el aprendizaje de estos estándares esenciales sea atractivo y efectivo.",
      startGame: "Iniciar Juego",
      submitAnswer: "Enviar Respuesta",
      comingSoon: "Próximamente",
      difficulty: "Dificultad:",
      progress: "Tu Progreso",
      gamesCompleted: "Juegos Completados",
      totalPoints: "Puntos Totales",
      startPlaying: "¡Comienza a jugar para seguir tu progreso!",
      viewDashboard: "Ver Panel",
      about: "Acerca de",
      help: "Ayuda",
      privacy: "Privacidad",
      contact: "Contacto",
      footerText: "Este proyecto está diseñado con fines educativos para ayudar a los estudiantes a aprender sobre los estándares ISO/IEC.",
      selectLanguage: "Seleccionar Idioma",
      english: "English",
      englishDesc: "Versión en inglés",
      spanish: "Español",
      spanishDesc: "Versión en español",
      // Game specific translations
      qualityQuest: "QualityQuest",
      qualityQuestDesc: "Identifica los 8 atributos de calidad de ISO/IEC 25010 en varios escenarios de software.",
      requirementRally: "RequirementRally",
      requirementRallyDesc: "Aprende principios de especificación de requisitos de ISO/IEC/IEEE 29148.",
      usabilityUniverse: "UsabilityUniverse",
      usabilityUniverseDesc: "Explora principios de usabilidad de ISO 9241 y mejora interfaces de usuario.",
      standardSafari: "StandardSafari",
      standardSafariDesc: "Explora múltiples estándares y sus relaciones en escenarios del mundo real.",
      finalChallenge: "RetoFinal",
      finalChallengeDesc: "Pon a prueba tu conocimiento integral de todos los estándares ISO cubiertos en juegos anteriores."
    }
  };
  
  // Apply the current language on page load
  applyLanguage(currentLanguage);
  
  // Show language modal when language buttons are clicked
  langButtons.forEach(button => {
    button.addEventListener('click', () => {
      languageModal.classList.remove('hidden');
      languageModal.classList.add('flex');
    });
  });
  
  // Close language modal with close button
  if (closeLangModal) {
    closeLangModal.addEventListener('click', () => {
      languageModal.classList.add('hidden');
      languageModal.classList.remove('flex');
    });
  }
  
  // Handle language selection from modal
  langOptions.forEach(option => {
    option.addEventListener('click', () => {
      const lang = option.getAttribute('data-lang');
      currentLanguage = lang;
      localStorage.setItem('iso-games-language', lang);
      applyLanguage(lang);
      languageModal.classList.add('hidden');
      languageModal.classList.remove('flex');
    });
  });
  
  // Close modal if clicking outside
  languageModal?.addEventListener('click', (e) => {
    if (e.target === languageModal) {
      languageModal.classList.add('hidden');
      languageModal.classList.remove('flex');
    }
  });
  
  // Function to update UI language
  function applyLanguage(lang) {
    document.documentElement.setAttribute('lang', lang);
    
    // Update header language buttons with better visibility
    document.querySelectorAll('.language-selector').forEach(btn => {
      if (btn.id === `lang-${lang}`) {
        btn.classList.add('bg-white', 'bg-opacity-40', 'font-bold');
        btn.classList.remove('bg-opacity-20');
      } else {
        btn.classList.remove('bg-white', 'bg-opacity-40', 'font-bold');
        btn.classList.add('bg-opacity-20');
      }
    });
    
    // Update welcome section (only if elements exist)
    const welcomeH2 = document.querySelector('#welcome h2');
    if (welcomeH2) welcomeH2.textContent = translations[lang].welcome;
    
    const welcomeSubtitle = document.querySelector('#welcome p.text-xl');
    if (welcomeSubtitle) welcomeSubtitle.textContent = translations[lang].subtitle;
    
    const welcomeLearn = document.querySelector('#welcome .text-left p');
    if (welcomeLearn) welcomeLearn.textContent = translations[lang].learn;
    
    // Update standards list
    const standards = [
      document.querySelector('#welcome .text-left li:nth-of-type(1)'),
      document.querySelector('#welcome .text-left li:nth-of-type(2)'),
      document.querySelector('#welcome .text-left li:nth-of-type(3)')
    ];
    
    standards.forEach((item, index) => {
      if (item) {
        const standardKey = `standard${index + 1}`;
        const span = item.querySelector('span');
        if (span && translations[lang][standardKey]) {
          const parts = translations[lang][standardKey].split('-');
          if (parts.length > 1) {
            span.textContent = parts[0].trim();
            const textNode = document.createTextNode(` - ${parts[1].trim()}`);
            item.innerHTML = '';
            item.appendChild(span);
            item.appendChild(textNode);
          }
        }
      }
    });
    
    // Update quote
    const quoteElem = document.querySelector('.bg-primary-50 p');
    if (quoteElem) {
      quoteElem.textContent = translations[lang].quote;
    }
    
    // Update game cards
    const gameDescriptions = {
      'qualityQuest': document.querySelector('.game-card:nth-of-type(1) p.mb-4'),
      'requirementRally': document.querySelector('.game-card:nth-of-type(2) p.mb-4'),
      'usabilityUniverse': document.querySelector('.game-card:nth-of-type(3) p.mb-4'),
      'standardSafari': document.querySelector('.game-card:nth-of-type(4) p.mb-4'),
      'finalChallenge': document.querySelector('.game-card:nth-of-type(5) p.mb-4')
    };
    
    Object.entries(gameDescriptions).forEach(([key, element]) => {
      if (element && translations[lang][`${key}Desc`]) {
        element.textContent = translations[lang][`${key}Desc`];
      }
    });
    
    // Update buttons
    const startButtons = document.querySelectorAll('a.bg-primary-500');
    startButtons.forEach(button => {
      button.textContent = translations[lang].startGame;
    });
    
    const comingSoonButtons = document.querySelectorAll('button[disabled]');
    comingSoonButtons.forEach(button => {
      // Skip buttons inside game containers or with specific IDs
      if (button.id === 'submit-btn' || button.closest('.game-container') || button.closest('#game-screen')) {
        return;
      }
      button.textContent = translations[lang].comingSoon;
    });
    
    // Update difficulty text
    const difficultyLabels = document.querySelectorAll('.flex.items-center span.text-sm');
    difficultyLabels.forEach(label => {
      label.textContent = translations[lang].difficulty;
    });
    
    // Update progress card
    const progressTitle = document.querySelector('.game-card:nth-of-type(6) h3');
    if (progressTitle) progressTitle.textContent = translations[lang].progress;
    
    const gamesCompletedLabel = document.querySelector('.game-card:nth-of-type(6) .space-y-4 div:nth-of-type(1) .flex.justify-between span:first-child');
    if (gamesCompletedLabel) gamesCompletedLabel.textContent = translations[lang].gamesCompleted;
    
    const totalPointsLabel = document.querySelector('.game-card:nth-of-type(6) .space-y-4 div:nth-of-type(2) .flex.justify-between span:first-child');
    if (totalPointsLabel) totalPointsLabel.textContent = translations[lang].totalPoints;
    
    const startPlayingText = document.querySelector('.game-card:nth-of-type(6) .flex.items-center span');
    if (startPlayingText) startPlayingText.textContent = translations[lang].startPlaying;
    
    const viewDashboardButton = document.querySelector('.game-card:nth-of-type(6) a.block');
    if (viewDashboardButton) viewDashboardButton.textContent = translations[lang].viewDashboard;
    
    // Update footer
    const footerLinks = document.querySelectorAll('footer .flex.flex-col.md\\:flex-row.space-y-2 a');
    const footerLinkLabels = [translations[lang].about, translations[lang].help, translations[lang].privacy, translations[lang].contact];
    footerLinks.forEach((link, index) => {
      if (index < footerLinkLabels.length) {
        link.textContent = footerLinkLabels[index];
      }
    });
    
    const footerText = document.querySelector('footer .text-sm.text-gray-500 p');
    if (footerText) footerText.textContent = translations[lang].footerText;
    
    // Update language modal
    const modalTitle = document.querySelector('#language-modal h2');
    if (modalTitle) modalTitle.textContent = translations[lang].selectLanguage;
    
    const englishOption = document.querySelector('.lang-option[data-lang="en"] .text-left p.font-medium');
    const englishDesc = document.querySelector('.lang-option[data-lang="en"] .text-left p.text-sm');
    if (englishOption) englishOption.textContent = translations[lang].english;
    if (englishDesc) englishDesc.textContent = translations[lang].englishDesc;
    
    const spanishOption = document.querySelector('.lang-option[data-lang="es"] .text-left p.font-medium');
    const spanishDesc = document.querySelector('.lang-option[data-lang="es"] .text-left p.text-sm');
    if (spanishOption) spanishOption.textContent = translations[lang].spanish;
    if (spanishDesc) spanishDesc.textContent = translations[lang].spanishDesc;
  }
  
  // Fetch API data
  async function fetchGames() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/games/`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      console.log('Available games:', data);
      
      // In a real implementation, we would use this data to populate the game cards dynamically
      
    } catch (error) {
      console.error('Failed to fetch games:', error);
    }
  }
  
  // Fetch games data
  fetchGames();
  
  // Add some animation effects
  const gameCards = document.querySelectorAll('.game-card');
  gameCards.forEach((card, index) => {
    // Add a small delay to each card for a staggered entrance effect
    setTimeout(() => {
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, 100 * index);
  });
});

// Function to start Quality Quest game
function startQualityQuest() {
  console.log('Starting Quality Quest game...');
  
  // Hide the main content and show the quality quest game
  const mainContent = document.querySelector('main');
  const qualityQuestContent = document.getElementById('quality-quest-content');
  
  if (mainContent && qualityQuestContent) {
    mainContent.style.display = 'none';
    qualityQuestContent.style.display = 'block';
    
    // Initialize the game if startGame function exists
    if (typeof startGame === 'function') {
      startGame();
    }
  } else {
    console.error('Could not find main content or quality quest content elements');
  }
}