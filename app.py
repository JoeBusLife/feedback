"""Flask app for Cupcakes"""
from flask import Flask, request, render_template, jsonify, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db,  connect_db, User, Feedback
from forms import UserRegisterForm, UserLoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "soup"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def home_page():
    """ Redirect user based on login status """
    username = session.get('username')
    if username:
        return redirect(f'/users/{username}')
    
    return redirect('/login')
    
    
@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """ Show and handle account registration form
    Redirect to user profile page if already logged in """
    username = session.get('username')
    if username:
        return redirect(f'/users/{username}')
    
    form = UserRegisterForm()
    if form.validate_on_submit():
        form_data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        new_user = User.register(**form_data)
        
        db.session.add(new_user)
        db.session.commit()
        session['username'] = new_user.username
        flash('Welcome! Successfully Created Your Account', "success")
        
        return redirect(f'/users/{new_user.username}')
    
    return render_template('register.html', form=form)
    
    
@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """ Show and handle account login form
    Redirect to user profile page if already logged in """
    username = session.get('username')
    if username:
        return redirect(f'/users/{username}')
    
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        
        if user:
            # flash(f"Welcome Back, {user.first_name}", "success")
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)
    
    
@app.route('/logout')
def logout_user():
    """ Logout user """
    session.pop('username')
    
    return redirect('/')
    
    
@app.route('/users/<username>')
def show_user(username):
    """ Show user profile page if correct user logged in """
    if session.get('username') == username:
        user = User.query.get(username)
        Feedback.query
        return render_template('user.html', user=user)
    else:
        return redirect('/')
    
    
@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """ Delete and logout user account if currently logged in """
    if session.get('username') == username:
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
        session.pop('username')
    
    return redirect('/')


@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def feedback_add(username):
    """ Show and handle new feedback form if correct user logged in """
    if session.get('username') != username:
        return redirect('/')

    form = FeedbackForm()
    if form.validate_on_submit():
        form_data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        new_feedback = Feedback(username=username, **form_data)
        db.session.add(new_feedback)
        db.session.commit()
        
        return redirect(f'/users/{username}')
    
    return render_template('feedback_add.html', form=form, username=username)


@app.route('/feedback/<feedback_id>/update', methods=['GET', 'POST'])
def feedback_update(feedback_id):
    """ Show and handle update feedback form if correct user logged in and feedback exists """
    feedback = Feedback.query.get_or_404(feedback_id)
    username = feedback.username
    if session.get('username') != username:
        return redirect('/')

    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        form.populate_obj(feedback)
        
        db.session.commit()
 
        return redirect(f'/users/{username}')
    
    return render_template('feedback_edit.html', form=form, username=username)


@app.route('/feedback/<feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    """ Delete feedback if correct user logged in and feedback exists """
    feedback = Feedback.query.get_or_404(feedback_id)
    username = feedback.username
    if session.get('username') == username:
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f'/users/{username}')
    else:
        return redirect('/')