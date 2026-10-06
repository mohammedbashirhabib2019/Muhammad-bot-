from flask import Flask, request, render_template_string
import datetime

app = Flask(__name__)

HTML = """
<h1>MuhammadBot is LIVE! ✅</h1>
<p>Owner: Mohammed Bashir</p>
<p>Time: {{time}}</p>
<p>WhatsApp: /webhook | Telegram: /telegram | Facebook: /webhook</p>
<p>Status: Ready for all platforms</p>
"""

@app.route('/')
def home():
    now = datetime.datetime.now()
    return render_template_string(HTML, time=now)

# --- WHATSAPP & FACEBOOK WEBHOOK ---
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Facebook/WhatsApp suna duba token
        verify_token = request.args.get('hub.verify_token')
        if verify_token == "muhammad123":
            return request.args.get('hub.challenge')
        return "Verification failed", 403
    else:
        data = request.get_json()
        print("WHATSAPP/FB MESSAGE:", data)
        # Nan ne zaka saka code na amsa sako
        return "OK", 200

# --- TELEGRAM WEBHOOK ---
@app.route('/telegram', methods=['POST'])
def telegram_bot():
    data = request.get_json()
    print("TELEGRAM MESSAGE:", data)
    # Nan ne zaka saka code na Telegram
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
