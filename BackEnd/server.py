from flask import Flask, request, jsonify
import json
import os
import google.generativeai as genai


# ======================================================
# 🔑 PASTE YOUR GEMINI KEY HERE
# ======================================================
genai.configure(api_key="AIzaSyC1hk5D8Aod0Oyqn4CE5RC5hUVq32sDYEo")

model = genai.GenerativeModel("gemini-pro")


# ======================================================
# SERVE FRONTEND FROM FrontEnd FOLDER
# ======================================================
app = Flask(__name__,
            static_folder="../FrontEnd",
            static_url_path="")

DB_FILE = "data.json"



# ======================================================
# HELPERS
# ======================================================

def load_data():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)



# ======================================================
# ROUTES
# ======================================================

# serve website
@app.route("/")
def home():
    return app.send_static_file("index.html")



# save scores
@app.route("/save", methods=["POST"])
def save_score():
    body = request.json

    data = load_data()
    data.append(body)

    save_data(data)

    return jsonify({"status": "saved"})



# leaderboard
@app.route("/leaderboard")
def leaderboard():
    data = load_data()
    data = sorted(data, key=lambda x: x["score"], reverse=True)
    return jsonify(data[:10])



# ======================================================
# 🔥 REAL GEMINI AI CHATBOT
# ======================================================
@app.route("/chat", methods=["POST"])
def chat():

    message = request.json["message"]

    prompt = f"""
You are SkillMap AI, an intelligent learning assistant.

When students ask:
- analyze weak skills
- create DAILY ROUTINE steps
- recommend FREE courses with links (YouTube, FreeCodeCamp, docs)
- answer technical questions clearly
- give short and helpful replies

If user asks normal questions, answer normally.

Student message:
{message}
"""

    response = model.generate_content(prompt)

    return jsonify({"reply": response.text})



# ======================================================
# RUN
# ======================================================
if __name__ == "__main__":
    app.run(debug=True)
