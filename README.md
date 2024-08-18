# Blogly

Blogly is a simple blogging application built with Flask and SQLAlchemy, designed to add, edit, and delete users, posts, and tags from db. 

## Features

- **View All Users:** View a list of users
- **Add a User:** Add a new user by providing full name, and image. 
- **Edit User Details:** Edit the details of an existing user.
- **Delete a User:** Remove a user from the database.
- **View User's Posts:** View a list of posts for a specific user.
- **Add a Post:** Create a new post for a user, including a title and content.
- **Edit a Post:** Modify the content or title of an existing post.
- **Delete a Post:** Remove a post from the database.
- **View and Manage Tags:** 
  - **Add a Tag:** Create a new tag to categorize posts.
  - **Edit a Tag:** Modify the name of an existing tag.
  - **Delete a Tag:** Remove a tag from the database.
  - **Assign Tags to Posts:** When creating or editing a post, assign one or more tags to it for better categorization.
  - **View Tags on Posts:** Tags associated with a post are displayed as badges on both the homepage and post detail page.

## Technologies Used

- **Flask**: The web framework used to build the application.
- **SQLAlchemy**: An ORM used for database management.
- **PostgreSQL**: The relational database used to store user data.
- **Jinja**: Template engine for rendering HTML.
- **HTML/CSS**: Used for frontend structure and styling.
- **Flask-DebugToolbar**: For debugging the application during development.

