from unicodedata import category
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired,Length, Email, EqualTo 


#Creating a registration form
class Registration(FlaskForm):
    name = StringField('Name', render_kw={'placeholder':'Name'}, validators=[DataRequired(), Length(1,100)])
    email = StringField('Email', render_kw={'placeholder':'Email'}, validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmpassword = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class Login(FlaskForm):
   
    email = StringField('Email', render_kw={'placeholder':'Email'}, validators=[DataRequired(), Email()])
    rememberme = BooleanField('Keep me logged in? ')
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class Logininstructor(FlaskForm):
   
    email = StringField('Email', render_kw={'placeholder':'Email'}, validators=[DataRequired(), Email()])
    rememberme = BooleanField('Keep me logged in? ')
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class Loginadmin(FlaskForm):
   
    email = StringField('Email', render_kw={'placeholder':'Email'}, validators=[DataRequired(), Email()])
    rememberme = BooleanField('Keep me logged in? ')
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class Registerinstructor(FlaskForm):
   
    email = StringField('Email', render_kw={'placeholder':'Email'}, validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmpassword = PasswordField('confirmpassword', validators=[DataRequired()])
    username = StringField('username', render_kw={'placeholder':'Enter username'}, validators=[DataRequired()])
    coursecode = StringField('coursecode', render_kw={'placeholder':'Enter coursecode'}, validators=[DataRequired()])
    rememberme = BooleanField('Keep me logged in? ')
    
    submit = SubmitField('Sign Up')



class Addcourse(FlaskForm):
   
    title = StringField('title', render_kw={'placeholder':'Title'}, validators=[DataRequired()])
    description = StringField(' ')
    category =StringField('category', validators=[DataRequired()])
    duration = StringField('duration', render_kw={'placeholder':'Enter duration'}, validators=[DataRequired()])
    image = StringField('image', render_kw={'placeholder':'img'}, validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class Subunit(FlaskForm):
   
    title = StringField('title', render_kw={'placeholder':'Title'}, validators=[DataRequired()])
    duration = StringField('duration', render_kw={'placeholder':'Enter duration'}, validators=[DataRequired()])
    link = StringField('link', render_kw={'placeholder':'link'}, validators=[DataRequired()])
    submit = SubmitField('Sign Up')