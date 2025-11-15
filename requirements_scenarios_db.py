#!/usr/bin/env python
"""
Requirements scenarios database for RequirementRally game
Handles loading and selection of requirement type scenarios from JSON file
"""

import json
import random
import os
from typing import List, Dict, Any, Optional

# Path to the JSON file
SCENARIOS_FILE = os.path.join(os.path.dirname(__file__), 'requirements_scenarios.json')

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

def get_random_scenarios(count: int = 5, category: Optional[str] = None, difficulty: Optional[str] = None, language: str = 'es') -> List[Dict[str, Any]]:
    """
    Get random scenarios from the database
    
    Args:
        count: Number of scenarios to return (default 5)
        category: Filter by category ('Functional', 'Non-Functional', 'Constraint')
        difficulty: Filter by difficulty ('easy', 'medium', 'hard')
        language: Language for content ('en' or 'es')
        
    Returns:
        List of scenario dictionaries with content localized to specified language
    """
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
        
    if len(scenarios) < count:
        print(f"WARNING: Only {len(scenarios)} scenarios available, requested {count}")
        count = len(scenarios)
    
    # Randomly select scenarios without replacement
    selected = random.sample(scenarios, count)
    
    # Localize content to specified language
    localized_scenarios = []
    for scenario in selected:
        localized = scenario.copy()
        
        # Localize content
        if isinstance(scenario.get('content'), dict):
            localized['content'] = scenario['content'].get(language, scenario['content'].get('es', ''))
        
        # Localize options
        if isinstance(scenario.get('options'), dict):
            localized['options'] = scenario['options'].get(language, scenario['options'].get('es', []))
        
        # Localize explanation
        if isinstance(scenario.get('explanation'), dict):
            localized['explanation'] = scenario['explanation'].get(language, scenario['explanation'].get('es', ''))
        
        localized_scenarios.append(localized)
    
    print(f"Selected {len(localized_scenarios)} random scenarios in {language}")
    for i, scenario in enumerate(localized_scenarios):
        print(f"   {i+1}. {scenario['id']} - {scenario['category']} ({scenario['difficulty']})")
    
    return localized_scenarios

def get_scenarios_by_category(category: str) -> List[Dict[str, Any]]:
    """Get all scenarios for a specific category"""
    data = load_scenarios()
    scenarios = data.get('scenarios', [])
    
    filtered = [s for s in scenarios if s.get('category') == category]
    print(f"📂 Found {len(filtered)} scenarios for category: {category}")
    
    return filtered

def get_database_stats() -> Dict[str, Any]:
    """Get statistics about the scenarios database"""
    data = load_scenarios()
    scenarios = data.get('scenarios', [])
    game_info = data.get('game_info', {})
    
    if not scenarios:
        return {"total": 0, "categories": {}, "difficulties": {}, "game_info": game_info}
    
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
    
    stats = {
        "total": len(scenarios),
        "categories": categories,
        "difficulties": difficulties,
        "game_info": game_info
    }
    
    print("📊 Database Statistics:")
    print(f"   Total scenarios: {stats['total']}")
    print(f"   Categories: {dict(stats['categories'])}")
    print(f"   Difficulties: {dict(stats['difficulties'])}")
    
    return stats

def validate_scenarios() -> Dict[str, Any]:
    """Validate all scenarios have required fields"""
    data = load_scenarios()
    scenarios = data.get('scenarios', [])
    
    required_fields = ['id', 'content', 'options', 'correctOption', 'explanation', 'category', 'difficulty']
    validation_results = {
        "total": len(scenarios),
        "valid": 0,
        "invalid": 0,
        "errors": []
    }
    
    for i, scenario in enumerate(scenarios):
        missing_fields = []
        for field in required_fields:
            if field not in scenario or not scenario[field]:
                missing_fields.append(field)
        
        if missing_fields:
            validation_results["invalid"] += 1
            validation_results["errors"].append({
                "scenario_index": i,
                "scenario_id": scenario.get('id', f'scenario_{i}'),
                "missing_fields": missing_fields
            })
        else:
            validation_results["valid"] += 1
    
    print("SUCCESS: Validation Results:")
    print(f"   Valid scenarios: {validation_results['valid']}")
    print(f"   Invalid scenarios: {validation_results['invalid']}")
    
    if validation_results["errors"]:
        print("ERROR: Errors found:")
        for error in validation_results["errors"][:5]:  # Show first 5 errors
            print(f"   - {error['scenario_id']}: missing {error['missing_fields']}")
    
    return validation_results

if __name__ == "__main__":
    print("RequirementRally Scenarios Database")
    print("=" * 50)
    
    # Show database stats
    stats = get_database_stats()
    print()
    
    # Validate scenarios
    validation = validate_scenarios()
    print()
    
    # Show some sample scenarios
    print("📝 Sample scenarios:")
    sample = get_random_scenarios(3)
    for i, scenario in enumerate(sample):
        print(f"\n{i+1}. {scenario['id']} ({scenario['category']}, {scenario['difficulty']})")
        print(f"   Content: {scenario['content'][:60]}...")
        print(f"   Correct: {scenario['correctOption']} - {scenario['options'][ord(scenario['correctOption']) - ord('A')]}")