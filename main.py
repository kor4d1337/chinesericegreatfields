from flask import Flask, render_template, request
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

app = Flask(__name__)

sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model = "blanchefort/rubert-base-cased-sentiment"
)

tokenizer = AutoTokenizer.from_pretrained("ai-forever/rugpt3medium_based_on_gpt2")
model = AutoModelForCausalLM.from_pretrained("ai-forever/rugpt3medium_based_on_gpt2")

def generate_recommendation(mood):
    prompt = (f"Посоветуй один популярный сериал для человека, у которого {mood} настроение."
              f"Назовит только сериал и кратко объясни почему.")
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_length = 50,
        do_sample = False,
        top_p = 0.9,
        temperature = 1
    )
    text = tokenizer.decode(outputs[0], skip_special_tokens = True)
    return text[len(prompt):].strip()

@app.route("/", methods=["GET", "POST"])
def index():
    recommendation = ""
    user_text = ""

    if request.method == "POST":
        user_text = request.form["message"]

        result = sentiment_analyzer(user_text)[0]
        label = result["label"]

        if label == "POSITIVE":
            mood = "хорошее"
        elif label == "NEGATIVE":
            mood = "плохое"
        else:
            mood = "нейтральное"
        
        ai_text = generate_recommendation(mood)
        recommendation = f"Настроение: {mood}. <br>Рекомендация: {ai_text}"

    return render_template("index.html", recommendation=recommendation, user_text=user_text)

if __name__ == "__main__":
    app.run(debug=True)