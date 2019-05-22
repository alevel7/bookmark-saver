from flask import Flask,render_template,url_for,request,redirect,flash,session
from forms import BookmarkForm,LoginForm,SignUpForm
from datetime import datetime
from flask_login import login_required, login_user, LoginManager,logout_user, current_user
import models
from bookmarks import app, db

#configure authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(user_id)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', new_bookmarks=models.Bookmark.newest(5))
    
@app.route('/user/<username>')
def user(username):
    user = models.User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@app.route('/add',methods=['GET','POST'])
@login_required
def add():
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        bm=models.Bookmark(user=current_user,url=url,description=description)
        db.session.add(bm) 
        db.session.commit()
        flash(f'stored bookmark {description}','success')
        return redirect(url_for('index'))
    return render_template('bookmark_form.html',form=form, title="Add form")

@app.route('/edit/<int:bookmark_id>', methods=['GET', 'POST'])
@login_required
def edit_bookmark(bookmark_id):
    bookmark = models.Bookmark.query.get_or_404(bookmark_id)
    print(type(bookmark))
    if current_user != bookmark.user:
        abort(403)
    form = BookmarkForm(obj=bookmark)
    if form.validate_on_submit():
        form.populate_obj(bookmark)
        db.session.commit()
        flash('Stored {}'.format(bookmark.description), "success")
        return redirect(url_for('user', username=current_user.username))
    return render_template('bookmark_form.html', form=form, title='Edit Bookmark')

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = models.User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data ):
            login_user(user, form.remember.data)
            flash(f'logged in successfully as {user.username}', 'success')
            return redirect(request.args.get('next') or url_for('user', username=user.username))
        flash("Incorrect username or password", 'alert-danger')
    return render_template('login.html',form=form, title="Login Form")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = models.User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome {}, Please Login'.format(user.username), 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'),500


if __name__=="__main__":
    app.run(debug=True)
