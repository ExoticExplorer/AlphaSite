from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length, EqualTo


class CreateForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(min=2, max =20)])
	server_type = RadioField('Server Type', choices=[('Public'), ('Private')], validators=[DataRequired()])
	password = PasswordField('Password')
	confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])
	submit = SubmitField('Submit')

class JoinForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(min=2, max =20)])
	server_type = RadioField('Server Type', choices=[('Public', 'Public'), ('Private', 'Private')], validators=[DataRequired()])
	password = PasswordField('Password')
	submit = SubmitField('Join')