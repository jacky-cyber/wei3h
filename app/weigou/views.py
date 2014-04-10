# -*- coding: utf-8 -*-

from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for


mod = Blueprint('weigou', __name__, url_prefix='/weigou')

@mod.route('/index/')
@mod.route('/')
def index():
    return render_template('weigou/index.html', title='Shewww\'s')
