#!/usr/bin/env python3
"""
Analizador de base de datos - identifica escenarios incompletos
"""
from quality_scenarios_db import QUALITY_SCENARIOS_DB

def analyze_database():
    print("🔍 ANÁLISIS COMPLETO DE LA BASE DE DATOS")
    print("="*60)
    
    total = len(QUALITY_SCENARIOS_DB)
    print(f"📊 Total de escenarios: {total}")
    
    complete_scenarios = []
    incomplete_scenarios = []
    
    for i, scenario in enumerate(QUALITY_SCENARIOS_DB):
        scenario_info = {"index": i, "languages": {}}
        
        for lang in ["es", "en"]:
            if lang in scenario:
                data = scenario[lang]
                has_description = "description" in data
                has_options = "options" in data
                has_correct = "correctOption" in data
                has_explanation = "explanation" in data
                
                scenario_info["languages"][lang] = {
                    "description": has_description,
                    "options": has_options,
                    "correctOption": has_correct,
                    "explanation": has_explanation,
                    "complete": has_description and has_options and has_correct and has_explanation
                }
            else:
                scenario_info["languages"][lang] = {"missing": True}
        
        # Determinar si el escenario está completo
        es_complete = scenario_info["languages"]["es"].get("complete", False)
        en_complete = scenario_info["languages"]["en"].get("complete", False)
        
        if es_complete and en_complete:
            complete_scenarios.append(i)
        else:
            incomplete_scenarios.append((i, scenario_info))
    
    print(f"✅ Escenarios completos: {len(complete_scenarios)}")
    print(f"❌ Escenarios incompletos: {len(incomplete_scenarios)}")
    
    if incomplete_scenarios:
        print("\n🚨 ESCENARIOS INCOMPLETOS:")
        for idx, info in incomplete_scenarios[:10]:  # Solo mostrar los primeros 10
            scenario = QUALITY_SCENARIOS_DB[idx]
            print(f"\n📍 Escenario {idx}:")
            
            for lang in ["es", "en"]:
                if lang in scenario:
                    data = scenario[lang]
                    desc = data.get("description", "NO DESCRIPTION")[:60] + "..."
                    print(f"   {lang.upper()}: {desc}")
                    
                    missing = []
                    if "description" not in data: missing.append("description")
                    if "options" not in data: missing.append("options") 
                    if "correctOption" not in data: missing.append("correctOption")
                    if "explanation" not in data: missing.append("explanation")
                    
                    if missing:
                        print(f"        ❌ Faltan: {', '.join(missing)}")
                    else:
                        print(f"        ✅ Completo")
                else:
                    print(f"   {lang.upper()}: ❌ IDIOMA FALTANTE")
    
    return complete_scenarios, incomplete_scenarios

if __name__ == "__main__":
    complete, incomplete = analyze_database()
    
    print(f"\n📋 RESUMEN:")
    print(f"   Completos: {len(complete)}/{len(QUALITY_SCENARIOS_DB)}")
    print(f"   Incompletos: {len(incomplete)}/{len(QUALITY_SCENARIOS_DB)}")
    print(f"   Porcentaje completo: {len(complete)/len(QUALITY_SCENARIOS_DB)*100:.1f}%")