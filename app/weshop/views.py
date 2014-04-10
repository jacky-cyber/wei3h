# -*- coding: utf-8 -*-

from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from app.weshop.models import Shop

mod = Blueprint('weshop', __name__, url_prefix='/weshop')

@mod.route('/index/')
@mod.route('/')
def index():
    return 'ass'
