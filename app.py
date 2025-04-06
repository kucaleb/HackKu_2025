#app.py
from flask import Flask, flash, request, redirect, url_for, render_template
from google import genai
from google.genai import types
import PIL.Image
import json
import urllib.request
import os
from werkzeug.utils import secure_filename
 
app = Flask(__name__)
 

 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = 'C:\\Users\\cneil\\CS Projects\\HackKu_2025\\static\\uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        #meals = get_Gemini_Meals(r"static\uploads\\" + filename)
        #print(meals)
        return render_template('index.html')
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/', methods=['GET'])
def get_Gemini_Meals(image_path):
    #Loop through pics in uploads
    image = PIL.Image.open(image_path)

    client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=["You are a chef doing meal prep for a healthy resteraunt. The image will containt coupons from a local store. Your job is to create three healthy meals from some of the items in the coupon and return the meals in the following JSON format. [{meal: Meal Name, Ingredients: {Ingredient_Names: quantities}}, {meal: Meal Name, Ingredients : {Ingredient_Names : quantities}}, {meal : Meal Name, Ingredients : {Ingredient_Names: quantities}}] but instead of writing ... finish the meals. The meals are only inspired from the items in the coupons, so please write out a full list of ingredients, even if the ingredients aren't in the coupons.", image]
    )

    text = response.text
    meals = json.loads(text.removeprefix("```json\n").removesuffix("```"))

    return meals

if __name__ == "__main__":
    app.run(host="0.0.0.0")