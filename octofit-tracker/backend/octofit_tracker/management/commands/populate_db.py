from django.core.management.base import BaseCommand
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Drop collections if they exist
        for col in ['users', 'teams', 'activities', 'leaderboard', 'workouts']:
            db[col].drop()

        # Create unique index for email in users
        db.users.create_index([('email', 1)], unique=True)

        # Sample data
        users = [
            {'name': 'Superman', 'email': 'superman@dc.com', 'team': 'DC'},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team': 'DC'},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team': 'DC'},
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': 'Marvel'},
            {'name': 'Captain America', 'email': 'cap@marvel.com', 'team': 'Marvel'},
            {'name': 'Spider-Man', 'email': 'spiderman@marvel.com', 'team': 'Marvel'},
        ]
        teams = [
            {'name': 'Marvel', 'members': ['Iron Man', 'Captain America', 'Spider-Man']},
            {'name': 'DC', 'members': ['Superman', 'Batman', 'Wonder Woman']},
        ]
        activities = [
            {'user': 'Superman', 'activity': 'Flight', 'duration': 60},
            {'user': 'Iron Man', 'activity': 'Suit Training', 'duration': 45},
        ]
        leaderboard = [
            {'team': 'Marvel', 'points': 120},
            {'team': 'DC', 'points': 110},
        ]
        workouts = [
            {'user': 'Batman', 'workout': 'Martial Arts', 'duration': 30},
            {'user': 'Spider-Man', 'workout': 'Web Swinging', 'duration': 40},
        ]

        db.users.insert_many(users)
        db.teams.insert_many(teams)
        db.activities.insert_many(activities)
        db.leaderboard.insert_many(leaderboard)
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data.'))
