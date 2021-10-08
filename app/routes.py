import os
import uuid

import torch
from flask import redirect, render_template, request, url_for
from flask_babel import _
from PIL import Image as pil

from app import app, db, model
from app.forms import UploadImageForm
from app.models import Classes, Image, Plot, Prediction
from app.utils import CLASSES, plot_probabilities, predict, prepare_image


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
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
    return render_template('index.html', title=_('Home'), form=form, latest=get_latest_predictions(), c=CLASSES)


@app.route('/prediction/<int:img_id>')
def prediction(img_id):
    # Get an Image entity from the database
    image = Image.query.get_or_404(img_id)

    if image.prediction == None:
        # Predict the image's class
        img = pil.open(os.path.join(app.static_folder, 'img', image.path))
        img = prepare_image(img)
        predicted, probs = predict(model=model, x=img)

        # Get Class from DB
        pred_class = Classes.query.get(predicted.item() + 1)
        # Create new Prediction entity
        prediction_data = Prediction(probability=torch.max(probs, dim=0)[
            0].item(), class_id=pred_class.id, image_id=image.id)
        # Create new Plot entity
        plot_filename = image.path.split('.')[0] + '_plot.png'
        plot_probabilities(probs, os.path.join(app.static_folder, 'img', plot_filename))
        plot = Plot(path=plot_filename, image_id=image.id)

        # Add all new entities
        db.session.add(prediction_data)
        db.session.add(plot)
        db.session.commit()

    result = {
        'img_path': 'img/' + image.path,
        'predicted': CLASSES[image.prediction.class_id - 1],
        'prob': image.prediction.probability * 100,
        'plot_path': 'img/' + image.plot.path
    }

    return render_template('predict.html', title=_('Prediction'), result=result, form=UploadImageForm())


def get_latest_predictions():
    return Image.query.filter(
        Image.prediction != None).order_by(Image.created.desc())[:3]
