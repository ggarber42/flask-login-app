from flask import render_template, url_for, flash, redirect
from .forms import LoginForm
from app import app
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User

@app.route('/')
@app.route('/index')
def index():
    message = {'message_value':'Página Inicial'}
    return render_template('message.html', title='Home', message=message)

@app.route('/aberta')
def aberta():
    message = {'message_value':'Página Aberta'}
    return render_template('message.html', title='Aberta', message=message)

@app.route('/protegida')
@login_required
def protegida():
    message = {'message_value':'Página Protegida'}
    return render_template('message.html', title='Protegida', message=message)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        flash('You have been logged in!', 'success')
        return redirect(url_for('index'))
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logout!', 'info')
    return redirect(url_for('index'))