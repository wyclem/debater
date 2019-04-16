from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Debate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.Text)
    affirmative_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    affirmative = db.relationship('User', foreign_keys=[affirmative_id])
    negative_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    negative = db.relationship('User', foreign_keys=[negative_id])
    affirmative_title = db.Column(db.Text)
    negative_title = db.Column(db.Text)
    affirmative_constructive = db.Column(db.Text)
    negative_constructive = db.Column(db.Text)
    affirmative_rebuttal = db.Column(db.Text)
    negative_rebuttal = db.Column(db.Text)
    affirmative_rejoinder = db.Column(db.Text)

    def __repr__(self):
        return '<Debate {}>'.format(self.topic)
