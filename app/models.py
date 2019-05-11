from app import db
from datetime import datetime


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(200), index=True, unique=True, nullable=False)
    plot_path = db.Column(db.String(200), index=False,
                          unique=True, nullable=True)
    predicted = db.Column(db.String(20), unique=False, nullable=True)
    probability = db.Column(db.Float, nullable=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Image {}>'.format(self.path)
