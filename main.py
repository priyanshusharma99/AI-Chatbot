from flask import Flask, render_template, request, jsonify

try:
    import google.generativeai as genai
except ModuleNotFoundError:
    genai = None

app = Flask(__name__)

# Configure the Gemini API (Replace 'YOUR_API_KEY' with your actual API key)
API_KEY = 'AIzaSyCFfAzyatRu0UdeGjOkPr2b9k4o83KOvlg'
if genai:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-2.5-pro-exp-03-25")
else:
    model = None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"response": "Please enter a message."})

    if not model:
        return jsonify(
            {"response": "Error: Gemini API module not found. Please install 'google-generativeai' package."})

    try:
        response = model.generate_content(user_input)
        reply = response.text if response.text else "I'm sorry, I couldn't understand that."
    except Exception as e:
        reply = f"Error: {str(e)}"

    return jsonify({"response": reply})


if __name__ == '__main__':
    app.run(debug=True)
