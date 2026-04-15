import streamlit as st
from database import DatabaseManager
from groq_client import GroqAIClient
import time

# Configure Streamlit
st.set_page_config(
    page_title="Personal Trainer AI",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.8rem;
        color: #004E89;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #FF6B35;
        padding-bottom: 0.5rem;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #cfe2ff;
        border-left: 4px solid #0d6efd;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    /* Tabs styling */
    button[data-baseweb="tab"] {
        font-size: 1.1rem !important;
        padding: 0.75rem 1.5rem !important;
        margin-right: 1rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Main title
st.markdown('<div class="main-header">🏋️ Personal Trainer AI</div>', unsafe_allow_html=True)

# Initialize database and AI clients
db = DatabaseManager()
ai_client = GroqAIClient()

# Sidebar for user selection/creation
with st.sidebar:
    st.title("👤 User Profile")
    
    # Section 1: Personal Data
    st.markdown('<div class="section-header">Personal Information</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name")
    with col2:
        age = st.number_input("Age", min_value=13, max_value=100, value=None)
    
    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, step=0.1, value=None)
    with col2:
        height = st.number_input("Height (cm)", min_value=100, max_value=250, value=None)
    
    gender = st.radio("Gender", ["Male", "Female", "Other"])
    
    activity_level = st.selectbox(
        "Activity Level",
        ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Super Active"]
    )
    
    if st.button("💾 Save Personal Data", use_container_width=True):
        if name:
            result = db.create_user_profile(name, age, weight, height, gender, activity_level)
            if result['success']:
                st.session_state.name = name
                st.session_state.age = age
                st.session_state.weight = weight
                st.session_state.height = height
                st.session_state.gender = gender
                st.session_state.activity_level = activity_level
                st.session_state.user_id = result['user_id']
                st.session_state.current_user = name
                st.success("✅ Profile saved successfully!")
                time.sleep(1)
                st.rerun()
            else:
                st.error(f"Error: {result.get('error')}")
        else:
            st.error("Please enter your name")

# Main content area
if st.session_state.user_id:
    user_name = st.session_state.current_user
    user_id = st.session_state.user_id
    
    st.success(f"👋 Welcome, {user_name}!")
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🎯 Goals", "🍽️ Nutrition", "📝 Notes", "🤖 Ask Trainer", "🏋️ Workout Plan", "🍴 Meal Planner"])
    
    # TAB 1: Fitness Goals
    with tab1:
        st.markdown('<div class="section-header">Select Your Fitness Goals</div>', unsafe_allow_html=True)
        
        available_goals = ["Muscle Gain", "Fat Loss", "Stay Active", "Improve Endurance", 
                          "Increase Flexibility", "Build Strength"]
        
        selected_goals = st.multiselect(
            "Choose your fitness goals:",
            available_goals,
            default=st.session_state.get('selected_goals', [])
        )
        
        if st.button("💾 Save Goals", key="save_goals", use_container_width=True):
            if selected_goals:
                result = db.save_goals(user_id, selected_goals)
                if result['success']:
                    st.session_state.selected_goals = selected_goals
                    st.success("✅ Goals saved successfully!")
                else:
                    st.error(f"Error: {result.get('error')}")
            else:
                st.warning("Please select at least one goal")
    
    # TAB 2: Nutrition Goals
    with tab2:
        st.markdown('<div class="section-header">Nutrition Goals</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            if st.button("🤖 Generate with AI", use_container_width=True, key="generate_nutrition"):
                with st.spinner("🔄 AI is calculating your nutrition goals..."):
                    result = ai_client.generate_nutrition_goals(
                        st.session_state.weight,
                        st.session_state.height,
                        st.session_state.gender,
                        st.session_state.age,
                        st.session_state.activity_level
                    )
                    
                    if result['success']:
                        goals = result['goals']
                        st.session_state.calories = goals.get('calories', 2500)
                        st.session_state.protein = goals.get('protein', 150)
                        st.session_state.fat = goals.get('fat', 70)
                        st.session_state.carbs = goals.get('carbs', 300)
                        st.success("✅ AI generated your nutrition plan!")
                        st.rerun()
                    else:
                        st.error(f"Error: {result.get('error')}")
        
        with col2:
            st.info("💡 Click 'Generate with AI' to get personalized nutrition recommendations based on your profile")
        
        st.divider()
        st.markdown("#### Manual Nutrition Input")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            calories = st.number_input("Calories", min_value=1500, max_value=5000, step=100, 
                                      value=st.session_state.get('calories') or None)
        with col2:
            protein = st.number_input("Protein (g)", min_value=50, max_value=300, step=10,
                                     value=st.session_state.get('protein') or None)
        with col3:
            fat = st.number_input("Fat (g)", min_value=30, max_value=150, step=5,
                                 value=st.session_state.get('fat') or None)
        with col4:
            carbs = st.number_input("Carbs (g)", min_value=100, max_value=500, step=10,
                                   value=st.session_state.get('carbs') or None)
        
        if st.button("💾 Save Nutrition Goals", key="save_nutrition", use_container_width=True):
            result = db.save_nutrition_goals(user_id, calories, protein, fat, carbs)
            if result['success']:
                st.session_state.calories = calories
                st.session_state.protein = protein
                st.session_state.fat = fat
                st.session_state.carbs = carbs
                st.success("✅ Nutrition goals saved!")
            else:
                st.error(f"Error: {result.get('error')}")
    
    # TAB 3: Notes
    with tab3:
        st.markdown('<div class="section-header">Your Notes</div>', unsafe_allow_html=True)
        
        # Display existing notes
        notes_result = db.get_notes(user_id)
        if notes_result['success'] and notes_result['notes']:
            st.markdown("#### 📋 Existing Notes:")
            for note in notes_result['notes']:
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.write(f"• {note['note']}")
                with col2:
                    if st.button("🗑️", key=f"delete_note_{note['id']}", help="Delete this note"):
                        db.delete_note(note['id'])
                        st.success("Note deleted!")
                        st.rerun()
        else:
            st.info("No notes yet. Add one below!")
        
        st.divider()
        
        # Add new note
        st.markdown("#### ➕ Add a New Note:")
        new_note = st.text_area("Write your note here (e.g., injuries, limitations, achievements)",
                               height=100, key="new_note_input")
        
        if st.button("📝 Add Note", use_container_width=True):
            if new_note.strip():
                result = db.add_note(user_id, new_note)
                if result['success']:
                    st.success("✅ Note added successfully!")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error(f"Error: {result.get('error')}")
            else:
                st.warning("Please write something in the note")
    
    # TAB 4: Ask Trainer
    with tab4:
        st.markdown('<div class="section-header">Ask Your AI Trainer</div>', unsafe_allow_html=True)
        
        st.info("💡 Ask any fitness, nutrition, or training-related questions and get personalized advice based on your profile and notes!")
        
        # Get user context
        profile_result = db.get_user_profile(user_name)
        nutrition_result = db.get_nutrition_goals(user_id)
        notes_result = db.get_notes(user_id)
        
        user_notes = [note['note'] for note in notes_result.get('notes', [])]
        nutrition_context = nutrition_result.get('nutrition', {}) if nutrition_result['success'] else {}
        
        # Question input
        question = st.text_area("Type your question here:", height=100, 
                               placeholder="E.g., Can you suggest a leg workout routine for me?")
        
        if st.button("🤖 Ask AI", use_container_width=True, key="ask_trainer"):
            if question.strip():
                with st.spinner("🤔 Your trainer is thinking..."):
                    result = ai_client.ask_trainer(
                        user_name,
                        question,
                        user_notes,
                        st.session_state.height,
                        st.session_state.weight,
                        nutrition_context,
                        st.session_state.get('selected_goals', [])
                    )
                    
                    if result['success']:
                        response = result['response']
                        # Save to database
                        db.save_ai_response(user_id, question, response)
                        
                        st.markdown("#### 🏋️ Trainer's Response:")
                        st.markdown(f"""
                        <div class="">
                        {response}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error(f"Error: {result.get('error')}")
            else:
                st.warning("Please ask a question")
    
    # TAB 5: Workout Plan
    with tab5:
        st.markdown('<div class="section-header">🏋️ 15-Day AI Workout Plan</div>', unsafe_allow_html=True)
        
        st.info("💡 Generate a personalized 15-day workout plan. Based on your goals, fitness level, and any constraints.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            experience_level = st.selectbox(
                "Experience Level",
                ["Beginner", "Intermediate", "Advanced"],
                key="experience_level"
            )
        
        with col2:
            st.write("")
        
        if st.button("🤖 Generate 15-Day Workout Plan", use_container_width=True, key="generate_workout"):
            if not st.session_state.get('selected_goals'):
                st.warning("⚠️ Please set your fitness goals first in the Goals tab")
            else:
                with st.spinner("🔄 AI is creating your personalized workout plan..."):
                    # Get user notes
                    notes_result = db.get_notes(user_id)
                    user_notes = [note['note'] for note in notes_result.get('notes', [])]
                    
                    result = ai_client.generate_workout_plan(
                        user_name,
                        st.session_state.age,
                        st.session_state.weight,
                        st.session_state.height,
                        st.session_state.activity_level,
                        st.session_state.get('selected_goals', []),
                        user_notes,
                        experience_level
                    )
                    
                    if result['success']:
                        st.success("✅ Your 15-day workout plan is ready!")
                        st.markdown("""
                        <div class="">
                        """ + result['plan'] + """
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Option to download
                        if st.button("📥 Copy Plan to Clipboard", key="copy_workout"):
                            st.info("Plan displayed above - you can copy it!")
                    else:
                        st.error(f"Error: {result.get('error')}")
    
    # TAB 6: Meal Planner
    with tab6:
        st.markdown('<div class="section-header">🍴 15-Day AI Meal Plan</div>', unsafe_allow_html=True)
        
        st.info("💡 Generate a personalized 15-day meal plan matching your nutrition goals. Includes shopping list!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            dietary_preference = st.selectbox(
                "Dietary Preference",
                ["Balanced", "High Protein", "Low Carb", "Vegetarian", "Vegan", "Keto"],
                key="dietary_pref"
            )
        
        with col2:
            st.write("")
        
        # Check if nutrition goals are set
        nutrition_result = db.get_nutrition_goals(user_id)
        has_nutrition_goals = nutrition_result['success']
        
        if st.button("🤖 Generate 15-Day Meal Plan", use_container_width=True, key="generate_meal"):
            if not has_nutrition_goals:
                st.warning("⚠️ Please set your nutrition goals first in the Nutrition tab")
            else:
                with st.spinner("🔄 AI is creating your personalized meal plan..."):
                    # Get user notes
                    notes_result = db.get_notes(user_id)
                    user_notes = [note['note'] for note in notes_result.get('notes', [])]
                    
                    nutrition = nutrition_result.get('nutrition', {})
                    
                    result = ai_client.generate_meal_plan(
                        user_name,
                        st.session_state.gender,
                        st.session_state.weight,
                        st.session_state.height,
                        nutrition.get('daily_calories', 2500),
                        nutrition.get('daily_protein', 150),
                        nutrition.get('daily_fat', 70),
                        nutrition.get('daily_carbs', 300),
                        dietary_preference,
                        user_notes
                    )
                    
                    if result['success']:
                        st.success("✅ Your 15-day meal plan is ready!")
                        st.markdown("""
                        <div class="">
                        """ + result['plan'] + """
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Option to download
                        if st.button("📥 Copy Meal Plan to Clipboard", key="copy_meal"):
                            st.info("Plan displayed above - you can copy it!")
                    else:
                        st.error(f"Error: {result.get('error')}")

else:
    # No user logged in
    st.info("👈 Please fill in your personal information in the sidebar and click 'Save Personal Data' to get started!")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊", "Track Progress", "Daily")
    with col2:
        st.metric("🤖", "AI Coach", "24/7")
    with col3:
        st.metric("🎯", "Custom Plans", "Personalized")

# Footer
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.9rem; margin-top: 2rem;'>
    Made with ❤️ | Personal Trainer AI v1.0 | Powered by Groq
    </div>
    """,
    unsafe_allow_html=True
)
