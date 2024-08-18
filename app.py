from flask import Flask, redirect, render_template, request, flash
from models import db, connect_db, User, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)

# Set a secret key for sessions
app.config['SECRET_KEY'] = 'frgtrhyjuj7grfr3gtghyt5h' 
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# Initialize the database connection
connect_db(app)


# Flask routes
@app.route('/')
def home():
    """Show the homepage with a list of posts."""
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('home.html', posts=posts)


@app.route('/users')
def list_users():
    """Show all users, ordered by last name and first name."""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('user_list.html', users=users)


@app.route('/users/new', methods=["GET", "POST"])
def new_user():
    """Display a form to add a new user or handle the form submission."""
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        image_url = request.form['image_url'] or None

        new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/users')
    return render_template('new_user_form.html')


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show information about the given user."""
    user = User.query.get_or_404(user_id)
    return render_template('user_details.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["GET", "POST"])
def edit_user(user_id):
    """Show a form to edit a user or handle the form submission."""
    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.image_url = request.form['image_url']
        db.session.commit()

        return redirect(f'/users/{user_id}')
    return render_template('edit_user_form.html', user=user)


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Handle the deletion of a user."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')


# Post routes ######################################################################
@app.route('/users/<int:user_id>/posts/new', methods=["GET", "POST"])
def new_post(user_id):
    """Show form to add a new post for a specific user and handle submission."""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        tag_ids = request.form.getlist('tag_ids')
  # This retrieves the selected tag IDs as a list

        # Print to check if tag_ids is being received
        print(f"Received tag IDs: {tag_ids}")

        # Create the post
        new_post = Post(title=title, content=content, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()

        # Associate tags with the new post
        for tag_id in tag_ids:
            post_tag = PostTag(post_id=new_post.id, tag_id=int(tag_id))
            db.session.add(post_tag)
        db.session.commit()

        flash(f'Post "{title}" added with tags!')
        return redirect(f'/users/{user_id}')

    return render_template('new_post_form.html', user=user, tags=tags)







@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show details for a specific post, including associated tags."""
    post = Post.query.get_or_404(post_id)
    return render_template('post_details.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["GET", "POST"])
def edit_post(post_id):
    """Show form to edit post and handle submission."""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    if request.method == "POST":
        post.title = request.form['title']
        post.content = request.form['content']
        tag_ids = request.form.getlist('tag_ids')

        # Print to check if tag_ids is being received
        print(f"Received tag IDs: {tag_ids}")

        # Update tags for the post
        post.tags = [Tag.query.get(tag_id) for tag_id in tag_ids]
        db.session.commit()

        flash(f'Post "{post.title}" edited!')
        return redirect(f'/posts/{post.id}')
    
    return render_template('edit_post_form.html', post=post, tags=tags)



@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Handle deletion of a post."""
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()

    flash(f'Post "{post.title}" deleted!')
    return redirect(f'/users/{user_id}')


# TAGS ROUTES #####################################################################
@app.route('/tags')
def list_tags():
    """List all tags."""
    tags = Tag.query.all()
    return render_template('tag_list.html', tags=tags)


@app.route('/tags/new', methods=['GET', 'POST'])
def add_tag():
    """Add a new tag."""
    if request.method == 'POST':
        name = request.form['name']
        new_tag = Tag(name=name)
        db.session.add(new_tag)
        db.session.commit()
        return redirect('/tags')
    
    return render_template('tag_form.html')


@app.route('/tags/<int:tag_id>/edit', methods=['GET', 'POST'])
def edit_tag(tag_id):
    """Edit an existing tag."""
    tag = Tag.query.get_or_404(tag_id)

    if request.method == 'POST':
        tag.name = request.form['name']
        db.session.commit()
        return redirect('/tags')
    
    return render_template('tag_edit_form.html', tag=tag)


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """Delete tag."""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')
