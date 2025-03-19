import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from flask import Flask
#from models2 import User, Post, Base
from models import db, User, Post
from datetime import datetime
from flask import Flask


# Load environment variables
load_dotenv()
#print(f"{os.getenv('DB_USER')}")
# Create the connection URL using environment variables
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME')}"
DATABASE_URL_DEFAULT = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}/postgres"

# # Create the engine
# engine = create_engine(DATABASE_URL)


# # Check if the database exists, if not create it
# if not database_exists(DATABASE_URL):
#     # Connect to default database first
#     engine = create_engine(DATABASE_URL_DEFAULT)
#     create_database
#     (DATABASE_URL)
#     print("Database 'testF' created successfully")
# else:
#     engine = create_engine(DATABASE_URL)
# Check if the database exists, if not create it
if not database_exists(DATABASE_URL):
    # Connect to default database first
    default_engine = create_engine(DATABASE_URL_DEFAULT)
    with default_engine.connect() as conn:
        #conn.execute("COMMIT")  # Close any open transactions
        create_database(DATABASE_URL)
    print(f"Database '{os.getenv('DB_NAME')}' created successfully")

# Create a Flask app and configure it
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the app with Flask-SQLAlchemy
db.init_app(app)


# # Only uncomment if models.py is use the Base class
# # Base.metadata.create_all(engine)
# db.create_all(engine)

# Session = sessionmaker(bind=engine)
# session = Session()


with app.app_context():
    db.create_all()
    # Create users
    users = [
        User(username='johnK', email='john@example.com', created_at=datetime(2024, 10, 3, 10, 10, 20)),
        User(username='janeS', email='jane@example.com', created_at=datetime(2024, 9, 10, 12, 15, 30)),
        User(username='bobJ', email='bob@example.com', created_at=datetime(2024, 8, 3, 8, 10, 40)),
        User(username='aliceW', email='alice@example.com', created_at=datetime(2025, 1, 3, 5, 40, 10)),
        User(username='jilK', email='jil@example.com', created_at=datetime(2025, 2, 4, 5, 15, 30))
    ]
    db.session.add_all(users)
    db.session.commit()

    # Create posts
    posts = [
        Post(title="To do", content="Lets do it", created_at=datetime(2025, 11, 3, 20, 30, 50), user_id=2),
        Post(title="To Let", content="Apt Relet", created_at=datetime(2024, 12, 9, 10, 30, 10), user_id=3),
        Post(title="Trip", content="Macau Details", created_at=datetime(2024, 10, 2, 5, 45, 33), user_id=1),
        Post(title="Hello di", content="Welcome message", created_at=datetime(2025, 2, 4, 6, 30, 20), user_id=4),
        Post(title="Itinerary", content="Trip items", created_at=datetime(2025, 3, 9, 11, 40, 50), user_id=5)
    ]
    db.session.add_all(posts)
    db.session.commit()

    # # Create users
    # users = [
    #     User(id=1, username='johnK', email='john@example.com', created_at=datetime(2024, 10, 3, 10, 10, 20)),
    #     User(id=2, username='janeS', email='jane@example.com', created_at=datetime(2024, 9, 10, 12, 15, 30)),
    #     User(id=3, username='bobJ', email='bob@example.com', created_at=datetime(2024, 8, 3, 8, 10, 40)),
    #     User(id=4, username='aliceW', email='alice@example.com', created_at=datetime(2025, 1, 3, 5, 40, 10)),
    #     User(id=5, username='jilK', email='jil@example.com', created_at=datetime(2025, 2, 4, 5, 15, 30))
    # ]
    # db.session.add_all(users)
    # db.session.commit()

    # # Create posts
    # posts = [
    #     Post(id=1, title="To do", content="Lets do it", created_at=datetime(2025, 11, 3, 20, 30, 50), user_id=2),
    #     Post(id=2, title="To Let", content="Apt Relet", created_at=datetime(2024, 12, 9, 10, 30, 10), user_id=3),
    #     Post(id=3, title="Trip", content="Macau Details", created_at=datetime(2024, 10, 2, 5, 45, 33), user_id=1),
    #     Post(id=4, title="Hello di", content="Welcome message", created_at=datetime(2025, 2, 4, 6, 30, 20), user_id=4),
    #     Post(id=5, title="Itinerary", content="Trip items", created_at=datetime(2025, 3, 9, 11, 40, 50), user_id=5)
    # ]
    # db.session.add_all(posts)
    # db.session.commit()



# # Example usage
# if __name__ == '__main__':
#     # Create users
#     users = [
#         User(id=1, username='johnK', email='john@example.com', created_at=datetime(2024, 10, 3, 10, 10, 20)),
#         User(id=2, username='janeS', email='jane@example.com', created_at=datetime(2024, 9, 10, 12, 15, 30)),
#         User(id=3, username='bobJ', email='bob@example.com', created_at=datetime(2024, 8, 3, 8, 10, 40)),
#         User(id=4, username='aliceW', email='alice@example.com', created_at=datetime(2025, 1, 3, 5, 40, 10)),
#         User(id=5, username='jilK', email='jil@example.com', created_at=datetime(2025, 2, 4, 5, 15, 30))
#     ]

#     session.add_all(users)
#     session.commit()

#     # Create posts
#     posts = [
#         Post(id=1, title="To do", content="Lets do it", created_at=datetime(2025, 11, 3, 20, 30, 50), user_id=2),
#         Post(id=2, title="To Let", content="Apt Relet", created_at=datetime(2024, 12, 9, 10, 30, 10), user_id=3),
#         Post(id=3, title="Trip", content="Macau Details", created_at=datetime(2024, 10, 2, 5, 45, 33), user_id=1),
#         Post(id=4, title="Hello di", content="Welcome message", created_at=datetime(2025, 2, 4, 6, 30, 20), user_id=4),
#         Post(id=5, title="Itinerary", content="Trip items", created_at=datetime(2025, 3, 9, 11, 40, 50), user_id=5)
#     ]
#     session.add_all(posts)
#     session.commit()

#     # Query to select a post by post_id
#     post_f = session.query(Post).filter_by(id=2).first()  

#     if post_f:
#         print(f"Post ID: {post_f.id}, Post Title: {post_f.title}, Post Content {post_f.content}")
#     else:
#         print("No post found with the given post ID.")

