from flask import Flask, render_template, request, jsonify, make_response, send_from_directory
from ..MRS.predict import predict
import pandas as pd
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow import Schema, fields
from werkzeug.utils import secure_filename
import json

app = Flask(__name__, template_folder='./swagger/templates')

spec = APISpec(
    title='flask-api-swagger-doc',
    version='1.0.0',
    openapi_version='3.0.2',
    plugins=[FlaskPlugin(), MarshmallowPlugin()]
)


@app.route('/api/swagger.json')
def create_swagger_spec():
    return jsonify(spec.to_dict())


@app.route('/', methods=['GET', 'POST'])
def recommend():
    """View that handles the default get request and the post request when
    a form is submitted."""

    # when the form is submitted this route gets a POST request
    if request.method == 'POST':
        review_text = request.form["lyric_input"]

        # if no input provided
        if not review_text.strip():
            return render_template('base.html', error="No text provided.")

        # catch any error during prediction
        try:
            predictions = predict(review_text)  # dataframe of recommendations
        except Exception as e:
            return render_template('base.html', error=e)

        predictions = predictions.drop(columns='lyrics').to_html(table_id='recommendations')

        # finally render template with correct sentiment
        return render_template('base.html', prediction=predictions)

    # this is the 'home' route with a get request (no form submitted)
    else:
        return render_template('base.html')


class PredictionResponseSchema(Schema):
    track_name = fields.Str()
    track_artist = fields.Str()
    track_album_name = fields.Str()
    track_id = fields.Str()
    tags = fields.Int()
    #id = fields.Str()


class PredictionListResponseSchema(Schema):
    pred_list = fields.List(fields.Nested(PredictionResponseSchema))

class InputLyricsSchema(Schema):
    input = fields.Str()

@app.route('/api/recommend/v1', methods=['POST'])
def predict_api():
    """
    Post some lyrics
    ---
    post:
        requestBody:
            description: lyrics without new lines
            required: true
            content:
                application/json:
                    schema: InputLyricsSchema

        description: post lyric data and get recommendations
        responses:
            200:
                description: a list of recommendations and other metadata like artist and album name
                content:
                    application/json:
                        schema: PredictionListResponseSchema


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
        except Exception as e:
            return jsonify({'recommendations': e, 'error': "Something wrong in server."}), 500

        preds = json.loads(predictions.drop(columns='lyrics').to_json(orient='index'))
        # print('======================================================================')
        # try:
        #     print(preds.values())
        # except Exception as e2:
        #     print(preds)
        #     print(e2)
        preds_list = [value for value in preds.values()]
        # print('======================================================================')
        # print(preds_list)
        return PredictionListResponseSchema().dump({'pred_list': preds_list})
        # return preds
    elif request.method == 'OPTIONS':
        # temporary solution for cross site resource sharing
        # later, a library can be used.
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


with app.test_request_context():
    spec.path(view=predict_api)
    print(spec.to_dict())


@app.route('/docs')
@app.route('/docs/<path:path>')
def swagger_docs(path=None):
    if not path or path == 'index.html':
        print('*************************')
        return render_template('index.html', base_url='/docs')
    else:
        return send_from_directory('./swagger/static', secure_filename(path))


if __name__ == '__main__':
    app.run(debug=True)
