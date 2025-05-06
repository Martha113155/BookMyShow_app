from database import db
from datetime import date, time

class Movie(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    showtimes = db.relationship('Showtime', backref='movie', lazy=True)

class Showtime(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    show_date = db.Column(db.Date, nullable=False)
    show_time = db.Column(db.String(5), nullable=False)  # Format: HH:MM
    total_seats = db.Column(db.Integer, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    bookings = db.relationship('Booking', backref='showtime', lazy=True)

class Booking(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    showtime_id = db.Column(db.Integer, db.ForeignKey('showtime.id'), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    seats_booked = db.Column(db.Integer, nullable=False)
    booking_time = db.Column(db.DateTime, nullable=False)