import os
from groq import Groq
from dotenv import load_dotenv
import streamlit as st

load_dotenv()


class GroqAIClient:
    """Handle all Groq AI interactions"""
    
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.1-8b-instant"  # Fast and efficient model
    
    def generate_nutrition_goals(self, weight: float, height: float, gender: str, 
                                 age: int, activity_level: str) -> dict:
        """Generate nutrition goals based on user metrics using AI"""
        try:
            prompt = f"""Based on the following user metrics, generate personalized daily nutrition goals:
- Gender: {gender}
- Age: {age} years
- Weight: {weight} kg
- Height: {height} cm
- Activity Level: {activity_level}

Provide ONLY the following in this exact format (numbers only):
Calories: [number]
Protein: [number]
Fat: [number]
Carbs: [number]

Calculate based on standard fitness formulas and Harris-Benedict equation for BMR."""

            message = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            response_text = message.choices[0].message.content
            nutrition_goals = self._parse_nutrition_response(response_text)
            
            return {"success": True, "goals": nutrition_goals}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def ask_trainer(self, user_name: str, question: str, user_notes: list, 
                   height: float, weight: float, nutrition_goals: dict, 
                   fitness_goals: list) -> dict:
        """Ask AI trainer a question based on user context"""
        try:
            notes_text = "\n".join(user_notes) if user_notes else "No notes added"
            goals_text = ", ".join(fitness_goals) if fitness_goals else "No goals set"
            nutrition_text = f"Calorie target: {nutrition_goals.get('daily_calories', 'Not set')} kcal"
            
            prompt = f"""You are a professional personal trainer and fitness coach. 
            
User Information:
- Name: {user_name}
- Height: {height} cm
- Weight: {weight} kg
- Fitness Goals: {goals_text}
- Daily Nutrition Target: {nutrition_text}

User Notes/Constraints:
{notes_text}

User Question: {question}

Provide a helpful, personalized response as a professional trainer. Be specific and actionable."""

            message = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            response_text = message.choices[0].message.content
            return {"success": True, "response": response_text}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def generate_workout_plan(self, user_name: str, age: int, weight: float, height: float,
                             activity_level: str, fitness_goals: list, user_notes: list,
                             experience_level: str = "Intermediate") -> dict:
        """Generate 15-day AI workout plan"""
        try:
            notes_text = "\n".join(user_notes) if user_notes else "No constraints"
            goals_text = ", ".join(fitness_goals) if fitness_goals else "General fitness"
            
            prompt = f"""You are a professional fitness coach. Generate a detailed 15-day workout plan for the user.

User Profile:
- Name: {user_name}
- Age: {age}, Weight: {weight}kg, Height: {height}cm
- Activity Level: {activity_level}
- Experience: {experience_level}
- Goals: {goals_text}

Constraints/Notes to avoid:
{notes_text}

Generate a 15-day workout split with:
- Each day's focus (e.g., Chest & Triceps, Back & Biceps, Legs, etc.)
- 4-6 exercises per day
- For each exercise: sets x reps (e.g., 4x8-10)
- Rest time between sets (45-90 seconds)
- Brief form tips

Avoid exercises that conflict with their notes/constraints.

Format each day clearly with:
DAY 1: [Focus Area]
Exercise 1: [Name] - [Sets x Reps] - Rest: [time]
Exercise 2: [Name] - [Sets x Reps] - Rest: [time]
[continue...]

DAY 2: [Focus Area]
[continue through DAY 15]"""

            message = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=3000
            )
            
            response_text = message.choices[0].message.content
            return {"success": True, "plan": response_text}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def generate_meal_plan(self, user_name: str, gender: str, weight: float, height: float,
                          daily_calories: int, daily_protein: int, daily_fat: int, 
                          daily_carbs: int, dietary_preference: str = "Balanced",
                          user_notes: list = None) -> dict:
        """Generate 15-day AI meal plan"""
        try:
            notes_text = "\n".join(user_notes) if user_notes else "No restrictions"
            
            prompt = f"""You are a professional nutritionist. Generate a detailed 15-day meal plan for the user.

User:
- Name: {user_name}
- Gender: {gender}
- Weight: {weight}kg, Height: {height}cm
- Daily targets: {daily_calories} calories, {daily_protein}g protein, {daily_fat}g fat, {daily_carbs}g carbs
- Dietary Preference: {dietary_preference}

Notes/Restrictions:
{notes_text}

For each day, provide:
- 3 meals (Breakfast, Lunch, Dinner)
- 1-2 snacks
- For each: Food items, portion sizes, estimated calories, protein, carbs, fat
- Total daily macros

Make sure meals:
- Match the daily calorie/macro targets
- Are varied and realistic
- Consider their restrictions
- Include foods they can actually cook

Format as:
DAY 1:
BREAKFAST: [Food] portions - [Cals, Protein, Carbs, Fat]
LUNCH: [Food] portions - [Cals, Protein, Carbs, Fat]
DINNER: [Food] portions - [Cals, Protein, Carbs, Fat]
SNACK: [Food] portions - [Cals, Protein, Carbs, Fat]
DAY TOTAL: [Total Cals, Protein, Carbs, Fat]

[Continue through DAY 15]

At the end, provide a SHOPPING LIST with quantities needed for the week."""

            message = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=4000
            )
            
            response_text = message.choices[0].message.content
            return {"success": True, "plan": response_text}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _parse_nutrition_response(self, response: str) -> dict:
        """Parse nutrition goals from AI response"""
        try:
            lines = response.strip().split('\n')
            goals = {}
            
            for line in lines:
                if 'Calories:' in line:
                    goals['calories'] = int(line.split(':')[1].strip())
                elif 'Protein:' in line:
                    goals['protein'] = int(line.split(':')[1].strip())
                elif 'Fat:' in line:
                    goals['fat'] = int(line.split(':')[1].strip())
                elif 'Carbs:' in line:
                    goals['carbs'] = int(line.split(':')[1].strip())
            
            return goals if len(goals) == 4 else {"error": "Could not parse response"}
        except Exception as e:
            return {"error": str(e)}
