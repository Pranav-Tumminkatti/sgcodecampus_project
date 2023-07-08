from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, BooleanField, PasswordField
#from wtforms.fields.html5 import DateField, IntegerField
from wtforms.fields import RadioField, SelectField, DecimalField
from flask import flash
from wtforms.validators import InputRequired, ValidationError, DataRequired, Length, Email, EqualTo, NumberRange
import email_validator
from BlogApp.models import Auth

class Post(FlaskForm):
  category = StringField("Category", validators=[InputRequired(), Length(max=50)])
  title = StringField("Title", validators=[InputRequired(), Length(max=200)])
  content = TextAreaField("Content", validators=[InputRequired(), Length(min=50)])
  tags = StringField("Tags (delimit each tag with a comma)")
  img = FileField('Upload optional picture for blog',validators=[FileAllowed(['jpg','JPG','png','PNG','jpeg','JPEG'])])
  grammar_checker = BooleanField('Grammar Checker')
  
  def validate_tags(form, field):
    validated = True  
    if field.data != '' and (field.data[-1] == ',' or field.data[-1] == ' '):
      form.tags.errors.append("You cannot end with a comma or a space! Please adhere to the specified guidelines")
      validated = False
    return validated


class Login(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember_me = BooleanField('Remember Me') 
  
  def validate_username(form, field):
    validated = True  
    user = Auth.query.filter_by(username = form.username.data).first()
    if user is None:
      form.username.errors.append("No such user! Check your username and try again!")
      validated = False
    
    if user is not None and user.deleted == True:
      form.username.errors.append("This user has already been deleted from the database! Please check your credentials and try again!")
      validated = False
      
    return validated
      
  def validate_password(form, field):
    validated = True  
    user = Auth.query.filter_by(username = form.username.data).first()
    if user is None:
      validated = False
    else:
      if not user.check_password(form.password.data):
        form.password.errors.append("Wrong password! Try again!")
        validated = False
    return validated


class Sign_up(FlaskForm):
  username = StringField('Username', validators=[DataRequired(), Length(max=50)])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
  confirm  = PasswordField('Confirm Password')
  
  def validate_username(form, field):
    validated = True  
    user = Auth.query.filter_by(username = form.username.data).first()
    if user is not None:
      form.username.errors.append("This username already exists! Please choose another one!")
      validated = False
    return validated
  
  def validate_email(form, field):
    validated = True  
    user = Auth.query.filter_by(email = form.email.data).first()
    if user is not None:
      form.email.errors.append("An account with that email already exists! Please log into your account.")
      validated = False
    return validated
  
  def validate_password(form, field):
    validated = True  
    if len(field.data) < 6:
      form.password.errors.append("Length of password must be at least 6 characters!")
      validated = False
    
    if not any(char.isdigit() for char in field.data):
      form.password.errors.append("Password should contain at least 1 numerical character!")
      validated = False
      
    if not any(c in "!.@#$%^&*()-+?_=,<>/" for c in field.data):
      form.password.errors.append("Password should contain at least 1 special character!")
      validated = False
      
    return validated
  
  def validate_confirm(form, field):
    validated = True  
    if form.password.data != form.confirm.data:
      form.confirm.errors.append("Passwords don't match, please try again.")
      validated = False
    return validated
  

class profile_handling(FlaskForm):
  name = StringField("Name", validators=[InputRequired(), Length(max=50)])
  job = StringField("Job", validators=[InputRequired(), Length(max=100)])
  location = StringField("Location", validators=[InputRequired(), Length(max=200)])
  description = TextAreaField("Description", validators=[InputRequired(), Length(max=500)])
  fb = StringField("Facebook Profile link")
  ig = StringField("Instagram Profile link")
  tw = StringField("Twitter Profile link")
  img = FileField('Upload Profile Picture',validators=[FileAllowed(['jpg','JPG','png','PNG','jpeg','JPEG'])])


class EmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')
    
    def validate_password(form, field):
      validated = True  
      if len(field.data) < 6:
        form.password.errors.append("Length of password must be at least 6 characters!")
        validated = False
      
      if not any(char.isdigit() for char in field.data):
        form.password.errors.append("Password should contain at least 1 numerical character!")
        validated = False
        
      if not any(c in "!.@#$%^&*()-+?_=,<>/" for c in field.data):
        form.password.errors.append("Password should contain at least 1 special character!")
        validated = False
        
      return validated
  
    def validate_confirm(form, field):
      validated = True  
      if form.password.data != form.confirm.data:
        form.confirm.errors.append("Passwords don't match, please try again.")
        validated = False
      return validated
    
class comment_form(FlaskForm):
  comment = TextAreaField('Leave a comment', validators=[DataRequired()])

class edit_comment(FlaskForm):
  new = StringField('Update your comment', validators = [DataRequired()])

class private_message(FlaskForm):
  message = TextAreaField(validators=[DataRequired()])
  
class Announcement(FlaskForm):
    category = StringField('Category', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])

class Merch(FlaskForm):
    brand = StringField('Brand', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    img = FileField('Upload Merch Image',validators=[FileAllowed(['jpg','JPG','png','PNG','jpeg','JPEG'])])
    price = DecimalField('Price', validators=[DataRequired()])
    order_link = StringField('Order Link', validators=[DataRequired()])
    colour = StringField('Colour', validators=[DataRequired()])
    sizes = StringField('Sizes', validators=[DataRequired()])