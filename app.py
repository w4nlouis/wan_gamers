import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

load_dotenv()

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/gaming_shop"
db=SQLAlchemy(app)


class Station(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    label=db.Column(db.String(50), nullable=False)
    status=db.Column(db.String(20), default="free")

class Games(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50), nullable=False)
    active=db.Column(db.Boolean, default=True)

class User(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50), nullable=False)
    username=db.Column(db.String(50), unique=True, nullable=False)
    password_hash=db.Column(db.String(255), nullable=False)
    role=db.Column(db.String(20), nullable=False)

class Price(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    game_id=db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)
    mode=db.Column(db.String(20), nullable=False, default="normal")
    billing_unit=db.Column(db.String(20), nullable=False)
    amount=db.Column(db.Integer, nullable=False)

class Session(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    station_id=db.Column(db.Integer, db.ForeignKey("station.id"), nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    started_at=db.Column(db.DateTime, default=db.func.now())
    ended_at=db.Column(db.DateTime, nullable=True)
    total_amount=db.Column(db.Integer, default=0)
    status=db.Column(db.String(20), default="active")

class SessionItem(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    session_id=db.Column(db.Integer, db.ForeignKey("session.id"), nullable=False)
    game_id=db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)
    mode=db.Column(db.String(20), nullable=False)
    billing_unit=db.Column(db.String(20), nullable=False)
    started_at=db.Column(db.DateTime, default=db.func.now())
    ended_at=db.Column(db.DateTime, nullable=True)
    amount=db.Column(db.Integer, default=0)

class Payments(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    session_id=db.Column(db.Integer, db.ForeignKey("session.id"), nullable=False)
    method=db.Column(db.String(20), nullable=False)
    amount=db.Column(db.Integer, nullable=False)
    reference=db.Column(db.String(50), unique=True, nullable=True)
    paid_at=db.Column(db.DateTime, default=db.func.now())
    recorded_by=db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

@app.route("/")
def home():
    return "Gaming shop system is aliiveeee"

@app.route("/stations")
def stations():
    all_stations=Station.query.all()
    lines=[]
    for s in all_stations:
        lines.append(f"{s.label}-{s.status}")
    return "<br>".join(lines)

with app.app_context():
    db.create_all()
