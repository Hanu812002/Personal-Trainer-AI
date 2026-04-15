import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class DatabaseManager:
    """Manage all database operations for Personal Trainer App"""
    
    @staticmethod
    def create_user_profile(name: str, age: int, weight: float, height: float, 
                           gender: str, activity_level: str) -> dict:
        """Create or update user profile"""
        try:
            # Check if user exists
            existing = supabase.table("user_profiles").select("*").eq("name", name).execute()
            
            user_data = {
                "name": name,
                "age": age,
                "weight": weight,
                "height": height,
                "gender": gender,
                "activity_level": activity_level,
                "updated_at": datetime.now().isoformat()
            }
            
            if existing.data:
                # Update existing user
                result = supabase.table("user_profiles").update(user_data).eq("name", name).execute()
                return {"success": True, "message": "Profile updated", "user_id": existing.data[0]["id"]}
            else:
                # Create new user
                user_data["created_at"] = datetime.now().isoformat()
                result = supabase.table("user_profiles").insert(user_data).execute()
                return {"success": True, "message": "Profile created", "user_id": result.data[0]["id"]}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_user_profile(name: str) -> dict:
        """Retrieve user profile by name"""
        try:
            result = supabase.table("user_profiles").select("*").eq("name", name).execute()
            if result.data:
                return {"success": True, "profile": result.data[0]}
            return {"success": False, "message": "User not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def save_goals(user_id: int, goals: list) -> dict:
        """Save user fitness goals"""
        try:
            goals_data = {
                "user_id": user_id,
                "goals": goals,
                "updated_at": datetime.now().isoformat()
            }
            
            # Check if goals exist for this user
            existing = supabase.table("fitness_goals").select("*").eq("user_id", user_id).execute()
            
            if existing.data:
                result = supabase.table("fitness_goals").update(goals_data).eq("user_id", user_id).execute()
            else:
                goals_data["created_at"] = datetime.now().isoformat()
                result = supabase.table("fitness_goals").insert(goals_data).execute()
            
            return {"success": True, "message": "Goals saved"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def save_nutrition_goals(user_id: int, calories: int, protein: int, fat: int, carbs: int) -> dict:
        """Save nutrition goals"""
        try:
            nutrition_data = {
                "user_id": user_id,
                "daily_calories": calories,
                "daily_protein": protein,
                "daily_fat": fat,
                "daily_carbs": carbs,
                "updated_at": datetime.now().isoformat()
            }
            
            existing = supabase.table("nutrition_goals").select("*").eq("user_id", user_id).execute()
            
            if existing.data:
                result = supabase.table("nutrition_goals").update(nutrition_data).eq("user_id", user_id).execute()
            else:
                nutrition_data["created_at"] = datetime.now().isoformat()
                result = supabase.table("nutrition_goals").insert(nutrition_data).execute()
            
            return {"success": True, "message": "Nutrition goals saved"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_nutrition_goals(user_id: int) -> dict:
        """Retrieve nutrition goals"""
        try:
            result = supabase.table("nutrition_goals").select("*").eq("user_id", user_id).execute()
            if result.data:
                return {"success": True, "nutrition": result.data[0]}
            return {"success": False, "message": "No nutrition goals found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def add_note(user_id: int, note_text: str) -> dict:
        """Add a note for the user"""
        try:
            note_data = {
                "user_id": user_id,
                "note": note_text,
                "created_at": datetime.now().isoformat()
            }
            result = supabase.table("user_notes").insert(note_data).execute()
            return {"success": True, "message": "Note added", "note_id": result.data[0]["id"]}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_notes(user_id: int) -> dict:
        """Get all notes for a user"""
        try:
            result = supabase.table("user_notes").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
            return {"success": True, "notes": result.data if result.data else []}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def delete_note(note_id: int) -> dict:
        """Delete a note"""
        try:
            supabase.table("user_notes").delete().eq("id", note_id).execute()
            return {"success": True, "message": "Note deleted"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def save_ai_response(user_id: int, question: str, response: str) -> dict:
        """Save AI conversation"""
        try:
            response_data = {
                "user_id": user_id,
                "question": question,
                "response": response,
                "created_at": datetime.now().isoformat()
            }
            # result = supabase.table("ai_conversations").insert(response_data).execute()
            return {"success": True, "message": "Response saved"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_ai_history(user_id: int) -> dict:
        """Get AI conversation history"""
        try:
            result = supabase.table("ai_conversations").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(10).execute()
            return {"success": True, "history": result.data if result.data else []}
        except Exception as e:
            return {"success": False, "error": str(e)}
