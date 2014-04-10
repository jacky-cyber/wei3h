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
    return app.send_static_file('home.html')

@app.route('/pricing')
def pricing():
    return app.send_static_file('pricing.html')

from app.zaiwenling.views import mod as zaiwenlingModule
app.register_blueprint(zaiwenlingModule)

from app.account.views import mod as accountModule
app.register_blueprint(accountModule)

from app.wechat.views import mod as wechatModule
app.register_blueprint(wechatModule)

from app.dashboard.views import mod as dashboardModule
app.register_blueprint(dashboardModule)

from app.games.views import mod as gamesModule
app.register_blueprint(gamesModule)


from app.weigou.views import mod as weigouModule
app.register_blueprint(weigouModule)


from app.weshop.views import mod as weshopModule
app.register_blueprint(weshopModule)