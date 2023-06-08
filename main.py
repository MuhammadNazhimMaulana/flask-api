from flask import Flask, request, render_template, jsonify
from flask_restful import Resource, Api
from flask.views import View
from flask_cors import CORS
import pandas as pd 
import requests
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import os

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

class MainView(View):
    def dispatch_request(self):
         return render_template("index.html")

class Predict(Resource):
    def get(self):
        return {"error":"Invalid Method."}

    def post(self):
        try:
            # Load Dataset
            ds = pd.read_excel('Words_Newest_2.0.xlsx', engine='openpyxl')

            # Remove Unnamed Column
            ds = ds.loc[:,~ds.columns.str.match("Unnamed")]

            # Fixes
            ds.dropna(subset=['Skor'], inplace=True)

            # Change Skor to Integer
            ds['Skor'] = ds['Skor'].astype(int)
            X_train, X_test, y_train, y_test = train_test_split(ds.Kalimat, ds.Skor, random_state=1)    

            # # Call Vectorizer
            v =CountVectorizer()

            # Fit TRansform
            X_train_count = v.fit_transform(X_train)
            X_test_count = v.transform(X_test)

            # Import Logreg
            from sklearn.linear_model import LogisticRegression

            # Variabel Logreg
            logreg = LogisticRegression()

            # Fit
            logreg.fit(X_train_count, y_train)

            # Get Request Data
            data = request.form['kalimat'] 

            if request.method == 'POST':
                    # Transform Sent Word
                    vect = v.transform([data])

                    # Predict
                    my_prediction = logreg.predict(vect)
                    # print(my_prediction[0])
                    # Result
                    return jsonify(my_prediction.tolist()[0])

        except requests.exceptions.HTTPError as errh:
            # return {'error': errh}
            print(errh)

# View
app.add_url_rule('/', view_func=MainView.as_view(name='index'))

# API
api.add_resource(Predict,'/predict')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)