import os
import uuid
import torch
from PIL import Image as pil
from flask import redirect, render_template, request, url_for
from app import app, db, model
from app.forms import UploadImageForm
from app.models import Image
from app.utils import predict, prepare_image, CLASSES


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadImageForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            f = form.image.data
            img_filename = str(uuid.uuid4()) + '.' + f.filename.split('.')[1]

            # Save image to the disk
            f.save(os.path.join(app.static_folder, 'img', img_filename))

            # Add a new Image entity to the database
            image = Image(path=img_filename)
            db.session.add(image)
            db.session.commit()

            return redirect(url_for('prediction', img_id=image.id))

    return render_template('upload.html', title='Upload Image', form=form)


@app.route('/prediction/<int:img_id>')
def prediction(img_id):
    # Get an Image entity from the database
    image = Image.query.get_or_404(img_id)

    # Predict the image's class
    img = pil.open(os.path.join(app.static_folder, 'img', image.path))
    img = prepare_image(img)
    predicted, probs = predict(model=model, x=img)

    # Update the image entity
    image.predicted = CLASSES[predicted]
    image.probability = torch.max(probs, dim=0)[0].item()
    db.session.commit()

    return render_template('predict.html', img_path='img/' + image.path,
                           predicted=image.predicted, prob=image.probability * 100, probs=probs * 100)
