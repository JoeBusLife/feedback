from app import app
from models import db, User, Feedback
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db.drop_all()
db.create_all()

p1 = bcrypt.generate_password_hash("largeboy").decode("utf8")
        
p2 = bcrypt.generate_password_hash("11one11").decode("utf8")

u1 = User(
    username="cherry",
    password=p1,
    email="CherryBoy@hotmail.com",
    first_name="Sally",
    last_name="Brock"
)

u2 = User(
    username="Cold",
    password=p2,
    email="brewskis@yahoo.com",
    first_name="Chad",
    last_name="Sizzler"
)

db.session.add_all([u1, u2])
db.session.commit()


f1 = Feedback(
    title="Top shelf too high",
    content="Couldn't raech the top shelf in the fridge, even with stool. Obviosusly too high up",
    username="cherry"
)

f2 = Feedback(
    title="Party was great!",
    content="You guys had all the top beers. Bud Lite, Coors Lite and even Miller lite!!",
    username="Cold"
)

db.session.add_all([f1, f2])
db.session.commit()