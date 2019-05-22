import click
from flask import Flask
from flask.cli import FlaskCLI

from run import app
FlaskCLI(app)

@app.cli.command()
def initdb():
    """Initialize the database."""
    print("something went wrong")
    click.echo('Init the db')