from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from scr.pipeline.predict_pipeline import CustomData, PredictPipeline

application = Flask(__name__)
app = application


## Route for home page
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')

    else:
        try:
            # ✅ Ensure form field names match HTML input names exactly
            data = CustomData(
                gender=request.form.get('gender'),
                race_ethnicity=request.form.get('ethnicity'),
                parental_level_of_education=request.form.get('parental_level_of_education'),
                StudyHoursPerDay=float(request.form.get('study_hours_per_day')),
                AttendancePercentage=float(request.form.get('attendance_percentage')),
                NumSubjects=float(request.form.get('number_of_subjects')),
                test_preparation_course=request.form.get('test_preparation_course'),
                reading_score=float(request.form.get('reading_score')),
                writing_score=float(request.form.get('writing_score'))
            )

            # ✅ Convert to DataFrame
            pred_df = data.get_data_as_data_frame()
            print(pred_df)
            print("Before Prediction")

            # ✅ Run prediction pipeline
            predict_pipeline = PredictPipeline()
            print("Mid Prediction")
            results = predict_pipeline.predict(pred_df)
            print("After Prediction")

            # ✅ Display result
            return render_template('home.html', results=round(results[0], 2))

        except Exception as e:
            # Debug output to help find the issue
            return render_template('home.html', results=f"Error: {str(e)}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
      