from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

OPENROUTER_API_KEY = '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'  
OPENROUTER_MODEL = 'mistralai/mistral-small-24b-instruct-2501:free'  

SYSTEM_PROMPT = """
You are a Chill Mentor chatbot.
You answer with a calm, relaxed tone, giving simple but meaningful advice like a wise older friend.
Stay positive, encouraging, and human-like.
"""

@app.route('/')
def index():
    return render_template('index.html')  

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json['message']

        headers = {
            'Authorization': f'Bearer {OPENROUTER_API_KEY}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'http://localhost:5000',   # required by OpenRouter
            'X-Title': 'Chill Mentor Bot'
        }
        payload = {
            "model": OPENROUTER_MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        }

        response = requests.post('https://openrouter.ai/api/v1/chat/completions', headers=headers, json=payload)
        res_json = response.json()
        print("FULL OpenRouter Response:", res_json)

        if 'choices' in res_json:
            bot_message = res_json['choices'][0]['message']['content']
            return jsonify({'reply': bot_message})
        else:
            return jsonify({'error': res_json}), 500

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
      