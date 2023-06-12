from flask import Blueprint, request, jsonify
import pandas as pd 

prediction_bp = Blueprint('prediction', __name__)
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import requests

@prediction_bp.route('/predict', methods = ['POST'])
def post():
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
        logreg = LogisticRegression(penalty='elasticnet', solver='saga', l1_ratio=0.99, C=0.8)

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