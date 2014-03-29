# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required

class MusicForm(Form):
    music_title = TextField('title', [Required()])
    music_artist = TextField('artist', [Required()])
    music_pic = TextField('pic', [Required()])
    music_audio = TextField('audio', [Required()])
