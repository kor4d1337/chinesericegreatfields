from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)

sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model = "blanchefort/rubert-base-cased-sentiment"
)

@app.route("/", methods=["GET", "POST"])
def index():
    recommendation = ""
    user_text = ""

    if request.method == "POST":
        user_text = request.form["message"]

        result = sentiment_analyzer(user_text)[0]
        label = result["label"]

        if label == "POSITIVE":
            recommendation = "Good, + 15 social credit <img class=\"SocialRating\" src=\"https://i.redd.it/nzxcf6vxle081.png\">"
        elif label == "NEGATIVE":
            recommendation = "1.. 2.. 3.. For the Chinese 槍射擊 <img class=\"SocialRating\" src=\"https://static.vecteezy.com/system/resources/thumbnails/049/188/191/small/man-aims-through-the-sight-of-combat-metal-pistol-to-hit-the-target-photo.jpg\">"
        else:
            recommendation = "cookies <img class=\"SocialRating\" src=\"https://cs4.pikabu.ru/post_img/big/2015/09/17/6/1442476979_1461212557.jpg\">"
        
    return render_template("index.html", recommendation=recommendation, user_text=user_text)

if __name__ == "__main__":
    app.run(debug=True)