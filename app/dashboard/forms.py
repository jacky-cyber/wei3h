# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import TextField, FileField
from wtforms.validators import Required


class FilepageForm(Form):
    files = FileField('photo')


