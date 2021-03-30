import os

import click

from app import app, db
from app.models import Classes


@app.cli.command("seed")
def seed():
    classes = [
        Classes(id=1, name="plane"),
        Classes(id=2, name="car"),
        Classes(id=3, name="bird"),
        Classes(id=4, name="cat"),
        Classes(id=5, name="deer"),
        Classes(id=6, name="dog"),
        Classes(id=7, name="frog"),
        Classes(id=8, name="horse"),
        Classes(id=9, name="ship"),
        Classes(id=10, name="truck"),
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
