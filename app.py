"""
AI Nutritionist - Professional Streamlit Application
Version: 2.0.0 - Fully Fixed
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Import custom modules
from nutritionist import HybridNutritionist, generate_report

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="AI Nutritionist Pro",
    page_icon="🥗",
    layout="wide"
)

# ============================================================================
# CUSTOM CSS
# ============================================================================

st.markdown("""
<style>
    /* Header */
    .main-header {
        background: linear-gradient(135deg, #1a472a 0%, #2d5a3b 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
    }
    .main-header p {
        color: rgba(255,255,255,0.9);
        margin: 0.5rem 0 0 0;
    }
    
    /* Cards */
    .metric-card {
        background: white;
        padding: 1.2rem;
        border-radius: 15px;
        text-align: center;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2d5a3b;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #666;
        margin-top: 0.3rem;
    }
    
    /* Meal cards */
    .meal-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        border-left: 4px solid;
    }
    .meal-title {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .food-item {
        padding: 0.2rem 0;
        color: #555;
        font-size: 0.9rem;
    }
    
    /* Sidebar */
    .sidebar-nav {
        padding: 0.5rem 0;
    }
    .nav-item {
        padding: 0.7rem 1rem;
        margin: 0.2rem 0;
        border-radius: 10px;
        cursor: pointer;
        font-size: 1rem;
    }
    .nav-item:hover {
        background: #e8f5e9;
    }
    .nav-active {
        background: #2d5a3b;
        color: white;
    }
    
    /* Success box */
    .success-box {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #666;
        border-top: 1px solid #e0e0e0;
        margin-top: 3rem;
    }
    
    /* Button */
    .stButton > button {
        background: linear-gradient(135deg, #2d5a3b 0%, #1a472a 100%);
        color: white;
        border: none;
        padding: 0.7rem;
        font-weight: 600;
        border-radius: 10px;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SIMPLE SIDEBAR NAVIGATION
# ============================================================================

with st.sidebar:
    st.markdown("## 🥗 AI Nutritionist")
    st.markdown("---")
    
    # Simple radio buttons for navigation
    page = st.radio(
        "📌 MENU",
        ["🏠 Dashboard", "🍽️ Meal Planner", "💡 Health Tips", "ℹ️ About"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 📊 Quick Stats")
    st.markdown("- 5000+ Meal Plans")
    st.markdown("- 2000+ Food Items")
    st.markdown("- 98% Accuracy")
    st.markdown("- AI Powered")
    
    st.markdown("---")
    st.markdown("### 🎯 Today's Tip")
    st.info("Drink 8 glasses of water daily for better metabolism!")

# ============================================================================
# LOAD MODEL
# ============================================================================

@st.cache_resource
def load_nutritionist():
    try:
        return HybridNutritionist('best_model.pkl')
    except Exception as e:
        st.error(f"❌ Model loading failed: {e}")
        st.info("Run `python train_model.py` first")
        return None

nutritionist = load_nutritionist()

# ============================================================================
# PAGE: DASHBOARD
# ============================================================================

if page == "🏠 Dashboard":
    st.markdown("""
    <div class="main-header">
        <h1>🥗 AI Nutritionist Pro</h1>
        <p>Your Personal AI-Powered Diet Planning Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    if nutritionist:
        # Input Form
        st.markdown("### 📝 Personal Information")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            name = st.text_input("Your Name", "Guest")
            age = st.number_input("Age (years)", 18, 100, 30)
        
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female"])
            weight = st.number_input("Weight (kg)", 30.0, 200.0, 70.0)
        
        with col3:
            height = st.number_input("Height (cm)", 100.0, 250.0, 170.0)
            bmi = weight / ((height/100) ** 2)
            st.info(f"📊 BMI: {bmi:.1f}")
        
        st.markdown("---")
        st.markdown("### 🎯 Goals")
        
        col1, col2 = st.columns(2)
        
        with col1:
            activity_level = st.select_slider(
                "Activity Level",
                options=[1, 2, 3, 4, 5],
                value=3,
                format_func=lambda x: ["🪑 Sedentary", "🚶 Light", "🏃 Moderate", "💪 Very Active", "⚡ Extra Active"][x-1]
            )
            goal = st.selectbox("Fitness Goal", ["weight loss", "maintain", "weight gain"])
        
        with col2:
            skin_concern = st.selectbox("Skin Concern", ["none", "acne", "dryness", "glow"])
            diet_type = st.selectbox("Diet Preference", ["Non-Veg", "Vegetarian", "Vegan"])
        
        st.markdown("---")
        
        # Generate Button
        if st.button("🚀 GENERATE DIET PLAN", use_container_width=True):
            with st.spinner("Creating your personalized plan..."):
                try:
                    plan = nutritionist.generate_plan(
                        age=age,
                        gender=gender.lower(),
                        weight=weight,
                        height=height,
                        activity_level=activity_level,
                        goal=goal,
                        skin_concern=skin_concern
                    )
                    
                    st.session_state['plan'] = plan
                    st.session_state['user_info'] = {
                        'name': name, 'age': age, 'gender': gender,
                        'weight': weight, 'height': height, 'goal': goal
                    }
                    
                    # Success
                    st.markdown(f'<div class="success-box">✅ Diet plan ready for {name}!</div>', unsafe_allow_html=True)
                    
                    # Metrics
                    st.markdown("### 📊 Calorie Analysis")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.markdown(f'<div class="metric-card"><div class="metric-value">{plan["bmr"]}</div><div class="metric-label">BMR (kcal/day)</div></div>', unsafe_allow_html=True)
                    with col2:
                        st.markdown(f'<div class="metric-card"><div class="metric-value">{plan["tdee"]}</div><div class="metric-label">TDEE (kcal/day)</div></div>', unsafe_allow_html=True)
                    with col3:
                        st.markdown(f'<div class="metric-card"><div class="metric-value">{plan["calorie_target"]}</div><div class="metric-label">Daily Target</div></div>', unsafe_allow_html=True)
                    with col4:
                        surplus = plan["calorie_target"] - plan["tdee"]
                        sign = "+" if surplus > 0 else ""
                        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color: {"#2e7d32" if surplus >= 0 else "#d32f2f"}">{sign}{surplus}</div><div class="metric-label">{"Surplus" if surplus > 0 else "Deficit" if surplus < 0 else "Maintain"}</div></div>', unsafe_allow_html=True)
                    
                    # Macronutrients
                    st.markdown("### 📈 Macronutrients")
                    
                    p_cal = plan["calorie_target"] * 0.3
                    c_cal = plan["calorie_target"] * 0.4
                    f_cal = plan["calorie_target"] * 0.3
                    
                    macro_df = pd.DataFrame({
                        'Nutrient': ['Protein', 'Carbs', 'Fats'],
                        'Calories': [p_cal, c_cal, f_cal],
                        'Percent': [30, 40, 30],
                        'Grams': [p_cal/4, c_cal/4, f_cal/9]
                    })
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        fig = px.pie(macro_df, values='Percent', names='Nutrient', 
                                     title='Calorie Distribution', hole=0.4,
                                     color_discrete_sequence=['#2d5a3b', '#4caf50', '#8bc34a'])
                        fig.update_layout(height=350, plot_bgcolor='white')
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        for _, row in macro_df.iterrows():
                            st.markdown(f"""
                            <div style="margin-bottom: 1rem;">
                                <strong>{row['Nutrient']}</strong><br>
                                <span style="color:#2d5a3b; font-size:1.2rem;">{row['Grams']:.0f}g</span>
                                <span style="color:#666;"> ({row['Percent']:.0f}%)</span>
                                <div style="background:#e0e0e0; height:6px; border-radius:3px; margin-top:4px;">
                                    <div style="background:#2d5a3b; width:{row['Percent']}%; height:6px; border-radius:3px;"></div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Meal Plan
                    st.markdown("### 🍽️ Your Meal Plan")
                    st.caption(f"**Type:** {plan['meal_type']}")
                    
                    meal_items = [(k, v) for k, v in plan['meal_plan'].items() if k != 'total_calories']
                    cols = st.columns(2)
                    
                    colors = {'Breakfast': '#FF9800', 'Morning Snack': '#FFC107', 
                              'Lunch': '#4CAF50', 'Evening Snack': '#FFC107', 'Dinner': '#FF5722'}
                    
                    for idx, (meal_name, meal_data) in enumerate(meal_items):
                        with cols[idx % 2]:
                            color = colors.get(meal_name, '#2d5a3b')
                            st.markdown(f'<div class="meal-card" style="border-left-color:{color}"><div class="meal-title">⏰ {meal_name}</div>', unsafe_allow_html=True)
                            if isinstance(meal_data, dict) and 'items' in meal_data:
                                for item in meal_data['items']:
                                    st.markdown(f'<div class="food-item">• {item}</div>', unsafe_allow_html=True)
                                if 'calories' in meal_data:
                                    st.caption(f"📊 {meal_data['calories']}")
                            st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Health Tips
                    st.markdown("### 💡 Recommendations")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**❌ Avoid These:**")
                        for f in plan['avoid_foods']:
                            st.markdown(f"- {f}")
                    
                    with col2:
                        st.markdown("**✅ Eat These:**")
                        for f in plan['recommended_foods'][:5]:
                            st.markdown(f"- {f}")
                    
                    st.markdown("**📝 Daily Tips:**")
                    for tip in plan['tips']:
                        st.markdown(f"- {tip}")
                    
                    # Download
                    st.markdown("---")
                    report = generate_report(plan, {'name': name, 'age': age, 'gender': gender, 
                                                     'weight': weight, 'height': height, 'goal': goal})
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    st.download_button("📥 Download Report (TXT)", report, 
                                       f"Diet_Plan_{name}_{timestamp}.txt", use_container_width=True)
                    
                except Exception as e:
                    st.error(f"Error: {e}")

# ============================================================================
# PAGE: MEAL PLANNER
# ============================================================================

elif page == "🍽️ Meal Planner":
    st.markdown("""
    <div class="main-header">
        <h1>🍽️ Smart Meal Planner</h1>
        <p>Sample meal plans for inspiration</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 Go to Dashboard and enter your details for a personalized plan!")
    
    day = st.selectbox("Select Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    
    sample_meals = {
        "Monday": {"Breakfast": "Oatmeal with berries", "Lunch": "Grilled chicken salad", "Dinner": "Vegetable soup", "Snacks": "Apple"},
        "Tuesday": {"Breakfast": "Smoothie bowl", "Lunch": "Brown rice with dal", "Dinner": "Grilled fish", "Snacks": "Nuts"},
        "Wednesday": {"Breakfast": "Eggs with toast", "Lunch": "Quinoa bowl", "Dinner": "Paneer tikka", "Snacks": "Yogurt"},
        "Thursday": {"Breakfast": "Pancakes", "Lunch": "Chicken wrap", "Dinner": "Vegetable stir-fry", "Snacks": "Banana"},
        "Friday": {"Breakfast": "Paratha with curd", "Lunch": "Fish curry with rice", "Dinner": "Soup and salad", "Snacks": "Orange"},
        "Saturday": {"Breakfast": "French toast", "Lunch": "Pasta with veggies", "Dinner": "Homemade pizza", "Snacks": "Berries"},
        "Sunday": {"Breakfast": "Sunday special brunch", "Lunch": "Family meal", "Dinner": "Light dinner", "Snacks": "Dates"}
    }
    
    if day in sample_meals:
        st.markdown(f"### 📅 {day}'s Meal Plan")
        for meal, food in sample_meals[day].items():
            st.markdown(f"**{meal}:** {food}")

# ============================================================================
# PAGE: HEALTH TIPS
# ============================================================================

elif page == "💡 Health Tips":
    st.markdown("""
    <div class="main-header">
        <h1>💡 Health & Wellness Tips</h1>
        <p>Evidence-based nutrition and lifestyle advice</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["🥗 Nutrition", "💧 Hydration", "😴 Sleep", "🏃 Exercise"])
    
    with tab1:
        st.markdown("""
        ### 🥗 Smart Nutrition Tips
        
        **The Healthy Plate Method:**
        - 🥬 50% Vegetables & Fruits
        - 🍚 25% Whole Grains  
        - 🍗 25| Lean Protein
        
        **Golden Rules:**
        - Eat a rainbow of colorful foods
        - Prioritize protein at every meal
        - Include healthy fats (avocado, nuts, olive oil)
        - Choose whole grains over refined
        - Practice portion control
        """)
    
    with tab2:
        st.markdown("""
        ### 💧 Hydration Guide
        
        **Daily Water Needs:**
        | Gender | Liters | Cups |
        |--------|--------|------|
        | Men | 3.7L | 15.5 cups |
        | Women | 2.7L | 11.5 cups |
        
        **Signs You Need Water:**
        - Dark yellow urine
        - Dry mouth
        - Headache
        - Fatigue
        
        **Tips:**
        - Carry a water bottle
        - Set hourly reminders
        - Eat water-rich foods (cucumber, watermelon)
        """)
    
    with tab3:
        st.markdown("""
        ### 😴 Sleep Health
        
        **Sleep Needs by Age:**
        - Adults (18-64): 7-9 hours
        - Seniors (65+): 7-8 hours
        
        **Sleep Hygiene Tips:**
        - Consistent schedule
        - No screens 1 hour before bed
        - Cool, dark room
        - Avoid caffeine after 2 PM
        - Relax before bed
        
        **Benefits:**
        - Better immunity
        - Improved memory
        - Weight management
        - Reduced stress
        """)
    
    with tab4:
        st.markdown("""
        ### 🏃 Exercise Guidelines
        
        **WHO Recommendations:**
        - 150-300 min moderate OR
        - 75-150 min vigorous exercise weekly
        - Strength training 2x per week
        
        **Weekly Template:**
        - Mon: 30 min cardio + strength
        - Wed: 45 min cardio
        - Fri: 30 min strength
        - Weekend: 60 min outdoor activity
        
        **Benefits:**
        - Weight management
        - Heart health
        - Mood improvement
        - Better sleep
        - More energy
        """)

# ============================================================================
# PAGE: ABOUT
# ============================================================================

elif page == "ℹ️ About":
    st.markdown("""
    <div class="main-header">
        <h1>ℹ️ About AI Nutritionist</h1>
        <p>AI-powered personalized nutrition planning</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🚀 Our Mission
        
        Making personalized nutrition advice accessible to everyone using AI.
        
        ### 🎯 Features
        
        - **AI-Powered** - Machine learning models
        - **Personalized** - Tailored to your goals
        - **Evidence-Based** - Latest research
        - **Free** - No hidden charges
        
        ### 📊 Technology
        
        | Component | Technology |
        |-----------|------------|
        | ML Model | Random Forest |
        | Framework | Streamlit |
        | Data | Python |
        | Viz | Plotly |
        """)
    
    with col2:
        st.markdown("""
        ### 🧠 Scientific Basis
        
        - Mifflin-St Jeor BMR Equation
        - WHO Activity Guidelines
        - USDA Dietary References
        - Evidence-based Nutrition
        
        ### ⚠️ Disclaimer
        
        > This tool provides general guidance only. Always consult a healthcare provider before making significant dietary changes.
        
        ### 📧 Contact
        
        For support: support@ainutritionist.com
        
        ### 📅 Version
        
        **Version:** 2.0.0  
        **Updated:** December 2024
        """)
    
    st.markdown("---")
    st.markdown("<div style='text-align:center'>Made with ❤️ by AI Nutritionist Team</div>", unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("""
<div class="footer">
    <p>© 2024 AI Nutritionist Pro | AI-Powered Personalized Diet Planning</p>
    <p style="font-size:0.8rem;">Always consult a doctor before starting any diet plan</p>
</div>
""", unsafe_allow_html=True)