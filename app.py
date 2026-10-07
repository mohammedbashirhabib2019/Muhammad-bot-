from flask import Flask, request, jsonify, render_template_string
import os, requests

app = Flask(__name__)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

def get_ai_answer(q):
    if not GROQ_API_KEY:
        return "⚠️ Ba a saka GROQ_API_KEY ba a Render > Environment"
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "Kai ne MuhammadBot, mataimaki mai hankali. Kana magana da Hausa da English."},
                {"role": "user", "content": q}
            ]
        }
        r = requests.post(url, headers=headers, json=data, timeout=30)
        j = r.json()
        # Idan error ne, nuna shi
        if "choices" not in j:
            return f"Groq Error: {j}"
        return j["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Matsala: {e}"
HTML = """
<!DOCTYPE html>
<html><head><meta name=viewport content="width=device-width,initial-scale=1">
<title>MuhammadBot</title>
<style>
body{font-family:sans-serif;background:#f5f5f5;margin:0;padding:0}
.header{background:#075E54;color:white;padding:15px;text-align:center;font-size:18px;font-weight:bold}
#chat{height:75vh;overflow-y:auto;padding:15px}
.user{background:#DCF8C6;padding:10px;border-radius:10px;margin:8px 0;margin-left:20%;text-align:right}
.bot{background:white;padding:10px;border-radius:10px;margin:8px 0;margin-right:20%;box-shadow:0 1px 1px #ccc}
.input-area{position:fixed;bottom:0;width:100%;background:white;display:flex;padding:10px;box-sizing:border-box}
input{flex:1;padding:12px;border:1px solid #ddd;border-radius:25px;outline:none}
button{background:#075E54;color:white;border:none;padding:12px 20px;border-radius:25px;margin-left:10px}
</style></head>
<body>
<div class=header>🤖 MuhammadBot - Kamar Meta AI</div>
<div id=chat><div class=bot>Sannu! Ni ne MuhammadBot. Me zan taimaka maka yau?</div></div>
<div class=input-area><input id=q placeholder="Rubuta tambaya..." onkeypress="if(event.key==='Enter')ask()"><button onclick="ask()">Send</button></div>
<script>
async function ask(){
 let v=document.getElementById('q').value; if(!v) return;
 let c=document.getElementById('chat');
 c.innerHTML+=`<div class=user>${v}</div>`; document.getElementById('q').value='';
 c.scrollTop=c.scrollHeight;
 let r=await fetch('/ask?q='+encodeURIComponent(v));
 let d=await r.json();
 c.innerHTML+=`<div class=bot>${d.answer}</div>`;
 c.scrollTop=c.scrollHeight;
}
</script></body></html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/ask')
def ask_q():
    q = request.args.get('q','')
    return jsonify({"answer": get_ai_answer(q)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
