from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField


allowed_extensions = ['jpg', 'jpeg', 'png', 'bmp', 'tiff', 'tif']


class UploadImageForm(FlaskForm):
    image = FileField('Image', validators=[
        FileRequired(),
        FileAllowed(allowed_extensions, 'You allowed to upload images only!')])
    submit = SubmitField("Upload")
