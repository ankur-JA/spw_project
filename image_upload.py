from flask import Flask, render_template, request, session
import os
import shutil
from werkzeug.utils import secure_filename
import pymongo
# *** Backend operation
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["school"]
mycol = mydb["students"]
# WSGI Application
# Defining upload folder path
UPLOAD_FOLDER = os.path.join('static', 'uploads')
# # Define allowed files
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Provide template folder name
# The default folder name should be "templates" else need to mention custom folder name for template path
# The default folder name for static files should be "static" else need to mention custom folder for static path
app = Flask(__name__, template_folder='template', static_folder='static')
# Configure upload folder for Flask application
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define secret key to enable session
app.secret_key = 'This is your secret key to utilize session in Flask'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/',  methods=("POST", "GET"))
def uploadFile():

    path1 = r"static/uploads/"
    dir = os.listdir(path1)
    for file_name in os.listdir(path1):
        file = path1 + file_name
        os.remove(file)

    if os.path.exists(r"static/annotated/exp/"):
        path2 = r"static/annotated/exp/"
        dir2=os.listdir(path2)
        for file_name in os.listdir(path2):
            file = path2 + file_name
            os.remove(file)
        os.rmdir(path2)

    path3=r"static/cropped/"
    dir3 = os.listdir(path3)
    for file_name in os.listdir(path3):
        file = path3 + file_name
        os.remove(file)

    if request.method == 'POST':
        # Upload file flask
        uploaded_img = request.files['uploaded-file']
        # Extracting uploaded data file name
        img_filename = secure_filename(uploaded_img.filename)
        # Upload file to database (defined uploaded folder in static path)
        uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        # Storing uploaded file path in flask session
        session['uploaded_img_file_path'] = os.path.join(
            app.config['UPLOAD_FOLDER'], img_filename)
        return render_template('index2.html')


@app.route('/show_image')
def displayImage():
    import detect
    a=detect.run()
    print(a)
    
    import shutil
    filelist=os.listdir()
    for file in filelist:
        if (file.endswith(".png")):
            dest=r"static/cropped/"
            shutil.move(file,dest)
    # Retrieving uploaded file path from session
    #img_file_path = session.get('C:/Users/DELL/Desktop/Image_upload/yolov5/runs/detect/exp/', None)
    # Display image in Flask application web page
    return render_template('index3.html')


@app.route('/newstudent')
def newstudent():
    
    return render_template('newstudent.html')


path1 = r"static/uploads/"
dir = os.listdir(path1)
for file_name in os.listdir(path1):
    file = path1 + file_name
    os.remove(file)

if os.path.exists(r"static/annotated/exp/"):
    path2 = r"static/annotated/exp/"
    dir2=os.listdir(path2)
    for file_name in os.listdir(path2):
        file = path2 + file_name
        os.remove(file)
    os.rmdir(path2)

path3=r"static/cropped/"
dir3 = os.listdir(path3)
for file_name in os.listdir(path3):
    file = path3 + file_name
    os.remove(file)


if __name__ == '__main__':
    app.run(debug=True)