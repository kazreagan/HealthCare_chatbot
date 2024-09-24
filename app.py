from flask import Flask, render_template, request, jsonify
import spacy

app = Flask(__name__)

#load the spaCy NLP model
nlp = spacy.load("en_core_web_sm")

#basic chatbot responses
responses = {
    "greeting": "Hello! how may I assist you with your health today?", 
    "symptom_inquiry": "May you describe your symptoms?", 
    "headache": "Headaches can be caused by various reasons. Have you tried resting or drinking plenty of water? Don't hesitate to consult a medic if it persists.",
    "fever": "Fever is your body's response to infection. Make sure you stay hydrated and rest. If your temperature remains high, seek medical attention.",
    "cough": "Coughing can be caused by allergies, a cold, or something more serious. If it's persistent, especially with difficulty breathing, consult a healthcare provider.",
    "stomach ache": "Stomach aches can result from indigestion, gas or something more serious. Try eating bland food and drinking water. If the pain is sharp or prolonged, consult a doctor.",
    "fatigue": "Fatigue could be due to lack of sleep, stress, or even dehydration. Make sure to rest and drink enough water. If it continues, a doctor may need to check for underlying issues.",
    "cold": "For a cold, drink lots of fluids, rest and consider over-the-counter remedies for symptoms. It should improve in a few days, but consult a doctor if it worsens.",
    "back pain": "Back pain can be due to poor posture or strain. Try gentle stretching and resting. If the pain persists or gets worse, consult a doctor.",
    "sore throat": "A sore throat can be a sign of a cold or infection. Drink warm liquids and consider throat lozenges. If it gets worse, visit a healthcare provider.",
    "dizziness": "Dizziness can be caused by dehydration or low blood pressure. Try sitting or lying down and drink water. If it happens frequently, consult a doctor.",
    "insomnia": "Insomnia could result from stress or an irregular sleep schedule. Try relaxation techniques before bed, like deep breathing or reading. Persistent issues should be discussed with a doctor.",
    "chest pain": "Chest pain is serious. It could be related to heart issues or something less critical. Regardless, if you experience chest pain, seek immediate medical attention.",
    "skin rash": "A skin rash can be caused by allergies, infections, or irritants. Try using a mild soap and moisturizer. If it spreads or worsens, consult a doctor.",
    "vomiting": "Vomiting can be a symptom of food poisoning, a virus, or other conditions. Try staying hydrated with small sips of water. If it persists, consult a healthcare provider.",
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
    elif "headache" in message:
        return "Headaches can be caused by various reasons. Have you tried resting or drinking plenty of water? Don't hesitate to consult a medic if it persists."
    elif "fever" in message:
        return "Fever can be a sign of infection or other health issues. Monitor your temperature and stay hydrated. If it gets too high, seek medical advice."
    elif "stomach ache" in message:
        return "Stomach aches can result from indigestion, gas or something more serious. Try eating bland food and drinking water. If the pain is sharp or prolonged, consult a doctor."
    elif "cold" in message:
        return "For a cold, drink lots of fluids, rest and consider over-the-counter remedies for symptoms. It should improve in a few days but consult a doctor if it worsens."
    elif "cough" in message:
        return "Coughing can be caused by allergies, a cold or something more serious. If it's persistent, especially with difficulty breathing, consult a healthcare provider."
    elif "vomiting" in message:
        return "Vomiting can be a symptom of food poisoning, a virus or other conditions. Try staying hydrated with small sips of water. If it persists, consult a healthcare provider."
    elif "diarrhea" in message:
        return "Diarrhea can be caused by infections, food or other health issues. Drink plenty of fluids to prevent dehydration and see a doctor if symptoms persist."
    else:
        return responses["default"]
    
@app.route('/')
def index():
    return render_template('index.html')

#route to handle AJAX requests
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['message']
    bot_response = get_response(user_message)
    
    #default bot response
    # bot_response = responses.get(user_message, "I'm sorry I don't have an answer for that, Please consult a medic.")
    #return a JSON response
    return jsonify({'user_message': user_message, 'bot_response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)