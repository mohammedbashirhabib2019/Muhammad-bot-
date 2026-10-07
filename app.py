from flask import Flask, request, render_template_string, jsonify
import os, requests
app = Flask(__name__)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
def get_ai_answer(q):
    if not GROQ_API_KEY:
        return "Saka GROQ_API_KEY a Render"
    try:
        url="https://api.groq.com/openai/v1/chat/completions"
        headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        data={"model": "llama-3.1-8b-instant", "messages": [{"role": "system", "content": "Kai ne MuhammadBot"}, {"role": "user", "content": q}]}
        r=requests.post(url, headers=headers, json=data, timeout=20)
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Matsala: {e}"
HTML="<html><body><h3>MuhammadBot</h3><div id=c></div><input id=q><button onclick=ask()>Send</button><script>async function ask(){let v=document.getElementById('q').value;let c=document.getElementById('c');c.innerHTML+=v+'<br>';let r=await fetch('/ask?q='+v);let d=await r.json();c.innerHTML+=d.answer+'<br>'}</script></body></html>"
@app.route('/')
def home():
    return render_template_string(HTML)
@app.route('/ask')
def ask_q():
    return jsonify({"answer": get_ai_answer(request.args.get('q',''))})
@app.route('/webhook', methods=['GET','POST'])
def webhook():
    if request.method=='GET':
        if request.args.get('hub.verify_token')=='muhammad123':
            return request.args.get('hub.challenge')
        return "Failed",403
    return "OK",200
if __name__=='__main__':
    app.run(host='0.0.0.0', port=10000)
