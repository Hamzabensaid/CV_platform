from faker import Faker
from pymongo import MongoClient
import random

fake = Faker()

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client["cv_database"]
collection = db["candidates"]

# Predefined lists
technologies = ["Python", "JavaScript", "React", "Node.js", "MongoDB", "Django", "FastAPI"]
languages = ["English", "French", "Arabic"]

def generate_education():
    return [
        {
            "degree": "Bachelor in Computer Science",
            "school": fake.company(),
            "year": str(random.randint(2015, 2022))
        }
    ]

def generate_experience():
    return [
        {
            "title": "Software Engineer",
            "company": fake.company(),
            "duration": f"{random.randint(1, 5)} years",
            "technologies": random.sample(technologies, 3)
        }
    ]

def generate_cv():
    return {
        "full_name": fake.name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "location": fake.city(),
        "education": generate_education(),
        "experience": generate_experience(),
        "skills": random.sample(technologies, 5),
        "languages": random.sample(languages, 2)
    }

# Insert fake CVs
for _ in range(10):  # Generate 10 fake CVs
    collection.insert_one(generate_cv())

print("✅ Fake CVs inserted successfully!")
