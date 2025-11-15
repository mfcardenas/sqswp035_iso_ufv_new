from quality_scenarios_db import get_random_scenarios

print("🧪 SIMPLE TEST: Getting scenarios 5 times to see if they change...")
print("="*60)

for i in range(5):
    print(f"\n🎲 Call {i+1}:")
    scenarios = get_random_scenarios(num_scenarios=3, language="es")
    
    for j, scenario in enumerate(scenarios, 1):
        print(f"   {j}. {scenario['content'][:50]}...")
        print(f"      ID: {scenario['id']}")

print("\n✅ If you see different scenarios above, randomization is working!")

# Prueba de consistencia de opciones para el mismo escenario
print("\n=== PRUEBA DE CONSISTENCIA DE OPCIONES ===")
print("Verificando que las opciones del mismo escenario sean consistentes:")

# Obtener el primer escenario varias veces
first_run = get_random_scenarios(1, language='es')
first_scenario_content = first_run[0]['content']

# Buscar el mismo escenario en múltiples ejecuciones
same_scenario_options = []
for attempt in range(10):  # Intentar 10 veces
    scenarios = get_random_scenarios(5, language='es')
    for scenario in scenarios:
        if scenario['content'] == first_scenario_content:
            same_scenario_options.append(scenario['options'])
            break

if len(same_scenario_options) >= 2:
    print(f"Encontrado el mismo escenario {len(same_scenario_options)} veces:")
    print(f"Escenario: {first_scenario_content[:50]}...")
    all_same = all(opts == same_scenario_options[0] for opts in same_scenario_options)
    print(f"Opciones consistentes: {'✅ SÍ' if all_same else '❌ NO'}")
    if not all_same:
        for i, opts in enumerate(same_scenario_options):
            print(f"  Intento {i + 1}: {opts}")
else:
    print("No se pudo encontrar el mismo escenario múltiples veces para verificar consistencia")

print("\n=== PRUEBA DE FILTRADO POR ATRIBUTO ===")
print("Escenarios de Seguridad:")
security_scenarios = get_random_scenarios(2, quality_attribute="Seguridad", language='es')
for i, scenario in enumerate(security_scenarios, 1):
    print(f"{i}. {scenario['category']} - {scenario['content'][:40]}...")
    print(f"   Respuesta correcta: {scenario['correctOption']}")