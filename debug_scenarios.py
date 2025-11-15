#!/usr/bin/env python3
"""
Test simple para verificar que la función funciona
"""
from quality_scenarios_db import get_random_scenarios

print("🧪 TESTING get_random_scenarios function")
print("="*50)

# Test simple
scenarios = get_random_scenarios(3, language="es")

print(f"\nGot {len(scenarios)} scenarios:")
for i, s in enumerate(scenarios, 1):
    print(f"\n{i}. ID: {s['id']}")
    print(f"   Content: {s['content'][:50]}...")
    print(f"   Options: {s['options']}")
    print(f"   Correct: {s['correctOption']}")

print("\n✅ Test completed!")