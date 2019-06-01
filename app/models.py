from app import db
from datetime import datetime


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(200), index=True, unique=True, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    plot = db.relationship('Plot', uselist=False,
                           backref='image', lazy='joined')
    prediction = db.relationship(
        'Prediction', uselist=False, backref='image', lazy='joined')

    def __repr__(self):
        return '<Image {}>'.format(self.path)


class Plot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(200), index=False, unique=True, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))

    def __repr__(self):
        return '<Plot {}>'.format(self.path)


class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    probability = db.Column(db.Float, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))

    def __repr__(self):
        return '<Prediction {}>'.format(self.id)


class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=False, unique=True, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    predictions = db.relationship(
        'Prediction', uselist=True, backref='class', lazy='joined')

    def __repr__(self):
        return '<Classes {}>'.format(self.name)
