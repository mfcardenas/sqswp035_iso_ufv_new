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