from myblog import app
from flask import render_template, g, request, url_for, redirect, flash, session
from myblog.database import db_session, init_db
from myblog.models import Post, Category

@app.route('/')
def index():
    return render_template('home.html',title='Home')

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        print(url_for('index'))
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))
