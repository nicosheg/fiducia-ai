from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from groq import Groq
import random

app = Flask(__name__)
CORS(app)

# Load all GROQ keys
GROQ_KEYS = [
    os.getenv('GROQ_KEY_1'),
    os.getenv('GROQ_KEY_2'),
    os.getenv('GROQ_KEY_3'),
]
GROQ_KEYS = [k for k in GROQ_KEYS if k]  # Remove None values

if not GROQ_KEYS:
    raise ValueError("No GROQ keys found! Add GROQ_KEY_1, GROQ_KEY_2, GROQ_KEY_3")

# ... rest of code ...

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '')
        user_id = data.get('user_id', 'unknown')
        
        # Use random key (load balancing)
        api_key = random.choice(GROQ_KEYS)
        client = Groq(api_key=api_key)
        
        # ... rest of chat logic ...

# Compressed system prompt
SP = """You are FIDUCIA AI - Nigerian student coach (exam + money + growth)

IDENTITY:
├─ Help students progress measurably (◈ AURA tracks it)
├─ Real advice, not fake motivation
├─ Offline-ready, Nigeria-grounded
└─ Learn from user data + improve continuously

CORE MODES (Auto-trigger):
├─ BUILDER: How-to → step-by-step, actionable
├─ STRATEGIST: Confused → pattern recognition, options
├─ ANALYST: Complex topic → break down, examples
├─ REALITY CHECK: Unrealistic → honest feedback
└─ CELEBRATOR: Wins → genuine celebration 🔥

MONEY + EXAM BALANCE:
├─ Months 1-2: ₦1K/week gigs + basic exam
├─ Months 3-8: ₦5K-20K/week + solid foundation
└─ Months 9-10: Exam focus (can pause income)

VERIFICATION:
├─ Internet = 40% trust ("verify yourself")
├─ Community = 70% trust ("real Nigerians doing this")
├─ Exam data = 95% trust ("from past papers")

CONVERSATION:
├─ Friend tone (emojis OK, human energy)
├─ Compressed by default (brief, respect time)
├─ Ask before teaching (engage first)
├─ Honest about limitations ("I'm not sure")

NIGERIA REALITY:
├─ Power cuts, internet drops, money tight, family pressure
├─ Need ₦ THIS WEEK, not ₦ in 6 months
├─ Mix English + Nigerian slang OK
└─ Never preach - SHOW through advice"""

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '')
        user_id = data.get('user_id', 'unknown')
        
        # Learn from app data
        user_context = ""
        
        if data.get('study_data'):
            study = data['study_data']
            user_context += f"\n📚 Study: {study.get('questions_count', 0)} Qs, Streak: {study.get('streak_days', 0)}d"
        
        if data.get('aura_data'):
            aura = data['aura_data']
            user_context += f"\n◈ AURA: {aura.get('balance', 0)}, Rank: {aura.get('rank', 'Alpha')}"
        
        if data.get('emotion'):
            user_context += f"\n Mood: {data['emotion']}"
        
        system_prompt = SP + user_context
        
        # Use Groq instead of Claude
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",  # Free, fast, good quality
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=1024,
            temperature=0.7
        )
        
        return jsonify({
            'reply': response.choices[0].message.content,
            'user_id': user_id,
            'model': 'Groq Mixtral',
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'FIDUCIA AI is alive! 🔥', 'api': 'Groq'})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
