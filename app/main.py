from flask import Flask, request, jsonify, url_for, send_file
from flask_cors import CORS
import subprocess
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = "../datasets/uploads/test"
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
    
ALLOWED_EXTENSIONS = set(["jpg", "png", "jpeg"])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/predict", methods=['GET', 'POST'])
def predict():
    print("starts")
    if request.method == 'GET':
            return send_file("..\\results\\human_pix2pix\\test_latest\\images\\img_fake_B.png", mimetype='image/jpeg')


    if request.method == 'POST':
        #check if file is in post request
        print(request.files)
        if 'img' not in request.files:
            print('No file part')
            return jsonify({"result" : 1})
        file = request.files['img']
        # if user does not select file, browser also
        # submit a empty part without filename
        print("found")

        if file.filename == '':
           print('No selected file')
           return redirect(request.url)

        if file and allowed_file(file.filename):
            # Create renaming system;
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # TODO: Get rid of subprocess for resize-image
        print("resize done")
        # TODO: add some comments here as well
        subprocess.run(["python", "resize-image.py"])
        print("resize done")
        subprocess.run(["python", "./test.py", "--dataroot", "./datasets/uploads", "--name",  "human_pix2pix", "--model", "pix2pix", "--direction", "BtoA", "--batch_size", "256", "--gpu_ids", "-1"], cwd = "C:\\Users\\smile\\00_repos\\susanna-server\\" )

    return jsonify({"process": "ok"})
# @app.route("/get-prediction/<imgName>")


if __name__ == "__main__":
    app.run(debug = true)