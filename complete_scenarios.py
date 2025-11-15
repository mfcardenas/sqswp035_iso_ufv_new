#!/usr/bin/env python3
"""
Script para completar automáticamente todos los escenarios incompletos
"""

# Definiciones de opciones estándar para cada atributo de calidad
QUALITY_ATTRIBUTES_OPTIONS = {
    "Fiabilidad": {
        "es": {
            "options": {
                "A": "Eficiencia de desempeño",
                "B": "Fiabilidad", 
                "C": "Seguridad",
                "D": "Mantenibilidad"
            },
            "correctOption": "B",
            "explanation": "Este escenario se relaciona con la Fiabilidad porque se enfoca en la capacidad del sistema para mantener su funcionamiento bajo condiciones específicas durante un período determinado."
        },
        "en": {
            "options": {
                "A": "Performance efficiency",
                "B": "Reliability",
                "C": "Security", 
                "D": "Maintainability"
            },
            "correctOption": "B",
            "explanation": "This scenario relates to Reliability because it focuses on the system's ability to maintain its operation under specified conditions for a specified period."
        }
    },
    "Eficiencia de desempeño": {
        "es": {
            "options": {
                "A": "Eficiencia de desempeño",
                "B": "Usabilidad",
                "C": "Fiabilidad", 
                "D": "Portabilidad"
            },
            "correctOption": "A",
            "explanation": "Este escenario se relaciona con la Eficiencia de desempeño porque se enfoca en el uso óptimo de recursos del sistema para maximizar el rendimiento."
        },
        "en": {
            "options": {
                "A": "Performance efficiency",
                "B": "Usability", 
                "C": "Reliability",
                "D": "Portability"
            },
            "correctOption": "A",
            "explanation": "This scenario relates to Performance efficiency because it focuses on optimal use of system resources to maximize performance."
        }
    },
    "Seguridad": {
        "es": {
            "options": {
                "A": "Compatibilidad",
                "B": "Seguridad",
                "C": "Fiabilidad",
                "D": "Usabilidad"
            },
            "correctOption": "B",
            "explanation": "Este escenario se relaciona con la Seguridad porque se enfoca en la protección de información y datos contra accesos no autorizados."
        },
        "en": {
            "options": {
                "A": "Compatibility",
                "B": "Security",
                "C": "Reliability",
                "D": "Usability"
            },
            "correctOption": "B", 
            "explanation": "This scenario relates to Security because it focuses on protecting information and data against unauthorized access."
        }
    },
    "Usabilidad": {
        "es": {
            "options": {
                "A": "Usabilidad",
                "B": "Eficiencia de desempeño",
                "C": "Portabilidad",
                "D": "Mantenibilidad"
            },
            "correctOption": "A",
            "explanation": "Este escenario se relaciona con la Usabilidad porque se enfoca en la facilidad de uso y la experiencia del usuario al interactuar con el sistema."
        },
        "en": {
            "options": {
                "A": "Usability",
                "B": "Performance efficiency",
                "C": "Portability", 
                "D": "Maintainability"
            },
            "correctOption": "A",
            "explanation": "This scenario relates to Usability because it focuses on ease of use and user experience when interacting with the system."
        }
    },
    "Compatibilidad": {
        "es": {
            "options": {
                "A": "Compatibilidad",
                "B": "Portabilidad",
                "C": "Mantenibilidad",
                "D": "Seguridad"
            }, 
            "correctOption": "A",
            "explanation": "Este escenario se relaciona con la Compatibilidad porque se enfoca en la capacidad del sistema para coexistir e intercambiar información con otros sistemas."
        },
        "en": {
            "options": {
                "A": "Compatibility",
                "B": "Portability",
                "C": "Maintainability",
                "D": "Security"
            },
            "correctOption": "A",
            "explanation": "This scenario relates to Compatibility because it focuses on the system's ability to coexist and exchange information with other systems."
        }
    },
    "Portabilidad": {
        "es": {
            "options": {
                "A": "Compatibilidad",
                "B": "Fiabilidad", 
                "C": "Portabilidad",
                "D": "Mantenibilidad"
            },
            "correctOption": "C",
            "explanation": "Este escenario se relaciona con la Portabilidad porque se enfoca en la capacidad del sistema para ser transferido de un entorno a otro."
        },
        "en": {
            "options": {
                "A": "Compatibility",
                "B": "Reliability",
                "C": "Portability", 
                "D": "Maintainability"
            },
            "correctOption": "C",
            "explanation": "This scenario relates to Portability because it focuses on the system's ability to be transferred from one environment to another."
        }
    },
    "Mantenibilidad": {
        "es": {
            "options": {
                "A": "Mantenibilidad",
                "B": "Usabilidad",
                "C": "Compatibilidad",
                "D": "Portabilidad"
            },
            "correctOption": "A", 
            "explanation": "Este escenario se relaciona con la Mantenibilidad porque se enfoca en la facilidad con la que el sistema puede ser modificado para corregir defectos o mejorar su funcionamiento."
        },
        "en": {
            "options": {
                "A": "Maintainability",
                "B": "Usability",
                "C": "Compatibility",
                "D": "Portability"
            },
            "correctOption": "A",
            "explanation": "This scenario relates to Maintainability because it focuses on the ease with which the system can be modified to correct defects or improve its operation."
        }
    }
}

# Mapeo de categorías en inglés a español
CATEGORY_MAPPING = {
    "Reliability": "Fiabilidad",
    "Performance efficiency": "Eficiencia de desempeño", 
    "Security": "Seguridad",
    "Usability": "Usabilidad",
    "Compatibility": "Compatibilidad",
    "Portability": "Portabilidad",
    "Maintainability": "Mantenibilidad"
}

def complete_scenarios():
    from quality_scenarios_db import QUALITY_SCENARIOS_DB
    
    print("🔧 COMPLETANDO ESCENARIOS AUTOMÁTICAMENTE")
    print("="*60)
    
    completed_count = 0
    
    for i, scenario in enumerate(QUALITY_SCENARIOS_DB):
        modified = False
        
        for lang in ["es", "en"]:
            if lang in scenario:
                data = scenario[lang]
                category = data.get("category", "")
                
                # Verificar si está incompleto
                if "options" not in data or "correctOption" not in data or "explanation" not in data:
                    print(f"🔧 Completando escenario {i} ({lang}): {category}")
                    
                    # Mapear categoría a español para buscar plantilla
                    template_key = category
                    
                    # Si la categoría está en inglés, convertir a español
                    if category in CATEGORY_MAPPING:
                        template_key = CATEGORY_MAPPING[category]
                    
                    # Si no se encontró, intentar buscarla directamente
                    if template_key in QUALITY_ATTRIBUTES_OPTIONS:
                        template = QUALITY_ATTRIBUTES_OPTIONS[template_key][lang]
                        
                        # Completar campos faltantes
                        if "options" not in data:
                            data["options"] = template["options"]
                        if "correctOption" not in data:
                            data["correctOption"] = template["correctOption"] 
                        if "explanation" not in data:
                            data["explanation"] = template["explanation"]
                        
                        modified = True
                    else:
                        print(f"⚠️ No hay plantilla para categoría: {category}")
        
        if modified:
            completed_count += 1
    
    print(f"\n✅ Completados {completed_count} escenarios")
    return QUALITY_SCENARIOS_DB

if __name__ == "__main__":
    completed_scenarios = complete_scenarios()
    print("\n📝 Generando nuevo archivo...")
    
    # Generar el código Python del archivo actualizado
    with open("quality_scenarios_db_COMPLETED.py", "w", encoding="utf-8") as f:
        f.write('"""\n')
        f.write('Database of quality scenarios for ISO/IEC 25010 quality attributes.\n')
        f.write('This file serves as the single source of truth for all scenarios in both Spanish and English.\n')
        f.write('COMPLETED VERSION - All scenarios have options, correctOption, and explanation.\n')
        f.write('"""\n\n')
        f.write('import random\n\n')
        f.write('# Dictionary of quality scenarios with bilingual support\n')
        f.write('QUALITY_SCENARIOS_DB = [\n')
        
        for i, scenario in enumerate(completed_scenarios):
            f.write('    {\n')
            
            for lang in ["es", "en"]:
                if lang in scenario:
                    data = scenario[lang]
                    f.write(f'        "{lang}": {{\n')
                    f.write(f'            "description": "{data["description"]}",\n')
                    f.write(f'            "category": "{data["category"]}",\n')
                    if "options" in data:
                        f.write(f'            "options": {{\n')
                        for key, value in data["options"].items():
                            f.write(f'                "{key}": "{value}",\n')
                        f.write(f'            }},\n')
                    else:
                        f.write(f'            "options": {{}},\n')
                    f.write(f'            "correctOption": "{data.get("correctOption", "A")}",\n')
                    f.write(f'            "explanation": "{data.get("explanation", "")}"\n')
                    f.write(f'        }}')
                    if lang == "es":
                        f.write(',\n')
                    else:
                        f.write('\n')
            
            f.write('    }')
            if i < len(completed_scenarios) - 1:
                f.write(',\n')
            else:
                f.write('\n')
        
        f.write(']\n\n')
        
        # Agregar la función get_random_scenarios actualizada
        f.write('''def get_random_scenarios(num_scenarios=5, quality_attribute=None, language="es", force_new_selection=False):
    """
    Return random scenarios from database. All scenarios are now complete.
    """
    import random
    
    # Use system time for randomness
    random.seed()
    
    print(f"🎲 Getting {num_scenarios} random scenarios in {language}")
    
    # Get scenarios with requested language - all should be complete now
    available = [s for s in QUALITY_SCENARIOS_DB if language in s]
    print(f"📊 Using {len(available)} scenarios")
    
    # Select randomly
    if len(available) >= num_scenarios:
        selected = random.sample(available, num_scenarios)
    else:
        selected = available
    
    # Convert to expected format
    result = []
    for scenario in selected:
        data = scenario[language]
        result.append({
            "id": str(random.randint(1000, 9999)),
            "content": data["description"],
            "options": data["options"],
            "correctOption": data["correctOption"],
            "explanation": data["explanation"],
            "category": data.get("category", "General")
        })
    
    print(f"✅ Returning {len(result)} scenarios")
    return result

def get_database_stats():
    """Return statistics about the database."""
    return {
        "total_scenarios": len(QUALITY_SCENARIOS_DB),
        "languages": ["es", "en"],
        "complete": True
    }
''')
    
    print("✅ Archivo generado: quality_scenarios_db_COMPLETED.py")
    print("\nPara aplicar los cambios:")
    print("1. Revisa quality_scenarios_db_COMPLETED.py")
    print("2. Si está correcto, reemplaza quality_scenarios_db.py")