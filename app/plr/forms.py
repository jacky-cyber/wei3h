# -*- coding: utf-8 -*-

from flask.ext.wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import Required, EqualTo, Email

class MusicForm(Form):
    music_title = TextField('title', [Required()])
    music_artist = TextField('artist', [Required()])
    music_pic = TextField('pic', [Required()])
    music_audio = TextField('audio', [Required()])
