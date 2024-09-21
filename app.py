from flask import Flask, render_template, request
import spacy

app = Flask(__name__)

#load the spaCy NLP model
nlp = spacy.load("en_core_web_sm")

#basic chatbot responses
responses = {
    "greeting": "Hello! how may I assist you with your health today?", 
    "symptom_inquiry": "May you describe your symptoms?", 
    "thanks": "You're welcome!",
    "default": "I didn't understand that, could you rephrase?"
}

def get_response(message):
    """Generate a response based on user input."""
    doc = nlp(message)
    if any(token.lemma_ == "hello" for token in doc):
        return responses["greeting"]
    elif any(token.lemma_ == "thank" for token in doc):
        return responses["thanks"]
    elif any(token.lemma_ == "symptom" or token.lemma_ == "feel" for token in doc):
         return responses["symptoms_inquiry"]
    elif "fever" in message or "cough" in message:
        return "It sounds like you are experiencing a fever or cough. Please monitor your symptoms and consult an expert if they persist"
    elif "headache" in message:
        return "Headaches can be caused by various reasons. Have you tried resting or drinking plenty of water? Don't hesitate to consult a medic if it persists"
    else:
        return responses["default"]
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['message']
    bot_response = get_response(user_message)
    return render_template('index.html', user_message=user_message, bot_response=bot_response)

if __name__ == '__main__':
    app.run(debug=True)