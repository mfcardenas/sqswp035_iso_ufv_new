// Configuration file for ISO Standards Games
// Single source of truth for all URLs and settings

const CONFIG = {
  // Server configuration
  SERVER: {
    PORT: 8001,
    HOST: '0.0.0.0'
  },
  
  // API endpoints - all relative to avoid hardcoded URLs
  API: {
    BASE_URL: '',  // Empty = relative URLs
    ENDPOINTS: {
      GAMES: '/api/v1/games',
      SESSIONS: '/api/v1/games/quality_quest/sessions',
      RESPONSE: '/api/v1/games/quality_quest/sessions/{sessionId}/response'
    }
  },
  
  // Frontend paths
  FRONTEND: {
    STATIC_DIR: './iso_standards_games/frontend/dist',
    INDEX_FILE: './iso_standards_games/frontend/dist/index.html'
  },
  
  // Game settings
  GAME: {
    TOTAL_SCENARIOS: 5,
    LLM_TIMEOUT: 15,
    SESSION_CLEANUP_INTERVAL: 3600 // 1 hour
  }
};

// Export for both Node.js and browser
if (typeof module !== 'undefined' && module.exports) {
  module.exports = CONFIG;
} else {
  window.CONFIG = CONFIG;
}