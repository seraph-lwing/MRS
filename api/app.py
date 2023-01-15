from flask import Flask, render_template, request
from ..MRS.predict import predict
import pandas as pd


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def recommend():
    """View that handles the default get request and the post request when
    a form is submitted."""

    # when the form is submitted this route gets a POST request
    if request.method == 'POST':
        review_text = request.form["lyric_input"]

        # if no input provided
        if not review_text.strip():
            return render_template('index.html', error="No text provided.")

        # catch any error during prediction
        try:
            predictions = predict(review_text) # dataframe of recommendations
        except Exception as e:
            return render_template('index.html', error=e)

        predictions = predictions.drop(columns='lyrics').to_html(table_id='recommendations')

        # finally render template with correct sentiment
        return render_template('index.html', prediction=predictions)

    # this is the 'home' route with a get request (no form submitted)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run()