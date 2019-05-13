import os
import uuid
import torch
from PIL import Image as pil
from flask import redirect, render_template, request, url_for
from flask_babel import _
from app import app, db, model
from app.forms import UploadImageForm
from app.models import Image
from app.utils import predict, prepare_image, CLASSES, plot_probabilities


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
    return render_template('index.html', title=_('Home'), form=form, latest=get_latest_predictions())


@app.route('/prediction/<int:img_id>')
def prediction(img_id):
    # Get an Image entity from the database
    image = Image.query.get_or_404(img_id)

    if image.predicted == None:
        # Predict the image's class
        img = pil.open(os.path.join(app.static_folder, 'img', image.path))
        img = prepare_image(img)
        predicted, probs = predict(model=model, x=img)

        # Update the image entity
        image.predicted = CLASSES[predicted]
        image.probability = torch.max(probs, dim=0)[0].item()
        image.plot_path = plot_probabilities(probs, os.path.join(
            app.static_folder, 'img', image.path.split('.')[0] + '_plot.png'))
        db.session.commit()

    result = {
        'img_path': 'img/' + image.path,
        'predicted': image.predicted,
        'prob': image.probability * 100,
        'plot_path': 'img/' + image.plot_path
    }

    return render_template('predict.html', title=_('Prediction'), result=result, form=UploadImageForm())


def get_latest_predictions():
    return Image.query.filter(
        Image.predicted != None).order_by(Image.created.desc())[:3]
