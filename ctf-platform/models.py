from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    team_name = db.Column(db.String(120), default='')
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    submissions = db.relationship('Submission', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password matches"""
        return check_password_hash(self.password_hash, password)
    
    def get_score(self):
        """Get total score from accepted submissions"""
        return sum(sub.challenge.points for sub in self.submissions if sub.is_correct)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Challenge(db.Model):
    """Challenge model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    flag = db.Column(db.String(255), nullable=False)
    points = db.Column(db.Integer, default=100)
    category = db.Column(db.String(80), default='General')
    writeup = db.Column(db.Text, default='')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    submissions = db.relationship('Submission', backref='challenge', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Challenge {self.title}>'


class Submission(db.Model):
    """Challenge submission model"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), nullable=False)
    flag_submitted = db.Column(db.String(255), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'challenge_id', name='uq_user_challenge'),)
    
    def __repr__(self):
        return f'<Submission {self.user_id} - {self.challenge_id}>'
