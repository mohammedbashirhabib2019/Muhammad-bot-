from flask import Flask, request, render_template_string, jsonify
import os, requests

app = Flask(__name__)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

def get_ai_answer(q):
    if not GROQ_API_KEY:
        return "Saka GROQ_API_KEY a Render > Environment"
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        sys_msg = "Kai ne MuhammadBot, mataimaki mai hankali. Amsa da yaren da aka tambaye ka: Hausa, English, Larabci, French."
        data = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": sys_msg},
                {"role": "user", "content": q}
            ]
        }
        r = requests.post(url, headers=headers, json=data, timeout=20)
        j = r.json()
        if "choices" in j:
            return j["choices"][0]["message"]["content"]
        return str(j)
    except Exception as e:
        return f"Matsala: {e}"

HTML = """<!DOCTYPE html><html><head><meta name=viewport content="width=device-width,initial-scale=1"><title>MuhammadBot</title><style>body{font-family:sans-serif;padding:10px;max-width:600px;margin:auto}#c{height:70vh;overflow-y:auto;border:1px solid #ccc;padding:10px}.u{text-align:right;margin:5px}.b{text-align:left;margin:5px;background:#f0f0f0;padding:5px;border-radius:8px}</style></head><body><h3>MuhammadBot 🤖</h3><div id=c></div><input id=q style="width:70%" placeholder="Rubuta..."><button onclick="ask()">Send</button><script>async function ask(){let i=document.getElementById('q');let v=i.value;if(!v)return;let c=document.getElementById('c');c.innerHTML+=`<div class=u>${v}</div>`;i.value='';let r=await fetch('/ask?q='+encodeURIComponent(v));let d=await r.json();c.innerHTML+=`<div class=b>${d.answer}</div>`;c.scrollTop=c.scrollHeight}</script></body></html>"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/ask')
def ask_q():
    q = request.args.get('q', '')
    return jsonify({"answer": get_ai_answer(q)})

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == 'muhammad123':
            return request.args.get('hub.challenge')
        return "Failed", 403
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
