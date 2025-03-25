from flask import Flask, request, jsonify, send_from_directory
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

RPM_SYSTEM_PROMPT = """You are a message diagnostics agent based on the Reality Processing Model (RPM).

Your task is to analyze any message or piece of writing for the following:
1. Rhetorical tone and structure: Is the message assertive, suggestive, conciliatory, narrative, data-driven?
2. Epistemic structure: Does it rely on shared consensus? Is it making a faith-based leap? Is it ambiguous or over-structured?
3. Stability index: How likely is the message to misfire, invite capture, or resist reconstitution?
4. Consensus orientation: Does this message seek to reinforce existing consensus, challenge it, or collapse it?
5. Capture risk: Is the message vulnerable to being reinterpreted or weaponized by adversarial audiences?

Return this format:

Message Summary:
...

Epistemic Diagnosis:
...

Stability Score (0–100):
Capture Risk: Low / Medium / High

Key Observations:
- ...
- ...
- ...

Suggestions for Improvement:
1. ...
2. ...
3. ...
"""

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/diagnose", methods=["POST"])
def diagnose():
    data = request.get_json()
    message = data.get("message")

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": RPM_SYSTEM_PROMPT},
            {"role": "user", "content": f"Message: {message}"}
        ]
    )

    return jsonify({"analysis": response.choices[0].message["content"]})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)