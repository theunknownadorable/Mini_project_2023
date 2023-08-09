from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
import time
import pickle
import pandas as pd

app = Flask(__name__)

# Configure MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'login_details'

mysql = MySQL(app)

# Load the trained Randomforest model
model = pickle.load(open("random_forest_model.pkl", "rb"))

# Mapping dictionaries for label encoding
gender_mapping = {'Female': 0, 'Male': 1, 'Others':2}
board_mapping= { 'CBSE':0,'ICSE/ISC':1,'State':2}
study_scale_mapping= {'1':0,'2':1,'3':2,'4':3,'5':4}
extra_activity_mapping={'No':0,'Yes':1}
learning_type_mapping={'Combination of both the above options':0,'Direct (Teacher and student interaction)':1,'YouTube videos or other references only':2}
qn_habit_mapping={'Maybe':0,'No':1,'Yes':2}
Genrl_type_mapping={'a combination of both':2,'Listener (one who like to listen more and engage with people)':0,'Talker (one who likes to talk more and engage with people)':1}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        Email = request.form['username']
        Password = request.form['password']

        # Verify user credentials
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM `login` WHERE Email = %s AND Password = %s"
        cursor.execute(query, (Email, Password))
        result = cursor.fetchone()

        if result is not None:
            # User authenticated successfully
            time.sleep(1)
            return render_template('landing.html')
        else:
            # Invalid credentials
            error = 'Invalid username or password.'
            return render_template('index.html', error=error)

    return render_template('index.html')


@app.route('/landing', methods=['POST'])
def landing():
    if request.method == 'POST':
        Email = request.form['Email']
        Password = request.form['Password']

        # Insert user data into the database
        cursor = mysql.connection.cursor()
        query = "INSERT INTO `login` (Email, Password) VALUES (%s, %s)"
        cursor.execute(query, (Email, Password))
        mysql.connection.commit()

        # Redirect to a success page or any other desired page
        return render_template('landing.html')

    return render_template('index.html')

@app.route('/cgpa')
def cgpa():
    time.sleep(1)
    return render_template('cgpa.html')

@app.route('/help')
def help():
    time.sleep(1)
    return render_template('help.html')

@app.route('/logout')
def logout():
    time.sleep(2)
    return render_template('index.html')


@app.route('/predict2')
def predict2():
    time.sleep(1)
    return render_template('grade_predict.html')

@app.route('/predict1', methods=['POST'])
def predict1():
    data = request.get_json(force=True)
    age = float(data['Age'])
    gender = gender_mapping[data['Gender']]
    board = board_mapping[data['Board']]
    std_tym = float(data['std_tym'])
    study_rate = study_scale_mapping[data['study_rate']]
    extra_activity = extra_activity_mapping[data['extra_activity']]
    no_backpaper = float(data['no_backpaper'])
    no_attend_paper = float(data['no_attend_paper'])
    learning_type = learning_type_mapping[data['learning_type']]
    family_time = float(data['family_time'])
    Qn_habit = qn_habit_mapping[data['Qn_habit']]
    Genrl_type = Genrl_type_mapping[data['Genrl_type']]

    

    # Preprocess the input data
    input_data = pd.DataFrame({
        'Gender': [gender],
        'Age': [age],
        'Board': [board],
        'std_tym': [std_tym],
        'study_scale': [study_rate],
        'extra_activity': [extra_activity],
        'no_backpaper': [no_backpaper],
        'no_attend_paper': [no_attend_paper],
        'learning_type': [learning_type],
        'family_time': [family_time],
        'Qn_habit': [Qn_habit],
        'Genrl_type': [Genrl_type]
    })

    # Make the prediction
    prediction = model.predict(input_data)[0]

            #Insert the input and prediction values into the database
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO `prediction` (Age, Gender, Board, std_tym, study_rate, extra_activity, no_attend_paper, no_backpaper, learning_type, family_time, Qn_habit, Genrl_type, predictionText) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
               (age, gender, board, std_tym, study_rate, extra_activity, no_attend_paper, no_backpaper, learning_type, family_time, Qn_habit, Genrl_type, prediction))
    mysql.connection.commit()
    cur.close()


    response = {'predict': int(prediction)}
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
