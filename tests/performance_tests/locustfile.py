from locust import HttpUser, task
import random
from app import loadClubs, loadCompetitions


class ProjectPerfTest(HttpUser):

    clubs = loadClubs()
    competitions = loadCompetitions()

    @task
    def index(self):
        self.client.get("")

    @task
    def login(self):
        club = random.choice(self.clubs)
        email = club['email']
        self.client.post("showSummary", {"email": email})

    @task
    def book_place(self):
        club = random.choice(self.clubs)
        competition = random.choice(self.competitions)
        data = {'club': club['name'],
                'competition': competition['name'],
                'places': random.randint(1, int(competition['numberOfPlaces']))}
        self.client.post("purchasePlaces", data=data)

    @task
    def logout(self):
        self.client.get("logout")

    @task
    def display_points(self):
        self.client.get("points")
