import os
import torch
from app import app, db
from app.models import Image
from app.utils import CNN, predict, prepare_image
from app.forms import UploadImageForm
from flask import render_template, flash, redirect, request, url_for
from PIL import Image
from werkzeug.utils import secure_filename


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'RouSage'}
    posts = [
        {
            'author': {'username': 'RouSage'},
            'body': 'Post 1'
        },
        {
            'author': {'username': 'Rous'},
            'body': 'Test Post 2'
        }
    ]

    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadImageForm()
    print(app.static_url_path)
    if request.method == 'POST':
        if form.validate_on_submit():
            f = form.image.data
            img_filename = secure_filename(f.filename)
            # Save image to the disk
            f.save(os.path.join(app.static_folder,
                                'img', secure_filename(f.filename)))

            # Add a new Image entity to the database
            image = Image(path=img_filename)
            db.session.add(image)
            db.session.commit()

            flash("File '{}' uploaded!".format(img_filename))

            return redirect(url_for('index'))

    return render_template('upload.html', title='Upload Image', form=form)


@app.route('/predict/<string:img_path>')
def predict(img_path):
    # Load exesting model to CPU and set model to evaluation mode
    net = CNN()
    net.load_state_dict(torch.load(
        "./trained_models/net_15e_086acc.pt", map_location="cpu"))
    net.eval()

    # Prepare the image for prediction
    img = Image.open("./test_images/cat_1.jpg")
    test_img = prepare_image(img)

    # Predict the image's class
    predicted, probs = predict(net, test_img)
