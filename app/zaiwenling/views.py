# -*- coding: utf-8 -*-

from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

from app import db
from app.zaiwenling.forms import MusicForm
from app.zaiwenling.models import Music

mod = Blueprint('zaiwenling', __name__, url_prefix='/zaiwenling')


import pymongo
conn = pymongo.Connection('localhost', 5430)
db = conn.test

@mod.route('/index/')
@mod.route('/')
def index():
    return render_template('zaiwenling/index.html')

@mod.route('/addmusic/', methods=['GET', 'POST'])
def add_music():
    form = MusicForm(request.form)
    if form.validate_on_submit():
        print form.music_pic.data

        music = Music(music_title=form.music_title.data, music_artist=form.music_artist.data, music_pic=form.music_pic.data, music_audio=form.music_audio.data)

        db.session.add(music)
        db.session.commit()

        return redirect(url_for('zaiwenling.list_music'))
    return render_template('zaiwenling/add_music.html', form=form)

@mod.route('/music/<id>/')
def get_music(id):
    music = Music.query.filter_by(id=id).first()
    return render_template('zaiwenling/music.html', music=music)

@mod.route('/musics/')
def list_music():
    musics = Music.query.all()
    return render_template('zaiwenling/musics.html', musics=musics)

@mod.route('/waimai/<id>/')
def get_waimai(id):
    from bson.objectid import ObjectId
    waimai = db.waimai.find_one({'_id': ObjectId(id)}, {'_id': 0})
    return render_template('zaiwenling/waimai.html', waimai=waimai)

@mod.route('/waimais/')
def list_waimai():
    waimais = []
    for i in db.waimai.find():
        id = str(i['_id'])
        del i['_id']
        i['objid'] = id

        waimais.append(i)

    return render_template('zaiwenling/waimais.html', waimais=waimais)


