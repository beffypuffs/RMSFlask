from flask import Flask, redirect, url_for, render_template
import pypyodbc as pp


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


@app.route("/sql")
def sql():
    return sql_connect()


def sql_connect(): #function for connecting to SQL server
    try:
        connection = pp.connect('Driver= {sqlsrv};Server = localhost\\SQLEXPRESS;Database = rms; '
                                'uid=rmsapp;pwd=ss1RMSpw@wb02')# figure out later
    except pp.Error:
        return render_template('error.html')
    return render_template('sql.html')

if __name__ == "__main__":
    app.run()