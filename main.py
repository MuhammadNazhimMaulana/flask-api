from flask import Flask, request, render_template, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
import pandas as pd 
import requests
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from blueprints.home.home import home_bp
from blueprints.prediction.prediction import prediction_bp
import os

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

# Register
app.register_blueprint(home_bp)
app.register_blueprint(prediction_bp)

if __name__ == "__main__":
    from waitress import serve
    port = int(os.environ.get("PORT", 5000))
    serve(app, host='0.0.0.0', port=port)