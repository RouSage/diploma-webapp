import os
from app import app
from flask import render_template, flash, redirect, request, url_for
from app.forms import UploadImageForm
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
    if request.method == 'POST':
        if form.validate_on_submit():
            f = form.image.data
            f.save(os.path.join(app.root_path, secure_filename(f.filename)))

            flash("File '{}' uploaded!".format(filename))

            return redirect(url_for('index'))

    return render_template('upload.html', title='Upload Image', form=form)
