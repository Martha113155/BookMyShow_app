
from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import db
from models import Movie, Showtime, Booking
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookmyshow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)  # Initialize SQLAlchemy with the Flask app

# Initialize database and seed data within app context
with app.app_context():
    db.create_all()
    # Seed database with sample data if empty
    if not Movie.query.first():
        movie1 = Movie(title="Avengers: Endgame", genre="Action", duration=180)
        movie2 = Movie(title="The Shawshank Redemption", genre="Drama", duration=142)
        db.session.add_all([movie1, movie2])
        
        # Add showtimes for the next 3 days
        for movie in [movie1, movie2]:
            for i in range(3):
                date = datetime.now().date() + timedelta(days=i)
                showtime1 = Showtime(movie=movie, show_date=date, show_time="14:00", total_seats=100, available_seats=100)
                showtime2 = Showtime(movie=movie, show_date=date, show_time="18:00", total_seats=100, available_seats=100)
                db.session.add_all([showtime1, showtime2])
        db.session.commit()

@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    showtimes = Showtime.query.filter_by(movie_id=movie_id).all()
    return render_template('movie_details.html', movie=movie, showtimes=showtimes)

@app.route('/book/<int:showtime_id>', methods=['GET', 'POST'])
def book(showtime_id):
    showtime = Showtime.query.get_or_404(showtime_id)
    if request.method == 'POST':
        name = request.form.get('name')
        seats = int(request.form.get('seats'))
        if not name or seats <= 0:
            return jsonify({'error': 'Invalid input'}), 400
        if showtime.available_seats < seats:
            return jsonify({'error': 'Not enough seats available'}), 400
        
        booking = Booking(
            showtime_id=showtime_id,
            user_name=name,
            seats_booked=seats,
            booking_time=datetime.utcnow()
        )
        showtime.available_seats -= seats
        db.session.add(booking)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('booking.html', showtime=showtime)

@app.route('/api/showtimes/<int:movie_id>')
def get_showtimes(movie_id):
    showtimes = Showtime.query.filter_by(movie_id=movie_id).all()
    showtime_list = [
        {
            'id': st.id,
            'date': st.show_date.strftime('%Y-%m-%d'),
            'time': st.show_time,
            'available_seats': st.available_seats
        } for st in showtimes
    ]
    return jsonify(showtime_list)

if __name__ == '__main__':
    app.run(debug=True)