from myblog import app
from flask import render_template, g, request, url_for, redirect, flash
from myblog.database import db_session, init_db
from myblog.models import Post, Category

@app.route('/')
def index():
    return render_template('home.html',title='Home')

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
