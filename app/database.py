from app.models import User, Event, Speaker, Registration

users: list[User] = []
events: list[Event] = []
speakers: list[Speaker] = [
    Speaker(id=1, name="Israel Boluwatife", topic="Full-Stack Web Development"),
    Speaker(id=2, name="Babatunde Taiwo", topic="Cloud Architecture"),
    Speaker(id=3, name="Frank Felix", topic="Machine Learning and AI"),
]
registrations: list[Registration] = []

