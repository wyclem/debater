from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField, PasswordField, RadioField
from wtforms.validators import DataRequired, EqualTo
from app.models import User, Debate

class DebaterForm(FlaskForm):
    argument = TextAreaField('Argument', validators=[DataRequired()])
    submit = SubmitField('Post Argument')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class CreateDebateForm(FlaskForm):
    topic = StringField('Topic', validators=[DataRequired()])
    user_role = RadioField('Your Role', choices=[('affirmative', 'Affirmative'), ('negative', 'Negative')])
    second_debater = StringField('Who Are You Debating?', validators=[DataRequired()])
    affirmative_title = StringField('What Should the Affirmative Be Called?', default='Affirmative')
    negative_title = StringField('What Should the Negative Be Called?', default='Negative')
    submit = SubmitField('Debate!')

    def validate_second_debater(self, second_debater):
        user = User.query.filter_by(username=second_debater.data).first()
        if user is None:
            raise ValidationError('Please enter a valid username.')
