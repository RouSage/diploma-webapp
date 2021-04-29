import os
import uuid
from os import path

import cv2
import torch
from flask import redirect, render_template, request, url_for
from flask_babel import _
from PIL import Image as pil

from app import app, db, model
from app.forms import UploadImageForm
from app.models import Classes, Image, Prediction
from app.tester import Tester
from app.yolov3.config import yolov3_config_voc as cfg


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
    return render_template('index.html', title=_('Home'), form=form, latest=get_latest_predictions(), c=cfg.DATA['CLASSES'])


@app.route('/prediction/<int:img_id>')
def prediction(img_id):
    # Get an Image entity from the database
    image = Image.query.get_or_404(img_id)

    if image.prediction == None:
        # Predict the image's class
        img = cv2.imread(os.path.join(app.static_folder, 'img', image.path))
        pred_img, predicted, probs = Tester(model=model, img=img).test()
        # predicted, probs = predict(model=model, x=img)

        # Save pred_img to the disk
        pred_img_filename = f"{image.path.split('.')[0]}_pred.{image.path.split('.')[1]}"
        cv2.imwrite(os.path.join(app.static_folder,
                    'img', pred_img_filename), pred_img)

        # Add pred_img to the DB
        image = Image(path=pred_img_filename)

        # Get all Class from DB
        classes = Classes.query.all()
        # Create new Prediction entity for each object on the given image
        for prob, pred in zip(probs, predicted):
            prediction_data = Prediction(
                probability=prob, class_id=classes[pred].id, image_id=image.id)
            db.session.add(prediction_data)
        # Create new Plot entity
        # plot = Plot(path=plot_probabilities(probs, os.path.join(
        #     app.static_folder, 'img', image.path.split('.')[0] + '_plot.png')), image_id=image.id)

        # Add all new entities
        # db.session.add(plot)
        db.session.add(image)
        db.session.commit()

    result = {
        'img_path': 'img/' + image.path,
        'predicted': cfg.DATA['CLASSES'][image.prediction.class_id - 1],
        'prob': image.prediction.probability * 100,
        'plot_path': 'img/' + image.plot.path
    }

    return render_template('predict.html', title=_('Prediction'), result=result, form=UploadImageForm())


def get_latest_predictions():
    return Image.query.filter(
        Image.prediction != None).order_by(Image.created.desc())[:3]
