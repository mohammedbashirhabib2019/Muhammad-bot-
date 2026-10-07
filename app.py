from flask import Flask, request, jsonify
import os, requests

app = Flask(__name__)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

def get_ai_answer(q):
    if not GROQ_API_KEY:
        return "Saka GROQ_API_KEY a Render"
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "user", "content": q}
            ]
        }
        r = requests.post(url, headers=headers, json=data, timeout=20)
        j = r.json()
        return j["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e}"

@app.route('/')
def home():
    return "MuhammadBot is Live! Go to /ask?q=Sannu"

@app.route('/ask')
def ask_q():
    q = request.args.get('q', '')
    ans = get_ai_answer(q)
    return jsonify({"answer": ans})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
