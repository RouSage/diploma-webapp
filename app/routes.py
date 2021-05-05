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

    if image.pred_img_path == None:
        # Predict the image's class
        img = cv2.imread(os.path.join(app.static_folder, 'img', image.path))
        pred_img, preds, probs = Tester(model=model, img=img).test()

        # Save pred_img to the disk
        pred_img_filename = f"{image.path.split('.')[0]}_pred.{image.path.split('.')[1]}"
        cv2.imwrite(os.path.join(app.static_folder,
                    'img', pred_img_filename), pred_img)

        # Add pred_img to the image entity
        image.pred_img_path = pred_img_filename

        # Get all classes from DB
        classes = Classes.query.all()
        # Create new Prediction entity for each object on the given image
        for prob, pred in zip(probs, preds):
            prediction_data = Prediction(
                probability=prob, class_id=classes[pred].id, image_id=image.id)
            db.session.add(prediction_data)

        # Add all new entities and commit changes
        db.session.commit()

    predicted = [cfg.DATA['CLASSES'][pred.class_id - 1]
                 for pred in image.prediction]
    probs = [prob.probability * 100 for prob in image.prediction]

    result = {
        'img_path': 'img/' + image.path,
        'predicted': zip(predicted, probs),
        'pred_img_path': 'img/' + image.pred_img_path
    }

    return render_template('predict.html', title=_('Prediction'), result=result, form=UploadImageForm())


def get_latest_predictions():
    return Image.query.filter(
        Image.prediction != None).order_by(Image.created.desc())[:3]
