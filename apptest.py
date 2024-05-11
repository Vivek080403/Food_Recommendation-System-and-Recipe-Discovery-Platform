import os
import re
from flask import Flask, render_template, request
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import OpenAI
from flask import Flask, render_template, redirect, url_for, request

os.environ['OPENAI_API_KEY'] = 'sk-proj-l7gak13g0o8HT2zyhWYZT3BlbkFJgFuC6S2XVHEhNJSn3x4w'
app = Flask(__name__)

llm_resto = OpenAI(temperature=0.6)
prompt_template_resto = PromptTemplate(
    input_variables=['age', 'gender', 'weight', 'height', 'veg_or_nonveg', 'desired_body-type', 'region', 'nutritional_aspiration', 'foodtype'],
    template="Diet Recommendation System:\n"
             "I want you to recommend 6 restaurants names, 6 breakfast names, 5 dinner names, and 6 workout names, "
             "based on the following criteria:\n"
             "Person age: {age}\n"
             "Person gender: {gender}\n"
             "Person weight: {weight}\n"
             "Person height: {height}\n"
             "Person veg_or_nonveg: {veg_or_nonveg}\n"
             "Person desired_body_type: {desired_body_type}\n"
             "Person region: {region}\n"
             "Person nutritional_aspiration: {nutritional_aspiration}\n"
             "Person foodtype: {foodtype}."
)


app = Flask(__name__, static_folder='static')
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/recipes')
def recipes():
    return render_template('recipes.html')
@app.route('/login', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        # Check login credentials (replace with your authentication logic)
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            # Redirect to the index page upon successful login
            return redirect(url_for('index'))
        else:
            message = "Incorrect username or password. Please try again."
    return render_template('login.html', message=message)
@app.route('/recommender')
def recommender():
    return render_template('home.html')

@app.route('/recommend', methods=['POST'])


def recommend():
    if request.method == "POST":
        age = request.form['age']
        gender = request.form['gender']
        weight = request.form['weight']
        height = request.form['height']
        veg_or_noveg = request.form['veg_or_nonveg']
        desired_body_type = request.form['desired_body_type']
        region = request.form['region']
        nutritional_aspiration = request.form['nutritional_aspiration']
        foodtype = request.form['foodtype']

        chain_resto = LLMChain(llm=llm_resto, prompt=prompt_template_resto)
        input_data = {'age': age,
                              'gender': gender,
                              'weight': weight,
                              'height': height,
                              'veg_or_nonveg': veg_or_noveg,
                              'desired_body_type': desired_body_type,
                              'region': region,
                              'nutritional_aspiration': nutritional_aspiration,
                              'foodtype': foodtype}
        results = chain_resto.run(input_data)

        # Extracting the different recommendations using regular expressions
        restaurant_names = re.findall(r'Restaurants:(.*?)Breakfast:', results, re.DOTALL)
        breakfast_names = re.findall(r'Breakfast:(.*?)Dinner:', results, re.DOTALL)
        dinner_names = re.findall(r'Dinner:(.*?)Workouts:', results, re.DOTALL)
        workout_names = re.findall(r'Workouts:(.*?)$', results, re.DOTALL)

        # Cleaning up the extracted lists
        restaurant_names = [name.strip() for name in restaurant_names[0].strip().split('\n') if name.strip()]
        breakfast_names = [name.strip() for name in breakfast_names[0].strip().split('\n') if name.strip()]
        dinner_names = [name.strip() for name in dinner_names[0].strip().split('\n') if name.strip()]
        workout_names = [name.strip() for name in workout_names[0].strip().split('\n') if name.strip()]

        return render_template('result.html', restaurant_names=restaurant_names,breakfast_names=breakfast_names,dinner_names=dinner_names,workout_names=workout_names)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)