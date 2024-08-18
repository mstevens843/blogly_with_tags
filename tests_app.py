from unittest import TestCase
from models import db, User, Post
from app import app
from datetime import datetime

class BloglyAppTestCase(TestCase):
    """Test Flask routes for Blogly, including posts."""

    def setUp(self):
        """Set up test client and sample data within the application context."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly_db'
        self.client = app.test_client()

        with app.app_context():
            db.drop_all()
            db.create_all()

            # Add sample user
            user = User(first_name="Mathew", last_name="Stevens", image_url="https://cdn-icons-png.flaticon.com/512/149/149071.png")
            db.session.add(user)
            db.session.commit()

            # Add sample post
            post = Post(title="Test Post", content="This is a test post.", user_id=user.id, created_at=datetime.utcnow())
            db.session.add(post)
            db.session.commit()

            self.user_id = user.id
            self.post_id = post.id

    def tearDown(self):
        """Clean up fouled transactions within the application context."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_post(self):
        """Test creating a new post."""
        with self.client as client:
            data = {"title": "New Post", "content": "This is a new test post."}
            res = client.post(f"/users/{self.user_id}/posts/new", data=data, follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn(b"New Post", res.data)

            # Check that the post was added to the database
            with app.app_context():
                post = Post.query.filter_by(title="New Post").first()
                self.assertIsNotNone(post)

    def test_view_post(self):
        """Test viewing a post."""
        with self.client as client:
            res = client.get(f"/posts/{self.post_id}")
            self.assertEqual(res.status_code, 200)
            self.assertIn(b"Test Post", res.data)
            self.assertIn(b"This is a test post.", res.data)

    def test_edit_post(self):
        """Test editing a post."""
        with self.client as client:
            data = {"title": "Updated Post", "content": "This is an updated test post."}
            res = client.post(f"/posts/{self.post_id}/edit", data=data, follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn(b"Updated Post", res.data)

            # Verify that the post was updated in the database
            with app.app_context():
                post = Post.query.get(self.post_id)
                self.assertEqual(post.title, "Updated Post")
                self.assertEqual(post.content, "This is an updated test post.")

    def test_delete_post(self):
        """Test deleting a post."""
        with self.client as client:
            res = client.post(f"/posts/{self.post_id}/delete", follow_redirects=True)
            self.assertEqual(res.status_code, 200)

            # Verify that the post was deleted from the database
            with app.app_context():
                post = Post.query.get(self.post_id)
                self.assertIsNone(post)

    def test_user_list(self):
        """Test the users list page."""
        with self.client as client:
            res = client.get("/users")
            self.assertEqual(res.status_code, 200)
            self.assertIn(b"Mathew Stevens", res.data)

    def test_user_detail(self):
        """Test the user detail page."""
        with app.app_context():
            user = User.query.first()

        with self.client as client:
            res = client.get(f"/users/{user.id}")
            self.assertEqual(res.status_code, 200)
            self.assertIn(b"Mathew Stevens", res.data)
