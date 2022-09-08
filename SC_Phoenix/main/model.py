from main import db
from datetime import datetime

joined_events = db.Table('joined_events',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    role = db.Column(db.String(20), nullable=False)


    def __repr__(self):
        return f"Username: {self.username}\nEmail: {self.email}"

class Event(db.Model):
    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(50), nullable=False)
    event_post_date = db.Column(db.Date, nullable=False, default=datetime.today().date())
    event_type = db.Column(db.String(10), nullable=False)
    event_date = db.Column(db.Date)
    event_location = db.Column(db.String(50))
    participant = db.relationship('User', secondary=joined_events, backref='events')

    def __repr__(self):
        return f"Event Name: {self.event_name}\nEvent Date: {self.event_date}"
