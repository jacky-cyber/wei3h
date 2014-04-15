# -*- coding: utf-8 -*-

from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for


mod = Blueprint('weigou', __name__, url_prefix='/weigou')

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
conn = MongoClient(host='localhost', port=5430)
db = conn.test

@mod.route('/index/')
@mod.route('/')
def index():
    return render_template('weigou/index.html', title='Shewww\'s')

@mod.route('/homepage')
def homepage():
    token = request.args.get('token', '')
    openid = request.args.get('openid', '')

    shop = db.shop.find_one({'_id': ObjectId(token)})
    shopics = db.shopics.find({'shop_id': str(shop['_id'])}).sort('rate')

    return render_template('weigou/homepage.html', shop=shop, shopics=shopics)
