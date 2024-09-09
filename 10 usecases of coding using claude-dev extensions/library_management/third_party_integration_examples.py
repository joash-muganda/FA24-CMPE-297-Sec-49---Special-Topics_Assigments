import requests
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Example 1: Making HTTP requests with the requests library
def fetch_github_user(username):
    """
    Fetch user information from GitHub API.
    
    Args:
        username (str): GitHub username to fetch information for.
    
    Returns:
        dict: User information if successful, None otherwise.
    """
    url = f"https://api.github.com/users/{username}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching GitHub user: {e}")
        return None

# Example usage of fetch_github_user
def github_api_example():
    user_info = fetch_github_user("octocat")
    if user_info:
        print(f"GitHub User: {user_info['login']}")
        print(f"Name: {user_info['name']}")
        print(f"Public Repos: {user_info['public_repos']}")
    else:
        print("Failed to fetch GitHub user information.")

# Example 2: Performing CRUD operations with SQLAlchemy
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(120), unique=True)

    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}')>"

def setup_database():
    """Set up the database and create tables."""
    engine = create_engine('sqlite:///example.db', echo=True)
    Base.metadata.create_all(engine)
    return engine

def crud_operations_example():
    engine = setup_database()
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Create
        new_user = User(name="John Doe", email="john@example.com")
        session.add(new_user)
        session.commit()
        logger.info(f"Created user: {new_user}")

        # Read
        user = session.query(User).filter_by(name="John Doe").first()
        logger.info(f"Read user: {user}")

        # Update
        user.email = "johndoe@example.com"
        session.commit()
        logger.info(f"Updated user: {user}")

        # Delete
        session.delete(user)
        session.commit()
        logger.info(f"Deleted user: {user}")

    except Exception as e:
        logger.error(f"An error occurred during CRUD operations: {e}")
        session.rollback()
    finally:
        session.close()

# Example 3: Interacting with a REST API (using JSONPlaceholder as an example)
class JSONPlaceholderAPI:
    BASE_URL = "https://jsonplaceholder.typicode.com"

    @staticmethod
    def get_posts():
        """Fetch all posts from the API."""
        try:
            response = requests.get(f"{JSONPlaceholderAPI.BASE_URL}/posts")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching posts: {e}")
            return None

    @staticmethod
    def create_post(title, body, user_id):
        """Create a new post."""
        try:
            data = {
                "title": title,
                "body": body,
                "userId": user_id
            }
            response = requests.post(f"{JSONPlaceholderAPI.BASE_URL}/posts", json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error creating post: {e}")
            return None

    @staticmethod
    def update_post(post_id, title, body, user_id):
        """Update an existing post."""
        try:
            data = {
                "id": post_id,
                "title": title,
                "body": body,
                "userId": user_id
            }
            response = requests.put(f"{JSONPlaceholderAPI.BASE_URL}/posts/{post_id}", json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error updating post: {e}")
            return None

    @staticmethod
    def delete_post(post_id):
        """Delete a post."""
        try:
            response = requests.delete(f"{JSONPlaceholderAPI.BASE_URL}/posts/{post_id}")
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            logger.error(f"Error deleting post: {e}")
            return False

def rest_api_example():
    # Get all posts
    posts = JSONPlaceholderAPI.get_posts()
    if posts:
        logger.info(f"Fetched {len(posts)} posts")

    # Create a new post
    new_post = JSONPlaceholderAPI.create_post("New Post", "This is a new post body", 1)
    if new_post:
        logger.info(f"Created new post: {new_post}")

    # Update the post
    updated_post = JSONPlaceholderAPI.update_post(new_post['id'], "Updated Post", "This is an updated post body", 1)
    if updated_post:
        logger.info(f"Updated post: {updated_post}")

    # Delete the post
    if JSONPlaceholderAPI.delete_post(new_post['id']):
        logger.info(f"Deleted post with ID: {new_post['id']}")

if __name__ == "__main__":
    print("Example 1: GitHub API")
    github_api_example()

    print("\nExample 2: SQLAlchemy CRUD Operations")
    crud_operations_example()

    print("\nExample 3: REST API Interaction")
    rest_api_example()