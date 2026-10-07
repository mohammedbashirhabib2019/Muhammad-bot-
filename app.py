
from flask import Flask, request, render_template_string, jsonify
import os, requests
app = Flask(__name__)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY","")
def get_ai_answer(q):
    if not GROQ_API_KEY: return "Saka GROQ_API_KEY a Render > Environment!"
    try:
        url="https://api.groq.com/openai/v1/chat/completions"
        headers={"Authorization": f"Bearer {GROQ_API_KEY}","Content-Type":"application/json"}
        sys="Kai ne MuhammadBot, mataimaki mai hankali kamar Meta AI. Sunanka MuhammadBot, mai gida Mohammed Bashir. Ka iya duk harsuna: Hausa, Turanci, Larabci, French. Amsa da yaren da aka tambaye ka."
        data={"model": "llama-3.1-8b-instant",
        r=requests.post(url,headers=headers,json=data,timeout=20).json()
        return r["choices"][0]["message"]["content"] if "choices" in r else str(r)
    except Exception as e: return f"Matsala: {e}"
HTML="""<!DOCTYPE html><html><head><meta name=viewport content='width=device-width, initial-scale=1'><title>MuhammadBot AI</title><style>body{font-family:Arial;padding:20px;max-width:800px;margin:auto;background:#f9f9f9}#chat{height:400px;overflow-y:auto;background:white;padding:15px;border-radius:10px;border:1px solid #ddd}.msg{margin:10px 0;padding:10px 15px;border-radius:15px;max-width:80%}.user{background:#007bff;color:white;margin-left:auto;text-align:right}.bot{background:#e9e9eb;color:black}input{width:70%;padding:12px;border-radius:25px;border:1px solid #ccc}button{padding:12px 20px;border-radius:25px;border:none;background:#007bff;color:white}</style></head><body><h1>🤖 MuhammadBot - Kamar Meta AI</h1><div id=chat><div class=msg bot>Sannu! Ni ne MuhammadBot. Ina amsa Hausa, English, العربية, Français - tambaye ni komai! 👋</div></div><div style='margin-top:15px;display:flex;gap:10px'><input id=q placeholder='Tambayarka...'><button onclick=ask()>Aika</button></div><script>async function ask(){let i=document.getElementById('q'),q=i.value;if(!q)return;let c=document.getElementById('chat');c.innerHTML+=`<div class=msg user>${q}</div>`;i.value='';c.scrollTop=c.scrollHeight;c.innerHTML+=`<div class=msg bot id=t>Ina tunani...</div>`;c.scrollTop=c.scrollHeight;let r=await fetch('/ask?q='+encodeURIComponent(q));let d=await r.json();document.getElementById('t').remove();c.innerHTML+=`<div class=msg bot>${d.answer.replace(/\\n/g,'<br>')}</div>`;c.scrollTop=c.scrollHeight;}</script></body></html>"""
@app.route('/')
def home(): return render_template_string(HTML)
@app.route('/ask')
def ask_ai():
    q=request.args.get('q','')
    return jsonify({"answer":get_ai_answer(q)})
@app.route('/webhook',methods=['GET','POST'])
def webhook():
    if request.method=='GET':
        if request.args.get('hub.verify_token')=="muhammad123": return request.args.get('hub.challenge')
        return "Failed",403
    return "OK",200
if __name__=='__main__': app.run(host='0.0.0.0',port=10000)
