from myblog import app
from flask import render_template, g, request, url_for, redirect, flash, session
from sqlalchemy import func
from myblog.database import db_session, init_db
from myblog.models import Post, Category

@app.route('/')
def index():
    return render_template('home.html',links=get_shortcuts())

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
    return render_template('login.html',links=get_shortcuts(), error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))

@app.route('/add_post', methods=['GET','POST'])
def add_post():
    if session.get('logged_in')== True:
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
            return redirect(url_for('view_post',postid=post.id,))
        return render_template('form_add_post.html',links=get_shortcuts())
    return redirect(url_for('index'))

@app.route('/post/<postid>')
def view_post(postid):
    post = db_session.query(Post).filter_by(id=postid).first()
    return render_template('view_post.html',post=post,links=get_shortcuts())

@app.route('/post/list', methods=['GET','POST'], defaults={'searchTarget':''})
@app.route('/post/list/<searchTarget>', methods=['GET','POST'])
def list_posts(searchTarget):
    if request.method == 'POST':
        searchTarget=request.form['searchTarget']
    if session.get('logged_in')== True:
        posts = db_session.query(Post).filter(Post.title.contains(searchTarget)).all()
    else:
        posts = db_session.query(Post).filter(Post.hidden==False).filter(Post.title.contains(searchTarget)).all()
    return render_template('list_posts.html',posts=posts,links=get_shortcuts())

@app.route('/post/list/categories/<category>')
def list_posts_by_category(category):
    posts = db_session.query(Post).join(Post.categories).filter(Post.hidden==False).filter(Category.name.ilike('%'+category+'%')).all()
    return render_template('list_posts.html',posts=posts,links=get_shortcuts())

@app.route('/post/list/year/<year>/month/<month>')
def list_posts_by_month(year,month):
    posts = db_session.query(Post).filter(Post.hidden==False).filter(func.strftime('%Y-%m',Post.timestamp)==year+'-'+month).all()
    return render_template('list_posts.html',posts=posts,links=get_shortcuts())

def get_shortcuts():
    categories = [c._asdict() for c in db_session.query(Category.name, func.count(Category.name).label('count')).join(Post).filter(Post.hidden==False).group_by(Category.name).all()]
    months = [month._asdict() for month in db_session.query(func.strftime('%Y',Post.timestamp).label('year'),func.strftime('%m',Post.timestamp).label('month'),func.count(func.strftime('%Y-%m',Post.timestamp)).label('count')).filter(Post.hidden==False).group_by(func.strftime('%Y-%m',Post.timestamp)).all()]
    links = {'categories':categories,'months':months}
    return links

@app.route('/edit_post/<postid>', methods=['GET','POST'])
def edit_post(postid):
    if session.get('logged_in')== True:
        post = db_session.query(Post).filter_by(id=postid).first()
        if request.method=='POST':
            tags = [] 
            for tag in request.form['categories'].split():
                tags.append(Category(name=tag))
            post.title =request.form['title']
            post.categories = tags            
            post.body = request.form['body']
            post.hidden =  request.form['hidden']=='hidden'
            db_session.commit()
            return redirect(url_for('view_post',postid=post.id))
        return render_template('form_edit_post.html',links=get_shortcuts(), post=post)
    return redirect(url_for('index'))

