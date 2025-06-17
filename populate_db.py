"""
Event Management Database Test Data Population Script

This script populates the database with realistic test data using Faker.

Usage:
    python populate_db.py           # Populate with test data
    python populate_db.py clear     # Clear all data
"""

import asyncio
import random
import sys
from datetime import date, timedelta
from typing import List
from sqlalchemy import text
from faker import Faker

# Import your models and database session
from app.models import User, Event, Speaker, Registration
from app.config.database import SessionDep, get_session

# Initialize Faker for generating realistic test data
fake = Faker()


class EventDataPopulator:
    def __init__(self, session: SessionDep): # type: ignore
        self.session = session
        self.created_data = {
            'users': [],
            'events': [],
            'speakers': [],
            'registrations': 0
        }



    async def create_users(self, count: int = 50) -> List[User]:
        """Create realistic users using Faker."""
        users = []
        
        print(f"Creating {count} users...")
        
        for i in range(count):
            # Generate realistic user data
            user = User(
                user_name=fake.name(),
                user_email=fake.unique.email(),
                user_is_active=random.choices([True, False], weights=[0.9, 0.1])[0]  # 90% active
            )
            users.append(user)
            self.session.add(user)
        
        await self.session.commit()
        # Refresh users to ensure they're properly loaded
        for user in users:
            await self.session.refresh(user)
        self.created_data['users'] = users
        print(f"✅ Created {len(users)} users")
        return users

    async def create_events(self, count: int = 25) -> List[Event]:
        """Create realistic events using Faker."""
        events = []
        today = date.today()
        
        # Event types and topics for more realistic data
        event_types = [
            "Workshop", "Conference", "Seminar", "Bootcamp", "Meetup", 
            "Symposium", "Training", "Webinar", "Summit", "Forum"
        ]
        
        tech_topics = [
            "Python Programming", "Machine Learning", "Web Development", "Data Science",
            "Cloud Computing", "Cybersecurity", "Mobile Development", "DevOps",
            "Artificial Intelligence", "Blockchain", "UI/UX Design", "Software Testing",
            "Database Management", "Network Security", "Game Development", "IoT",
            "Robotics", "Digital Marketing", "E-commerce", "Project Management"
        ]
        
        venues = [
            "Convention Center", "University Auditorium", "Tech Hub", "Innovation Center",
            "Business Center", "Community Hall", "Conference Room", "Event Space",
            "Training Center", "Corporate Headquarters", "Co-working Space", "Hotel Conference Room"
        ]
        
        print(f"Creating {count} events...")
        
        for i in range(count):
            # Generate event date (mix of past, present, and future)
            if i < count * 0.3:  # 30% past events
                event_date = fake.date_between(start_date='-6M', end_date='today')
                is_open = False
            elif i < count * 0.1:  # 10% current events (within a week)
                event_date = fake.date_between(start_date='today', end_date='+7d')
                is_open = random.choice([True, False])
            else:  # 60% future events
                event_date = fake.date_between(start_date='+1d', end_date='+1y')
                is_open = True
            
            # Generate realistic event title
            event_type = random.choice(event_types)
            topic = random.choice(tech_topics)
            event_title = f"{topic} {event_type}"
            
            # Add year or level sometimes for variety
            if random.random() < 0.3:
                year = event_date.year
                event_title = f"{event_title} {year}"
            elif random.random() < 0.2:
                level = random.choice(["Beginner", "Intermediate", "Advanced"])
                event_title = f"{level} {event_title}"
            
            # Generate realistic location
            venue = random.choice(venues)
            city = fake.city()
            location = f"{venue}, {city}"
            
            event = Event(
                event_title=event_title,
                event_location=location,
                event_date=event_date,
                event_is_open=is_open
            )
            events.append(event)
            self.session.add(event)
        
        await self.session.commit()
        # Refresh events to ensure they're properly loaded
        for event in events:
            await self.session.refresh(event)
        self.created_data['events'] = events
        print(f"✅ Created {len(events)} events")
        return events

    async def create_speakers(self, count: int = 30) -> List[Speaker]:
        """Create realistic speakers using Faker."""
        speakers = []
        
        # Technology and business topics for speakers
        speaker_topics = [
            "Machine Learning and AI", "Full-Stack Web Development", "Cloud Architecture",
            "Data Science and Analytics", "Cybersecurity Best Practices", "Mobile App Development",
            "DevOps and CI/CD", "Blockchain Technology", "UI/UX Design Principles",
            "Software Engineering", "Database Optimization", "Network Security",
            "Digital Transformation", "Agile Project Management", "Leadership in Tech",
            "Startup Entrepreneurship", "Product Management", "Sales and Marketing",
            "Data Privacy and Compliance", "Internet of Things (IoT)", "Game Development",
            "Open Source Technologies", "Cloud Migration Strategies", "API Development",
            "Quality Assurance and Testing", "Business Intelligence", "E-commerce Solutions",
            "Digital Marketing Strategies", "Remote Team Management", "Tech Innovation"
        ]
        
        print(f"Creating {count} speakers...")
        
        for i in range(count):
            # Generate realistic speaker data
            speaker = Speaker(
                speaker_name=fake.name(),
                speaker_topic=random.choice(speaker_topics)
            )
            speakers.append(speaker)
            self.session.add(speaker)
        
        await self.session.commit()
        self.created_data['speakers'] = speakers
        print(f"✅ Created {len(speakers)} speakers")
        return speakers

    async def create_registrations(self, users: List[User], events: List[Event]):
        """Create realistic user registrations for events."""
        registrations_count = 0
        today = date.today()
        
        print("Creating event registrations...")
        
        for event in events:
            # Access event_date safely - it should be available since we refreshed the objects
            event_date = event.event_date
            
            # Determine number of registrations based on event characteristics
            if event_date < today:  # Past events
                base_registrations = random.randint(15, 40)
            elif event_date <= today + timedelta(days=7):  # Current events
                base_registrations = random.randint(10, 30)
            else:  # Future events
                base_registrations = random.randint(5, 25)
            
            # Don't exceed total users
            num_registrations = min(base_registrations, len(users))
            
            # Select random users for this event
            selected_users = random.sample(users, num_registrations)
            
            for user in selected_users:
                # Generate realistic registration date
                if event_date > today:
                    # Future events: registration between 1-60 days before event
                    days_before = random.randint(1, min(60, (event_date - today).days))
                    registration_date = event_date - timedelta(days=days_before)
                    # Ensure registration date is not in the future
                    if registration_date > today:
                        registration_date = today
                else:
                    # Past events: registration was 1-60 days before the event
                    days_before = random.randint(1, 60)
                    registration_date = event_date - timedelta(days=days_before)
                
                # For past events, determine if user attended
                user_attended = False
                if event_date < today:
                    # 80% attendance rate for past events
                    user_attended = random.choices([True, False], weights=[0.8, 0.2])[0]
                
                registration = Registration(
                    user_id=user.user_id,
                    event_id=event.event_id,
                    registration_date=registration_date,
                    user_attended=user_attended
                )
                self.session.add(registration)
                registrations_count += 1
        
        await self.session.commit()
        self.created_data['registrations'] = registrations_count
        print(f"✅ Created {registrations_count} registrations")

    async def populate_all_data(self, user_count: int = 50, event_count: int = 25, speaker_count: int = 30):
        """Main method to populate all test data."""
        print("🚀 Starting event management database population...")
        print("=" * 60)
        
        try:
            # Create base entities
            users = await self.create_users(user_count)
            events = await self.create_events(event_count)
            speakers = await self.create_speakers(speaker_count)
            
            # Create relationships
            await self.create_registrations(users, events)
            
            # Print summary
            print("\n🎉 Database population completed successfully!")
            print("=" * 60)
            print(f"📊 Summary:")
            print(f"   • Users: {len(self.created_data['users'])}")
            print(f"   • Events: {len(self.created_data['events'])}")
            print(f"   • Speakers: {len(self.created_data['speakers'])}")
            print(f"   • Registrations: {self.created_data['registrations']}")
            print(f"   • Database: event_management.db")
            
            return self.created_data
            
        except Exception as e:
            await self.session.rollback()
            print(f"❌ Error during data population: {e}")
            raise


async def clear_database():
    """Clear all data from the database tables."""
    print("🧹 Clearing database data...")
    
    # Create a session instance using the get_session generator
    async for session in get_session():
        try:
            # Clear data in reverse order to respect foreign key constraints
            await session.exec(text('DELETE FROM "Registration"'))
            await session.exec(text('DELETE FROM "Event"'))
            await session.exec(text('DELETE FROM "Speaker"'))
            await session.exec(text('DELETE FROM "User"'))
            await session.commit()
            print("✅ Database data cleared successfully")
            break  # Exit the async for loop after successful operation
        except Exception as e:
            await session.rollback()
            print(f"❌ Error clearing database: {e}")
            raise


async def populate_test_data():
    """Standalone function to populate test data."""
    # Create a session instance using the get_session generator
    async for session in get_session():
        try:
            populator = EventDataPopulator(session)
            return await populator.populate_all_data()
        except Exception as e:
            await session.rollback()
            raise


async def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) > 1 and sys.argv[1] == "clear":
        await clear_database()
    else:
        await populate_test_data()


if __name__ == "__main__":
    # Install required packages if not available
    try:
        import faker
    except ImportError:
        print("❌ Faker package not found. Please install it:")
        print("pip install faker")
        sys.exit(1)
    
    asyncio.run(main())

