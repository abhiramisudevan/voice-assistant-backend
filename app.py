from flask import Flask, request, jsonify
from flask_cors import CORS
import wikipedia

app = Flask(__name__)
CORS(app)

def clean_query(query):
    query = query.lower()
    for phrase in ["who is", "what is", "tell me about", "define"]:
        query = query.replace(phrase, "")
    return query.strip()

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    print("Received data:", data)       # Debug print
    query = data.get("query")
    print("Query:", query)              # Debug print

    if not query:
        return jsonify({"answer": "No input received"})

    topic = clean_query(query)
    try:
        result = wikipedia.summary(topic, sentences=2)
        print("Answer:", result)        # Debug print
        return jsonify({"answer": result})
    except Exception as e:
        print("Wikipedia error:", e)   # Debug print
        return jsonify({"answer": "Sorry, I couldn’t find that."})

@app.route("/", methods=["GET"])
def home():
    return "Voice Assistant Backend Running"

if __name__ == "__main__":
    app.run(debug=True)