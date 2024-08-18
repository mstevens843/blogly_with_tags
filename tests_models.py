from unittest import TestCase
from models import db, User
from app import app

class BloglyAppTestCase(TestCase):
    """Test Flask models for Blogly."""

    def setUp(self):
        """Set up test client and sample data within the application context."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly_db'
        self.client = app.test_client()

        # Wrap in app context
        with app.app_context():
            db.drop_all()
            db.create_all()

            # Add sample data
            user = User(first_name="Mathew", last_name="Stevens", image_url="https://cdn-icons-png.flaticon.com/512/149/149071.png")
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        """Clean up fouled transactions within the application context."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_list(self):
        """Test the users list page."""
        with self.client as client:
            res = client.get("/users")
            self.assertEqual(res.status_code, 200)
            self.assertIn(b"Mathew Stevens", res.data)

    def test_user_detail(self):
        """Test the user detail page."""
        with self.client as client:
            user = User.query.first()
            res = client.get(f"/users/{user.id}")
            self.assertEqual(res.status_code, 200)
            self.assertIn(b"Mathew Stevens", res.data)

    def test_add_user(self):
        """Test adding a new user without providing an image URL."""
        with self.client as client:
            data = {"first_name": "Mathew", "last_name": "Stevens", "image_url": ""}
            res = client.post("/users/new", data=data, follow_redirects=True)
            self.assertEqual(res.status_code, 200)

            # Check that the user was added
            self.assertIn(b"Mathew Stevens", res.data)

            # Fetch the user from the database
            user = User.query.filter_by(first_name="Mathew", last_name="Stevens").first()

            # Check that the default image URL is applied
            self.assertEqual(user.image_url, "https://cdn-icons-png.flaticon.com/512/149/149071.png")

    def test_default_image_url(self):
        """Test that default image URL is applied when no image URL is provided."""
        with app.app_context():
            user = User(first_name="John", last_name="Doe")  # No image_url provided
            db.session.add(user)
            db.session.commit()

            fetched_user = User.query.filter_by(first_name="John").first()
            self.assertEqual(fetched_user.image_url, "https://cdn-icons-png.flaticon.com/512/149/149071.png")
