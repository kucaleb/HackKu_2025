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
def get_Gemini_Meals():
    prompt = "You are a chef doing meal prep for a healthy resteraunt. The images will containt coupons from a local store. Your job is to create three healthy main courses from some of the items in the coupons and return the meals in the following JSON format. [{meal: Meal Name, Ingredients: {Ingredient_Names: quantities}}, {meal: Meal Name, Ingredients : {Ingredient_Names : quantities}}, {meal : Meal Name, Ingredients : {Ingredient_Names: quantities}}]. The meals are only inspired from the items in the coupons, so please write out a full list of ingredients, even if the ingredients aren't in the coupons. RESPOND ONLY WITH THE JSON"
    content = [prompt]
    dir_path = r"static\uploads"
    for file in os.scandir(r"static\uploads"):
        image = PIL.Image.open(file.path)
        content.append(image)
    
    client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=content,
    )

    text = response.text.removeprefix("```json\n").removesuffix("```")
    meals = json.loads(text)

    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

    return meals

if __name__ == "__main__":
    app.run(host="0.0.0.0")