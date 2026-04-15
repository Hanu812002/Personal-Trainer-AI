# Personal Trainer AI 🏋️

An intelligent fitness coaching application powered by Groq AI and Streamlit. Get personalized workout plans, nutrition guidance, and AI-powered trainer coaching.

## Features

- 👤 **User Profiles**: Track your personal fitness data (age, weight, height, gender, activity level)
- 🎯 **Fitness Goals**: Set and track multiple fitness objectives
- 🍽️ **Nutrition Planning**: AI-generated or custom nutrition goals based on your metrics
- 📝 **Notes & Tracking**: Record injuries, limitations, achievements
- 🤖 **AI Trainer**: Ask questions and get personalized coaching based on your profile
- ☁️ **Cloud Database**: All data stored securely in Supabase
- 🚀 **Fast AI**: Powered by Groq's fast LLM inference

## Quick Start

### Prerequisites
- Python 3.8+
- Groq API Key (free from https://console.groq.com)
- Supabase Account (free from https://supabase.com)

### Installation

1. **Clone the repository**
```bash
git clone <your-repo>
cd personel_trainer
```

2. **Set up virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up database** (See SETUP_GUIDE.md for detailed SQL setup)

5. **Create .env file**
```
GROQ_API_KEY=your_key_here
SUPABASE_URL=your_url_here
SUPABASE_KEY=your_key_here
```

6. **Run the app**
```bash
streamlit run app.py
```

Open browser to `http://localhost:8501`

## Usage

### Step 1: Create Your Profile
- Enter name, age, weight, height, gender, activity level
- Click "Save Personal Data"

### Step 2: Set Your Fitness Goals
- Select from available goals (Muscle Gain, Fat Loss, etc.)
- Click "Save Goals"

### Step 3: Set Nutrition Goals
- Option A: Click "Generate with AI" for personalized recommendations
- Option B: Manually enter calories, protein, carbs, fat targets
- Click "Save Nutrition Goals"

### Step 4: Add Notes
- Track injuries, limitations, or achievements
- These will be considered when getting AI recommendations

### Step 5: Ask Your AI Trainer
- Type any fitness or nutrition question
- Get personalized advice based on your profile and history

## Architecture

### Frontend
- **Streamlit**: Interactive web UI
- **Tabs**: Organize different sections (Goals, Nutrition, Notes, AI Trainer)
- **Sidebar**: User profile management

### Backend
- **Groq AI**: LLM inference for nutrition planning and coaching
- **Supabase**: PostgreSQL database with REST API
- **Python**: Core application logic

### Database Schema
- `user_profiles`: User information
- `fitness_goals`: Selected fitness objectives
- `nutrition_goals`: Daily nutrition targets
- `user_notes`: User notes and constraints
- `ai_conversations`: Chat history

## Configuration

### Environment Variables
```
GROQ_API_KEY         # Your Groq API key
SUPABASE_URL         # Your Supabase project URL
SUPABASE_KEY         # Your Supabase anon key
```

## Customization

### Change AI Model
In `groq_client.py`:
```python
self.model = "mixtral-8x7b-32768"  # Change to other Groq models
```

Available models:
- mixtral-8x7b-32768 (fast, versatile)
- llama2-70b-4096 (powerful)
- gemma-7b-it (lightweight)

### Change UI Theme
Modify CSS in `app.py` `st.markdown()` sections

### Add More Goals
Update the `available_goals` list in `app.py`

## Database Setup (Supabase)

See `SETUP_GUIDE.md` for complete setup instructions with SQL scripts.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| ModuleNotFoundError | Install requirements: `pip install -r requirements.txt` |
| Invalid API Key | Check .env file with correct Groq/Supabase keys |
| Connection error | Verify internet and credentials |
| Database error | Rerun SQL setup in Supabase |

## Performance Tips

- First AI request may take 2-3 seconds (network latency)
- Subsequent requests faster
- Groq inference is optimized for speed
- Database operations are cached in session state

## Future Enhancements

- 📊 Progress visualization charts
- 📅 Workout schedule generation
- 📱 Mobile app version
- 🔐 User authentication
- 💾 PDF export for plans
- 🎥 Exercise video integration
- 🏆 Achievement badges

## Contributing

Feel free to fork, modify, and improve!

## License

MIT License - feel free to use for personal or commercial projects

## Support

For issues or questions:
1. Check SETUP_GUIDE.md
2. Review Supabase dashboard
3. Check Groq API status
4. Verify .env credentials

---

**Start your fitness journey with AI-powered coaching today!** 🚀

Made with ❤️ | Powered by Groq & Supabase
