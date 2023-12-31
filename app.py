import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


# Function to load clubs from a JSON file
def loadClubs():
    """
    Load clubs from a JSON file.

    Returns:
        list: List of club dictionaries.
    """
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


# Function to load competitions from a JSON file
def loadCompetitions():
    """
    Load competitions from a JSON file.

    Returns:
        list: List of competition dictionaries.
    """
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


# Flask app setup
app = Flask(__name__)
app.secret_key = 'something_special'

# Load competitions and clubs
competitions = loadCompetitions()
clubs = loadClubs()


# Route for the home page
@app.route('/')
def index():
    """
    Render the home page.

    Returns:
        str: Rendered HTML for the home page.
    """
    return render_template('index.html')


# Route to handle form submission and show club summary
@app.route('/showSummary', methods=['POST'])
def showSummary():
    """
    Process form submission, find the club based on email,
    and render the welcome page with club details.

    Returns:
        str: Rendered HTML for the welcome page or index page in case of failure.
    """
    email = request.form['email']
    matching_clubs = [club for club in clubs if club['email'] == email]

    if matching_clubs:
        for competition in competitions:
            competition_date = datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S')
            now = datetime.now()
            if competition_date > now:
                competition['passed'] = False
            else:
                competition['passed'] = True
        club = matching_clubs[0]
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        flash('Club not found for the provided email.')
        return render_template('index.html')


# Route to handle booking page
@app.route('/book/<competition>/<club>')
def book(competition, club):
    """
    Render the booking page with details of the selected competition and club.

    Args:
        competition (str): Name of the competition.
        club (str): Name of the club.

    Returns:
        str: Rendered HTML for the booking page or welcome page in case of failure.
    """
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


# Route to handle the purchase of places
@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    """
    Process the form submission for purchasing places and update competition and club data.

    Returns:
        str: Rendered HTML for the welcome page with updated information.
    """
    global competitions, clubs
    competition_name = request.form['competition']

    matching_competitions = [c for c in competitions if c['name'] == competition_name]

    if not matching_competitions:
        flash(f"Competition '{competition_name}' not found.")
        return render_template('index.html')

    competition = matching_competitions[0]

    club_name = request.form['club']
    club = [c for c in clubs if c['name'] == club_name][0]
    places_required = int(request.form['places'])
    competition_date = datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S')
    now = datetime.now()

    if (
        int(competition['numberOfPlaces']) >= places_required
        and int(club['points']) >= places_required
        and places_required <= 12
        and now < competition_date
    ):
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
        club['points'] = int(club['points']) - places_required
        flash(f'Great-booking complete! {places_required} places for {competition["name"]} competition')
    else:
        flash("There is not enough places or you don't have enough points or competition date is passed")

    return render_template('welcome.html', club=club, competitions=competitions)


# Route to handle logout
@app.route('/logout')
def logout():
    """
    Redirect to the home page upon logout.

    Returns:
        str: Redirect to the home page.
    """
    return redirect(url_for('index'))


# Route to display points
@app.route('/points')
def points():
    """
    Render the points page with information about all the clubs.

    Returns:
        str: Rendered HTML for the points page.
    """
    return render_template('points.html', clubs=clubs)
