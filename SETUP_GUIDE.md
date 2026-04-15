# Personal Trainer AI - Setup Guide

## Project Overview
A comprehensive fitness coaching application built with Streamlit, Groq AI, and Supabase database.

## Prerequisites
- Python 3.8 or higher
- Groq API Key
- Supabase Account (free)

---

## Step 1: Get API Keys

### 1.1 Groq API Key
1. Go to https://console.groq.com
2. Sign up or log in
3. Create an API key
4. Copy the key for later use

### 1.2 Supabase Setup
1. Go to https://supabase.com
2. Sign up with your email (FREE tier available)
3. Create a new project
4. Wait for the project to initialize (about 2 minutes)
5. Go to Project Settings > API
6. Copy:
   - **Project URL** (SUPABASE_URL)
   - **Anon Key** (SUPABASE_KEY)

---

## Step 2: Create Database Tables in Supabase

1. In Supabase, go to **SQL Editor**
2. Click **"New Query"**
3. Copy and paste the following SQL:

```sql
-- Create user_profiles table
CREATE TABLE user_profiles (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) UNIQUE NOT NULL,
  age INT,
  weight FLOAT,
  height FLOAT,
  gender VARCHAR(50),
  activity_level VARCHAR(100),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Create fitness_goals table
CREATE TABLE fitness_goals (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES user_profiles(id) ON DELETE CASCADE,
  goals TEXT[] DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Create nutrition_goals table
CREATE TABLE nutrition_goals (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES user_profiles(id) ON DELETE CASCADE,
  daily_calories INT,
  daily_protein INT,
  daily_fat INT,
  daily_carbs INT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Create user_notes table
CREATE TABLE user_notes (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES user_profiles(id) ON DELETE CASCADE,
  note TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Create ai_conversations table
CREATE TABLE ai_conversations (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES user_profiles(id) ON DELETE CASCADE,
  question TEXT,
  response TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Set Row Level Security (RLS)
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE fitness_goals ENABLE ROW LEVEL SECURITY;
ALTER TABLE nutrition_goals ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_notes ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_conversations ENABLE ROW LEVEL SECURITY;

-- Create policies for anonymous access (for development)
CREATE POLICY "Enable all for anonymous" ON user_profiles AS PERMISSIVE FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Enable all for anonymous" ON fitness_goals AS PERMISSIVE FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Enable all for anonymous" ON nutrition_goals AS PERMISSIVE FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Enable all for anonymous" ON user_notes AS PERMISSIVE FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Enable all for anonymous" ON ai_conversations AS PERMISSIVE FOR ALL USING (true) WITH CHECK (true);
```

4. Click **"Run"** to execute the SQL

---

## Step 3: Local Setup

### 3.1 Clone/Download Project
```bash
cd c:\genai_project\personel_trainer
```

### 3.2 Create Python Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3.3 Install Dependencies
```bash
pip install -r requirements.txt
```

### 3.4 Create .env File
1. Create a file named `.env` in the project root
2. Add your credentials:

```env
GROQ_API_KEY=your_groq_api_key_here
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your_supabase_anon_key_here
```

Replace the values with your actual keys from:
- Groq: https://console.groq.com
- Supabase: Project Settings > API

---

## Step 4: Run the Application

### 4.1 Start Streamlit
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

### 4.2 Using the App
1. **Enter Your Profile**: Fill in name, age, weight, height, gender, and activity level in the sidebar
2. **Save Personal Data**: Click the save button
3. **Set Goals**: Go to the Goals tab and select your fitness objectives
4. **Nutrition**: Either generate AI recommendations or enter manually
5. **Add Notes**: Track injuries, limitations, or achievements
6. **Ask Trainer**: Ask your AI coach any fitness question

---

## Features

✅ **User Profiles**: Store personal information securely
✅ **AI Nutrition Planning**: Auto-generate meal targets using Groq AI
✅ **Fitness Goals**: Track multiple fitness objectives
✅ **Notes**: Add constraints, injuries, or progress notes
✅ **AI Trainer**: Get personalized workout and nutrition advice
✅ **Cloud Database**: Data persists in Supabase

---

## Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution**: Make sure you installed requirements.txt and activated the virtual environment

### Issue: "Invalid API Key"
**Solution**: Double-check your GROQ_API_KEY and SUPABASE credentials in .env

### Issue: "Connection refused"
**Solution**: 
1. Check your internet connection
2. Verify API keys are correct
3. Ensure Supabase project is active

### Issue: Database tables not found
**Solution**: Re-run the SQL setup in Supabase SQL Editor

---

## Project Structure

```
personel_trainer/
├── app.py                 # Main Streamlit application
├── database.py            # Supabase database operations
├── groq_client.py         # Groq AI integration
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
└── SETUP_GUIDE.md        # This file
```

---

## Environment Variables

| Variable | Example | Where to Get |
|----------|---------|-------------|
| GROQ_API_KEY | gsk_... | https://console.groq.com |
| SUPABASE_URL | https://xxx.supabase.co | Supabase Project Settings |
| SUPABASE_KEY | eyJhbGc... | Supabase Project Settings > API |

---

## Next Steps (Advanced)

### Authentication
To add user authentication, implement Supabase Auth:
- Enable Google OAuth in Supabase
- Implement session management in Streamlit

### Data Visualization
Add charts to track progress:
- Weight over time
- Workout history
- Nutrition adherence

### Workout Plans
Generate complete workout plans with exercises and sets

### Export Features
Allow users to download nutrition and workout plans as PDF

---

## Support

For issues:
1. Check error messages in terminal
2. Review Supabase logs (https://app.supabase.com)
3. Check Groq API status
4. Verify all credentials in .env file

---

## Deploy to Production

### Streamlit Cloud
1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Deploy directly from repo
4. Set environment variables in Streamlit Cloud settings

### Alternative: Docker
```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

---

**Happy Training! 🏋️**
