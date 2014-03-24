# -*- coding: utf-8 -*-

from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

from app import db
from app.plr.forms import MusicForm
from app.plr.models import Music

mod = Blueprint('plr', __name__, url_prefix='/plr')

@mod.route('/index/')
@mod.route('/')
def index():
    return render_template('plr/index.html')

@mod.route('/addmusic/', methods=['GET', 'POST'])
def add_music():
    form = MusicForm(request.form)
    if form.validate_on_submit():
        print form.music_pic.data

        music = Music(music_title=form.music_title.data, music_artist=form.music_artist.data, music_pic=form.music_pic.data, music_audio=form.music_audio.data)

        db.session.add(music)
        db.session.commit()
        print music.getHref()

        flash(music.getHref())
        return redirect(music.getHref())
    return render_template('plr/add_music.html', form=form)

@mod.route('/music/<id>/')
def get_music(id):
    music = Music.query.filter_by(id=id).first()
    return render_template('plr/music.html', music=music)

@mod.route('/musics/')
def list_music():
    musics = Music.query.all()
    return render_template('plr/musics.html', musics=musics)