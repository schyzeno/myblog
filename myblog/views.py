from myblog import app
from flask import render_template, g, request, url_for, redirect, flash

@app.route('/')
def index():
    return render_template('home.html',title='Home')
