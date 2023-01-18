from flask import Flask, render_template, request, jsonify, make_response
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
            predictions = predict(review_text)  # dataframe of recommendations
        except Exception as e:
            return render_template('index.html', error=e)

        predictions = predictions.drop(columns='lyrics').to_html(table_id='recommendations')

        # finally render template with correct sentiment
        return render_template('index.html', prediction=predictions)

    # this is the 'home' route with a get request (no form submitted)
    else:
        return render_template('index.html')


@app.route('/api/recommend/v1', methods=['POST'])
def predict_api():
    """
    JSON Response for requests over api
    waiting:
        '{"input": "text"}'
    returning:

    """

    # when the form is submitted this route gets a POST request
    if request.method == 'POST':
        lyrics = request.json["input"]

        # if no input provided
        if not lyrics.strip():
            return jsonify({'prediction': "", 'error': "No input text."}), 400

        # catch any error during prediction
        try:
            predictions = predict(lyrics)
        except Exception as _:
            return jsonify({'recommendations': "", 'error': "Something wrong in server."}), 500

        return predictions.drop(columns='lyrics').to_json()
    elif request.method == 'OPTIONS':
        # temporary solution for cross site resource sharing
        # later, a library can be used.
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


if __name__ == '__main__':
    app.run(debug=True)
