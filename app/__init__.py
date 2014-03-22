# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
#    return 'Hello World!'
    return app.send_static_file('track.html')

# from app.users.views import mod as usersModule
# app.register_blueprint(usersModule)
