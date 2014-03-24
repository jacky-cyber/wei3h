# -*- coding: utf-8 -*-

from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for


mod = Blueprint('games', __name__, url_prefix='/games')

@mod.route('/index/')
@mod.route('/')
def index():
    return render_template('plr/index.html')

@mod.route('/2048/')
def game_2048():
    return render_template('games/2048.html')