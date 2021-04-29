import os

import click

from app import app, db
from app.models import Classes


@app.cli.command("seed")
def seed():
    classes = [
        Classes(id=1, name="aeroplane"),
        Classes(id=2, name="bicycle"),
        Classes(id=3, name="bird"),
        Classes(id=4, name="boat"),
        Classes(id=5, name="bottle"),
        Classes(id=6, name="bus"),
        Classes(id=7, name="car"),
        Classes(id=8, name="cat"),
        Classes(id=9, name="chair"),
        Classes(id=10, name="cow"),
        Classes(id=11, name="diningtale"),
        Classes(id=12, name="dog"),
        Classes(id=13, name="horse"),
        Classes(id=14, name="motorbike"),
        Classes(id=15, name="person"),
        Classes(id=16, name="pottedplant"),
        Classes(id=17, name="sheep"),
        Classes(id=18, name="sofa"),
        Classes(id=19, name="train"),
        Classes(id=20, name="tvmonitor"),
    ]
    classes_query = Classes.query.all()
    if(len(classes_query) != 10):
        db.session.query(Classes).delete()
        for c in classes:
            db.session.add(c)

    db.session.commit()


@app.cli.group()
def translate():
    """Translation and localization commands."""
    pass


@translate.command()
def update():
    """Update all languages."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system('pybabel update -i messages.pot -d app/translations'):
        raise RuntimeError('update command failed')
    os.remove('messages.pot')


@translate.command()
def compile():
    """Compile all languages."""
    if os.system('pybabel compile -d app/translations'):
        raise RuntimeError('compile command failed')


@translate.command()
@click.argument('lang')
def init(lang):
    """Initialize a new language."""
    if os.system('pybabel extract -F babel.cfg -k -l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system('pybabel init -i messages.pot -d app/translations -l ' + lang):
        raise RuntimeError('init command failed')
    os.remove('messages.pot')
