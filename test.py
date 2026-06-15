"""
test.py - Test the nutritionist system
"""
from nutritionist import HybridNutritionist, generate_report

def test():
    print("="*60)
    print("TESTING AI NUTRITIONIST")
    print("="*60)
    
    # Create nutritionist
    nutritionist = HybridNutritionist('best_model.pkl')
    
    # Test case 1
    print("\nTest Case 1: Male, Weight Loss, Acne")
    plan = nutritionist.generate_plan(
        age=30,
        gender='male',
        weight=80,
        height=175,
        activity_level=3,
        goal='weight loss',
        skin_concern='acne'
    )
    
    print(f"Calorie Target: {plan['calorie_target']} kcal/day")
    print(f"Meal Type: {plan['meal_type']}")
    
    # Generate report
    user_info = {
        'name': 'John',
        'age': 30,
        'gender': 'male',
        'weight': 80,
        'height': 175,
        'goal': 'weight loss'
    }
    
    report = generate_report(plan, user_info)
    print("\n" + report[:500] + "...")
    
    print("\n✅ Test passed!")

if __name__ == "__main__":
    test()