"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import EmailType, PasswordType
from flask_bcrypt import Bcrypt
from wtforms import PasswordField

from sqlalchemy_defaults import Column, make_lazy_configured

from wtforms.validators import InputRequired, Email, Optional, URL, NumberRange, Length

db = SQLAlchemy()

bcrypt = Bcrypt()

make_lazy_configured(db.mapper)

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __lazy_options__ = {}
    __tablename__ = 'users'
    
    username = db.Column(db.String(20),
                        unique=True,
                        primary_key=True)
    
    password = db.Column(db.String(50),
                        info={'form_field_class': PasswordField},
                        nullable=False)
    
    email = db.Column(EmailType(50),
                        unique=True,
                        nullable=False)
    
    first_name = db.Column(db.String(30),
                            nullable=False)
    
    last_name = db.Column(db.String(30),
                            nullable=False)
    
    feedback = db.relationship('Feedback', backref='user', cascade="all, delete-orphan")
    
    
    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, password):
            # return user instance
            return u
        else:
            return False
    
    def __repr__(self):
        u = self
        return f"<username={u.username} password={bool(u.password)} email={u.email} first_name={u.first_name} last_name={u.last_name}>"
    
    
class Feedback(db.Model):
    __tablename__ = 'feedback'
    
    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    
    title = db.Column(db.String(100),
                            nullable=False)
    
    content = db.Column(db.Text,
                            nullable=False)
    
    username = db.Column(db.String(20),
                            db.ForeignKey('users.username'))
    
    def __repr__(self):
        f = self
        return f"<Feedback {f.id} title={f.title} content_len={len(f.content)} username={f.username}>"
    


    # def serialize(self):
    #     """Returns a dict representation of Cupcake which we can turn into JSON"""
    #     c = self
    #     return {
    #         'id': c.id,
    #         'flavor': c.flavor,
    #         'size': c.size,
    #         'rating': c.rating,
    #         'image': c.image
    #     }
