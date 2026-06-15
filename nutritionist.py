"""
nutritionist.py
Hybrid Nutritionist Class with Detailed Meal Plans
"""
import joblib
import os

class HybridNutritionist:
    """AI-powered nutritionist for personalized diet plans"""
    
    def __init__(self, model_path='best_model.pkl'):
        """Initialize with trained model"""
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
            print(" Model loaded successfully")
        else:
            raise FileNotFoundError(f"Model not found at {model_path}")
        
        # Activity multipliers
        self.activity_multipliers = {
            1: 1.2,   # Sedentary
            2: 1.375, # Light activity
            3: 1.55,  # Moderate activity
            4: 1.725, # Very active
            5: 1.9    # Extra active
        }
        
        # Goal adjustments (calories)
        self.goal_adjustments = {
            'weight loss': -500,
            'maintain': 0,
            'weight gain': 500
        }
        
        # Detailed Meal Plans with complete food items
        self.meal_plans = {
            'light': {
                'Breakfast': {
                    'items': [
                        'Oatmeal (1 bowl) - made with water or low-fat milk',
                        'Mixed berries (1/2 cup) - strawberry, blueberry',
                        '1 teaspoon honey (optional)',
                        'Green tea (1 cup)'
                    ],
                    'calories': '250-300 kcal'
                },
                'Morning Snack': {
                    'items': [
                        '1 Apple OR 1 Banana',
                        '5-6 almonds (soaked overnight)'
                    ],
                    'calories': '100-120 kcal'
                },
                'Lunch': {
                    'items': [
                        'Grilled chicken breast (100g) OR Paneer (100g for veg)',
                        'Large green salad - lettuce, cucumber, tomato, bell peppers',
                        '1 teaspoon olive oil dressing',
                        'Lemon water'
                    ],
                    'calories': '350-400 kcal'
                },
                'Evening Snack': {
                    'items': [
                        '1 cup green tea',
                        '2-3 whole grain crackers',
                        'OR 1 small orange'
                    ],
                    'calories': '80-100 kcal'
                },
                'Dinner': {
                    'items': [
                        'Vegetable soup (1 bowl) - tomato, carrot, broccoli',
                        'Steamed vegetables (1 cup) - broccoli, cauliflower, carrot',
                        '1 slice whole grain bread (optional)'
                    ],
                    'calories': '300-350 kcal'
                },
                'total_calories': '~1100-1300 kcal'
            },
            
            'balanced': {
                'Breakfast': {
                    'items': [
                        'Smoothie bowl - blended banana, spinach, protein powder',
                        'Topped with: 2 tbsp granola, 5-6 walnuts, chia seeds',
                        'OR 2 eggs with 1 slice whole grain toast',
                        '1 cup milk (low-fat)'
                    ],
                    'calories': '400-450 kcal'
                },
                'Morning Snack': {
                    'items': [
                        'Greek yogurt (150g)',
                        '1 tablespoon mixed seeds (pumpkin, sunflower, flax)',
                        'Handful of berries'
                    ],
                    'calories': '180-200 kcal'
                },
                'Lunch': {
                    'items': [
                        '2 whole wheat rotis/chapatis',
                        '1 bowl dal (lentil curry) - 150g',
                        '1 bowl mixed vegetable sabzi (150g)',
                        '1 bowl salad - cucumber, tomato, onion',
                        '1/2 bowl brown rice (optional)'
                    ],
                    'calories': '550-600 kcal'
                },
                'Evening Snack': {
                    'items': [
                        'Handful of mixed nuts (7-8 almonds, 2 walnuts)',
                        '1 fruit - apple or pear',
                        'Buttermilk (1 glass)'
                    ],
                    'calories': '200-250 kcal'
                },
                'Dinner': {
                    'items': [
                        'Grilled fish (150g) OR Tofu (150g for veg)',
                        '1 cup quinoa OR brown rice',
                        'Steamed broccoli and zucchini (1 cup)',
                        'Lemon herb dressing'
                    ],
                    'calories': '500-550 kcal'
                },
                'total_calories': '~1850-2050 kcal'
            },
            
            'heavy': {
                'Breakfast': {
                    'items': [
                        '3 egg omelette with spinach and mushroom',
                        '2 slices whole grain toast with avocado',
                        '1 glass full fat milk',
                        '5-6 almonds and 2 walnuts'
                    ],
                    'calories': '600-650 kcal'
                },
                'Morning Snack': {
                    'items': [
                        'Peanut butter sandwich (2 slices bread, 2 tbsp peanut butter)',
                        '1 banana',
                        'Protein shake (1 scoop)'
                    ],
                    'calories': '350-400 kcal'
                },
                'Lunch': {
                    'items': [
                        'Chicken biryani (1 full plate) - 250g chicken, 2 cup rice',
                        'Raita (1 bowl) - yogurt with cucumber',
                        'Salad - onion, tomato, cucumber',
                        'Egg curry (1 egg)'
                    ],
                    'calories': '700-800 kcal'
                },
                'Evening Snack': {
                    'items': [
                        'Protein smoothie - banana, peanut butter, protein powder',
                        'Dates (3-4 pieces)',
                        'Handful of nuts (10-12 almonds, 4-5 walnuts)'
                    ],
                    'calories': '400-450 kcal'
                },
                'Dinner': {
                    'items': [
                        'Paneer tikka (200g) OR Chicken tikka (200g)',
                        '2 multigrain rotis',
                        'Dal makhani (1 bowl)',
                        'Mix vegetable curry (1 bowl)',
                        'Brown rice (1/2 cup)'
                    ],
                    'calories': '650-750 kcal'
                },
                'total_calories': '~2750-3100 kcal'
            }
        }
        
        # Skin-specific advice
        self.skin_tips = {
            'acne': {
                'avoid': ['Dairy products', 'Sugary foods', 'Fried foods', 'Processed snacks', 'White bread'],
                'tips': [
                    'Drink 3-4 liters water daily',
                    'Wash face twice daily with mild cleanser',
                    'Include zinc-rich foods: pumpkin seeds, chickpeas',
                    'Avoid touching face',
                    'Change pillow cover weekly'
                ],
                'foods': ['Green tea', 'Turmeric', 'Berries', 'Spinach', 'Lentils', 'Pumpkin seeds']
            },
            'dryness': {
                'avoid': ['Caffeine', 'Alcohol', 'Salty foods', 'Sugary drinks', 'Processed food'],
                'tips': [
                    'Apply moisturizer immediately after bath',
                    'Use humidifier at home',
                    'Take omega-3 supplements',
                    'Avoid long hot showers',
                    'Use gentle soap-free cleanser'
                ],
                'foods': ['Avocado', 'Walnuts', 'Flaxseeds', 'Olive oil', 'Fatty fish', 'Coconut oil']
            },
            'glow': {
                'avoid': ['Sugar', 'Trans fats', 'Excess dairy', 'Packaged foods', 'Maida products'],
                'tips': [
                    'Get 7-8 hours of sleep daily',
                    'Exercise for 30 minutes daily',
                    'Apply sunscreen daily',
                    'Exfoliate once a week',
                    'Reduce stress with meditation'
                ],
                'foods': ['Amla (Indian gooseberry)', 'Oranges', 'Bell peppers', 'Kiwi', 'Tomatoes', 'Papaya']
            },
            'none': {
                'avoid': ['Junk food', 'Sugary beverages', 'Excess salt'],
                'tips': [
                    'Maintain balanced diet',
                    'Exercise 5 days a week',
                    'Stay hydrated',
                    'Get regular health checkup'
                ],
                'foods': ['All fruits', 'All vegetables', 'Whole grains', 'Lean proteins']
            }
        }
    
    def calculate_bmr(self, weight, height, age, gender):
        """Calculate BMR using Mifflin-St Jeor formula"""
        if gender.lower() == 'male':
            return (10 * weight) + (6.25 * height) - (5 * age) + 5
        else:
            return (10 * weight) + (6.25 * height) - (5 * age) - 161
    
    def calculate_tdee(self, bmr, activity_level):
        """Calculate Total Daily Energy Expenditure"""
        return bmr * self.activity_multipliers[activity_level]
    
    def get_calorie_target(self, tdee, goal):
        """Adjust calories based on goal"""
        return tdee + self.goal_adjustments[goal]
    
    def get_meal_plan(self, calories):
        """Get detailed meal plan based on calorie target"""
        if calories < 1600:
            return self.meal_plans['light'], 'Light (Weight Loss)'
        elif calories <= 2500:
            return self.meal_plans['balanced'], 'Balanced (Maintenance)'
        else:
            return self.meal_plans['heavy'], 'Heavy (Weight Gain)'
    
    def generate_plan(self, age, gender, weight, height, activity_level, goal, skin_concern):
        """Generate complete personalized diet plan"""
        
        # Validate inputs
        if weight <= 0 or height <= 0 or age <= 0:
            raise ValueError("Weight, height, and age must be positive")
        
        if activity_level not in range(1, 6):
            raise ValueError("Activity level must be between 1 and 5")
        
        # Calculate
        bmr = self.calculate_bmr(weight, height, age, gender)
        tdee = self.calculate_tdee(bmr, activity_level)
        calorie_target = self.get_calorie_target(tdee, goal)
        meal_plan, meal_type = self.get_meal_plan(calorie_target)
        
        # Get skin advice
        skin_data = self.skin_tips.get(skin_concern.lower(), self.skin_tips['none'])
        
        # Format meal plan for display
        formatted_meal_plan = {}
        for meal, details in meal_plan.items():
            if isinstance(details, dict) and 'items' in details:
                formatted_meal_plan[meal] = {
                    'items': details['items'],
                    'calories': details.get('calories', '')
                }
            else:
                formatted_meal_plan[meal] = details
        
        return {
            'bmr': round(bmr),
            'tdee': round(tdee),
            'calorie_target': round(calorie_target),
            'meal_type': meal_type,
            'meal_plan': formatted_meal_plan,
            'total_calories': meal_plan.get('total_calories', ''),
            'avoid_foods': skin_data['avoid'],
            'tips': skin_data['tips'],
            'recommended_foods': skin_data['foods']
        }


def generate_report(plan, user_info):
    """Generate detailed text report with complete food items"""
    report = []
    report.append("="*70)
    report.append("AI NUTRITIONIST - PERSONALIZED DIET REPORT")
    report.append("="*70)
    report.append("")
    
    report.append("USER PROFILE")
    report.append("-"*50)
    report.append(f"Name: {user_info.get('name', 'User')}")
    report.append(f"Age: {user_info['age']} years")
    report.append(f"Gender: {user_info['gender'].capitalize()}")
    report.append(f"Weight: {user_info['weight']} kg")
    report.append(f"Height: {user_info['height']} cm")
    report.append(f"Goal: {user_info['goal'].capitalize()}")
    report.append("")
    
    report.append("CALORIE CALCULATIONS")
    report.append("-"*50)
    report.append(f"BMR (Basal Metabolic Rate): {plan['bmr']} calories/day")
    report.append(f"TDEE (Total Daily Energy): {plan['tdee']} calories/day")
    report.append(f"Daily Calorie Target: {plan['calorie_target']} calories/day")
    report.append(f"Meal Type: {plan['meal_type']}")
    report.append("")
    
    report.append("="*70)
    report.append("COMPLETE MEAL PLAN WITH FOOD ITEMS")
    report.append("="*70)
    report.append("")
    
    # Detailed meal plan
    for meal_name, meal_data in plan['meal_plan'].items():
        if meal_name == 'total_calories':
            continue
            
        report.append(f"\n{'='*50}")
        report.append(f"{meal_name.upper()}")
        report.append(f"{'='*50}")
        
        if isinstance(meal_data, dict):
            if 'items' in meal_data:
                for i, item in enumerate(meal_data['items'], 1):
                    report.append(f"  {i}. {item}")
            if 'calories' in meal_data and meal_data['calories']:
                report.append(f"\n  Calories: {meal_data['calories']}")
        else:
            report.append(f"  {meal_data}")
    
    report.append(f"\n{'='*50}")
    report.append(f"TOTAL DAILY CALORIES: {plan.get('total_calories', 'Calculate as per portions')}")
    report.append(f"{'='*50}")
    report.append("")
    
    report.append("FOODS TO AVOID")
    report.append("-"*50)
    for food in plan['avoid_foods']:
        report.append(f"  X {food}")
    report.append("")
    
    report.append("RECOMMENDED FOODS FOR SKIN HEALTH")
    report.append("-"*50)
    for food in plan['recommended_foods']:
        report.append(f"  ✓ {food}")
    report.append("")
    
    report.append("HEALTH & SKIN TIPS")
    report.append("-"*50)
    for i, tip in enumerate(plan['tips'], 1):
        report.append(f"  {i}. {tip}")
    report.append("")
    
    report.append("ADDITIONAL GUIDELINES")
    report.append("-"*50)
    report.append("  1. Drink 8-10 glasses of water throughout the day")
    report.append("  2. Eat slowly and chew food properly")
    report.append("  3. Don't skip meals - eat every 3-4 hours")
    report.append("  4. Stop eating 2-3 hours before sleeping")
    report.append("  5. Include physical activity for 30 minutes daily")
    report.append("")
    
    report.append("="*70)
    report.append("Report generated by AI Nutritionist System")
    report.append("For best results, follow this plan consistently for 4 weeks")
    report.append("="*70)
    
    return "\n".join(report)