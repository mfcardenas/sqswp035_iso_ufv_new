#!/usr/bin/env python3
"""
Validador de base de datos - encuentra escenarios incompletos
"""
from quality_scenarios_db import QUALITY_SCENARIOS_DB

def validate_database():
    print("🔍 VALIDANDO BASE DE DATOS")
    print("="*60)
    
    required_fields = ["description", "options", "correctOption", "explanation"]
    languages = ["es", "en"]
    
    total_scenarios = len(QUALITY_SCENARIOS_DB)
    print(f"📊 Total scenarios to validate: {total_scenarios}")
    
    errors = []
    
    for i, scenario in enumerate(QUALITY_SCENARIOS_DB):
        scenario_errors = []
        
        for lang in languages:
            if lang not in scenario:
                scenario_errors.append(f"Missing language '{lang}'")
                continue
                
            lang_data = scenario[lang]
            
            for field in required_fields:
                if field not in lang_data:
                    scenario_errors.append(f"Missing field '{field}' in {lang}")
                elif field == "options" and not isinstance(lang_data[field], dict):
                    scenario_errors.append(f"Field 'options' is not a dict in {lang}")
                elif field == "options" and len(lang_data[field]) < 4:
                    scenario_errors.append(f"Field 'options' has less than 4 options in {lang}")
        
        if scenario_errors:
            errors.append({
                "index": i,
                "preview": str(scenario)[:100] + "...",
                "errors": scenario_errors
            })
    
    if errors:
        print(f"❌ Found {len(errors)} problematic scenarios:")
        for error in errors:
            print(f"\n🚨 Scenario {error['index']}:")
            print(f"   Preview: {error['preview']}")
            for err in error['errors']:
                print(f"   - {err}")
    else:
        print("✅ All scenarios are valid!")
    
    return len(errors) == 0

if __name__ == "__main__":
    validate_database()