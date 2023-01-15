from flask import Flask, render_template, request
from ..music_recommender_system.predict import predict


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def predict():
    """View that handles the default get request and the post request when
    a form is submitted."""

    # when the form is submitted this route gets a POST request
    if request.method == 'POST':
        review_text = request.form["text_input"]

        # if no input provided
        if not review_text.strip():
            return render_template('index.html', error="No text provided.")

        # catch any error during prediction
        try:
            predictions = make_prediction_raw([review_text])
        except Exception as e:
            return render_template('index.html', error=e)

        prediction = 'positive' if predictions[0] == 1 else 'negative'
        # finally render template with correct sentiment
        return render_template('index.html', prediction=prediction)

    # this is the 'home' route with a get request (no form submitted)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run()