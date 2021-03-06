from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, IntegerField, RadioField, SelectField, TextAreaField, PasswordField
from wtforms.validators import InputRequired, Email, Optional, URL, NumberRange, Length
from wtforms_alchemy import model_form_factory
from models import db, User, Feedback


BaseModelForm = model_form_factory(FlaskForm)

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session

def length(min=0, max=50):
    return Length(min=min, max=max, message='Wrong length')
    
class UserRegisterForm(ModelForm):
    class Meta:
        model = User
        include_primary_keys = True
        field_args = {'password': {'validators': [Length(min=6, message='Password must be at least 6 characters long')]}}
        # password = PasswordField("Password", [InputRequired(), Length(min=6, message='Password must be at least 6 characters long')])
        # length_validator = length
        
# class UserForm(ModelForm):
#     class Meta:
#         model = User
#         only = ['password']
#         # password = PasswordField("1Password", validators=[InputRequired()])
#         length_validator = length
        
# class UserRegisterForm(ModelForm):
#     class Meta:
#         model = User
#         include_primary_keys = True
#         # password = PasswordField("1Password", validators=[InputRequired()])
#         length_validator = length
        
class UserLoginForm(ModelForm):
    class Meta:
        model = User
        # password = PasswordField("1Password", validators=[InputRequired()])
        only = ['username', 'password']
        unique_validator = None
        # length_validator = length
        
class FeedbackForm(ModelForm):
    class Meta: 
        model = Feedback