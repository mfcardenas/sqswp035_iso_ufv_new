#!/usr/bin/env python
"""
Usability scenarios database for UsabilityUniverse game
Handles loading and selection of usability principle scenarios from JSON file
"""

import json
import random
import os
from typing import List, Dict, Any, Optional

# Path to the JSON file
SCENARIOS_FILE = os.path.join(os.path.dirname(__file__), 'usability_scenarios.json')

# Global tracker for recently used scenarios to avoid repetition
_recently_used_scenarios = []
_max_recent_scenarios = 10  # Keep track of last 10 used scenarios

def load_scenarios() -> Dict[str, Any]:
    """Load scenarios from JSON file"""
    try:
        with open(SCENARIOS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Could not find scenarios file at {SCENARIOS_FILE}")
        return {"scenarios": [], "game_info": {}}
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in scenarios file: {e}")
        return {"scenarios": [], "game_info": {}}

def get_random_scenarios(count: int = 5, category: Optional[str] = None, difficulty: Optional[str] = None, language: str = 'en', force_new_selection: bool = False) -> List[Dict[str, Any]]:
    """
    Get random scenarios from the database with improved variety to avoid repetition
    
    Args:
        count: Number of scenarios to return (default 5)
        category: Filter by category ('Learnability', 'Efficiency', 'Memorability', 'Error_Prevention', 'User_Satisfaction')
        difficulty: Filter by difficulty ('easy', 'medium', 'hard')
        language: Language for content ('en' or 'es', default 'en')
        force_new_selection: If True, prioritize scenarios not used recently
        
    Returns:
        List of scenario dictionaries with content localized to specified language
    """
    global _recently_used_scenarios
    
    data = load_scenarios()
    scenarios = data.get('scenarios', [])
    
    if not scenarios:
        print("WARNING: No scenarios found in database")
        return []
    
    # Filter by category if specified
    if category:
        scenarios = [s for s in scenarios if s.get('category', '').lower() == category.lower()]
        print(f"Filtered to {len(scenarios)} scenarios for category: {category}")
    
    # Filter by difficulty if specified
    if difficulty:
        scenarios = [s for s in scenarios if s.get('difficulty', '').lower() == difficulty.lower()]
        print(f"Filtered to {len(scenarios)} scenarios for difficulty: {difficulty}")

    if not scenarios:
        print("WARNING: No scenarios match the specified filters")
        return []

    # Prioritize scenarios not used recently if force_new_selection is True
    if force_new_selection and _recently_used_scenarios:
        unused_scenarios = [s for s in scenarios if s.get('id') not in _recently_used_scenarios]
        if unused_scenarios:
            scenarios = unused_scenarios
            print(f"Prioritizing {len(scenarios)} unused scenarios to avoid repetition")
        else:
            print("All scenarios have been used recently, selecting from full pool")
    
    # Select random scenarios
    selected_count = min(count, len(scenarios))
    selected_scenarios = random.sample(scenarios, selected_count)
    
    # Update recently used tracker
    for scenario in selected_scenarios:
        scenario_id = scenario.get('id')
        if scenario_id:
            if scenario_id in _recently_used_scenarios:
                _recently_used_scenarios.remove(scenario_id)  # Remove if already present
            _recently_used_scenarios.append(scenario_id)  # Add to end
    
    # Keep only the most recent scenarios in tracker
    if len(_recently_used_scenarios) > _max_recent_scenarios:
        _recently_used_scenarios = _recently_used_scenarios[-_max_recent_scenarios:]
    
    print(f"Selected {selected_count} scenarios in language: {language}")
    print(f"Recently used scenarios tracker: {len(_recently_used_scenarios)} scenarios")
    
    # Localize content to specified language
    localized_scenarios = []
    for scenario in selected_scenarios:
        localized_scenario = localize_scenario(scenario, language)
        localized_scenarios.append(localized_scenario)

    return localized_scenarios

def localize_scenario(scenario: Dict[str, Any], language: str) -> Dict[str, Any]:
    """
    Localize scenario content to specified language
    
    Args:
        scenario: Scenario dictionary
        language: Target language ('en' or 'es')
        
    Returns:
        Scenario with localized content
    """
    localized = scenario.copy()
    
    # Get content for specified language, fallback to English if not available
    content_key = f'content_{language}' if language != 'en' else 'content'
    
    if content_key in scenario:
        localized['content'] = scenario[content_key]
    elif 'content' in scenario:
        localized['content'] = scenario['content']
    else:
        localized['content'] = "Content not available"
    
    # Localize feedback
    feedback_key = f'feedback_{language}' if language != 'en' else 'feedback'
    
    if feedback_key in scenario:
        localized['feedback'] = scenario[feedback_key]
    elif 'feedback' in scenario:
        localized['feedback'] = scenario['feedback']
    else:
        localized['feedback'] = "Feedback not available"
    
    # Localize options if they exist
    if 'options' in scenario:
        localized['options'] = scenario['options']
    
    return localized

def get_database_stats() -> Dict[str, Any]:
    """Get statistics about the scenarios database"""
    data = load_scenarios()
    scenarios = data.get('scenarios', [])
    
    if not scenarios:
        return {
            'total_scenarios': 0,
            'categories': {},
            'difficulties': {},
            'languages': []
        }
    
    # Count by category
    categories = {}
    for scenario in scenarios:
        cat = scenario.get('category', 'Unknown')
        categories[cat] = categories.get(cat, 0) + 1
    
    # Count by difficulty
    difficulties = {}
    for scenario in scenarios:
        diff = scenario.get('difficulty', 'Unknown')
        difficulties[diff] = difficulties.get(diff, 0) + 1
    
    # Detect available languages
    languages = set(['en'])  # English is always assumed to be available
    for scenario in scenarios:
        for key in scenario.keys():
            if key.startswith('content_') and key != 'content':
                lang = key.replace('content_', '')
                languages.add(lang)
            elif key.startswith('feedback_') and key != 'feedback':
                lang = key.replace('feedback_', '')
                languages.add(lang)
    
    return {
        'total_scenarios': len(scenarios),
        'categories': categories,
        'difficulties': difficulties,
        'languages': list(languages)
    }

def validate_scenarios() -> Dict[str, Any]:
    """Validate the scenarios database for completeness and correctness"""
    data = load_scenarios()
    scenarios = data.get('scenarios', [])
    
    errors = []
    warnings = []
    
    required_fields = ['id', 'content', 'category', 'correct_answer', 'feedback']
    optional_fields = ['difficulty', 'content_es', 'feedback_es', 'options']
    
    for i, scenario in enumerate(scenarios):
        scenario_id = scenario.get('id', f'scenario_{i}')
        
        # Check required fields
        for field in required_fields:
            if field not in scenario:
                errors.append(f"Scenario {scenario_id}: Missing required field '{field}'")
        
        # Validate category
        valid_categories = ['Learnability', 'Efficiency', 'Memorability', 'Error_Prevention', 'User_Satisfaction']
        if 'category' in scenario and scenario['category'] not in valid_categories:
            warnings.append(f"Scenario {scenario_id}: Unknown category '{scenario['category']}'")
        
        # Validate difficulty
        valid_difficulties = ['easy', 'medium', 'hard']
        if 'difficulty' in scenario and scenario['difficulty'] not in valid_difficulties:
            warnings.append(f"Scenario {scenario_id}: Unknown difficulty '{scenario['difficulty']}'")
        
        # Check for content length
        if 'content' in scenario and len(scenario['content']) < 10:
            warnings.append(f"Scenario {scenario_id}: Content seems too short")
    
    return {
        'total_scenarios': len(scenarios),
        'errors': errors,
        'warnings': warnings,
        'is_valid': len(errors) == 0
    }

if __name__ == "__main__":
    # Test the database functions
    print("UsabilityUniverse Scenarios Database Test")
    print("=" * 50)
    
    # Test loading
    stats = get_database_stats()
    print(f"Total scenarios: {stats['total_scenarios']}")
    print(f"Categories: {stats['categories']}")
    print(f"Difficulties: {stats['difficulties']}")
    print(f"Languages: {stats['languages']}")
    
    # Test validation
    validation = validate_scenarios()
    print(f"\nValidation results:")
    print(f"Valid: {validation['is_valid']}")
    print(f"Errors: {len(validation['errors'])}")
    print(f"Warnings: {len(validation['warnings'])}")
    
    # Test scenario retrieval
    scenarios = get_random_scenarios(3, language='en')
    print(f"\nSample scenarios (English): {len(scenarios)}")
    for scenario in scenarios:
        print(f"- {scenario.get('id', 'Unknown ID')}: {scenario.get('category', 'Unknown Category')}")