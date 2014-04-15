# -*- coding: utf-8 -*-

from app import db


class Music(db.Model):

    __tablename__ = 'zaiwenling_music'
    id = db.Column(db.Integer, primary_key=True)
    music_title = db.Column(db.String(50))
    music_artist = db.Column(db.String(50))
    music_pic = db.Column(db.String(120))
    music_audio = db.Column(db.String(512))

    def __init__(self, music_title=None, music_artist=None, music_pic=None, music_audio=None):
        self.music_title = music_title
        self.music_artist = music_artist
        self.music_pic = music_pic
        self.music_audio = music_audio

    def __repr__(self):
        return '<Music %r>' % self.music_title








