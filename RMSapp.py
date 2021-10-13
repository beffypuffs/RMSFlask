from flask import Flask, redirect, url_for, render_template
import sqlalchemy
from sqlalchemy import create_engine


app = Flask(__name__)


@app.route("/")
def help_page():
    return render_template('help.html')


@app.route("/chocks")
def chocks():
    return render_template('chocks.html')


@app.route("/notifications")
def notification():
    return render_template('notifications.html')


@app.route("/home")
def home():
    return render_template('index.html')


def ChAnGe_LaTeR(): #function for connecting to SQL server
    engine = create_engine() # figure out later


if __name__ == "__main__":
    app.run()