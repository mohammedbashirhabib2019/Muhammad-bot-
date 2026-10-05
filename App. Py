from flask import Flask, render_template_string
import datetime
app = Flask(__name__)
HTML = """
<h1>MuhammadBot is LIVE!</h1>
<p>Owner: Mohammed Bashir</p>
<p>Time: {{time}}</p>
"""
@app.route('/')
def home():
    now = datetime.datetime.now()
    return render_template_string(HTML, time=now)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
