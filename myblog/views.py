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

@app.route('/add_post', methods=['GET','POST'])
def add_post():
    if request.method=='POST':
        print(request.form['categories'].split())
        tags = [] 
        for tag in request.form['categories'].split():
            tags.append(Category(name=tag))
        post = Post(title=request.form['title'],
                    categories=tags,
                    body=request.form['body'])
        db_session.add(post)
        db_session.commit()
        return redirect(url_for('view_post',postid=post.id))
    return render_template('form_post.html')

@app.route('/post/<postid>')
def view_post(postid):
    post = db_session.query(Post).filter_by(id=postid).first()
    return render_template('view_post.html',post=post)

@app.route('/post/list', defaults={'searchTarget':''})
@app.route('/post/list/<searchTarget>')
def list_posts(searchTarget):
    posts = db_session.query(Post).filter(Post.title.contains(searchTarget)).all()
    return render_template('list_posts.html',posts=posts)
