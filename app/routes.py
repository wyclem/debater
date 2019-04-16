from flask import render_template, flash, redirect, request, url_for
from app import app, db
from app.forms import DebaterForm, LoginForm, RegistrationForm, CreateDebateForm
from flask_login import current_user, login_user, logout_user
from app.models import User, Debate
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
def index():
    debates = Debate.query.all()
    return render_template('index.html', title='Home', debates=debates)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/debate/<id>', methods=['GET', 'POST'])
def debate(id):
    debate = Debate.query.filter_by(id=id).first_or_404()
    round = 1
    current_debater = debate.affirmative
    if (debate.affirmative_constructive is not None) and (debate.negative_constructive is None):
        round = 2
        current_debater = debate.negative
    elif (debate.negative_constructive is not None) and (debate.affirmative_rebuttal is None):
        round = 3
        current_debater = debate.affirmative
    elif (debate.affirmative_rebuttal is not None) and (debate.negative_rebuttal is None):
        round = 4
        current_debater = debate.negative
    elif (debate.negative_rebuttal is not None) and (debate.affirmative_rejoinder is None):
        round = 5
        current_debater = debate.affirmative
    elif (debate.affirmative_rejoinder is not None):
        round = 6
        current_debater = None
    form = DebaterForm()
    if form.validate_on_submit():
        if round == 1:
            debate.affirmative_constructive = form.argument.data
            db.session.commit()
        elif round == 2:
            debate.negative_constructive = form.argument.data
            db.session.commit()
        elif round == 3:
            debate.affirmative_rebuttal = form.argument.data
            db.session.commit()
        elif round == 4:
            debate.negative_rebuttal = form.argument.data
            db.session.commit()
        elif round == 5:
            debate.affirmative_rejoinder = form.argument.data
            db.session.commit()
        # flash(form.argument.data)
        return redirect(url_for('debate', id=id))
    return render_template('debate.html', debate=debate, title="Debate", form=form, round=round, current_debater=current_debater)

@app.route('/create-debate', methods=['GET', 'POST'])
def create_debate():
    form = CreateDebateForm()
    if form.validate_on_submit():
        second_debater = User.query.filter_by(username=form.second_debater.data).first()
        if form.user_role.data == "affirmative":
            debate = Debate(topic=form.topic.data, affirmative=current_user, negative=second_debater, affirmative_title=affirmative_title.data, negative_title=negative_title.data)
            db.session.add(debate)
            db.session.commit()
        elif form.user_role.data == "negative":
            debate = Debate(topic=form.topic.data, affirmative=second_debater, negative=current_user, affirmative_title=affirmative_title.data, negative_title=negative_title.data)
            db.session.add(debate)
            db.session.commit()
        return redirect(url_for('debate', id=debate.id))
    return render_template('create-debate.html', form=form)
