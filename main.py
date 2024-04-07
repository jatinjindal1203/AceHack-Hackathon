from flask import Flask, render_template, request, redirect, url_for, session
import secrets

app = Flask(__name__)

# Generate a random secret key
secret_key = secrets.token_hex(16)

# Set the secret key for the Flask app
app.secret_key = secret_key

# Dummy data for demonstration purposes

posts = [
    {'id': 1, 'author': 'John Doe', 'title': 'First post', 'content': 'This is my first post!', 'date_posted': 'April 1, 2024', 'category': 'IT','email': 'john@example.com'},
    {'id': 2, 'author': 'Jane Smith', 'title': 'Second post', 'content': 'Another day, another post.', 'date_posted': 'April 2, 2024', 'category': 'IT', 'email': 'jane@example.com'}
]

user_array = [
    {'full_name': 'John Doe', 'email': 'john@example.com', 'password': 'password123', 'dob': '1990-01-01', 'gender': 'male'},
    {'full_name': 'Jane Smith', 'email': 'jane@example.com', 'password': 'password456', 'dob': '1995-05-05', 'gender': 'female'}
]

def generate_post_id():
    if posts:
        return max(post['id'] for post in posts) + 1
    else:
        return 1 

@app.route('/')
@app.route('/home')
def home():
    if 'login_email' in session:
        return render_template('home.html', posts=posts)
    else:
        return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/mypost')
def mypost():
    if 'login_email' in session:
        login_email = session['login_email']
        user_posts = [post for post in posts if post['email'] == login_email]
        return render_template('mypost.html', posts=user_posts)
    else:
        # Redirect to login page if user is not logged in
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Check if user exists and credentials match
        for user in user_array:
            if user['email'] == email and user['password'] == password:
                # Redirect to home page if credentials are correct
                session['login_email'] = email
                return redirect(url_for('home'))
        
        # If no matching user found, display error message
        error = 'Invalid email or password. Please try again.'
        return render_template('login.html', title='Login', error=error)
    else:
        return render_template('login.html', title='Login')
    
@app.route('/logout')
def logout():
    # Remove email from session
    session.pop('login_email', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])  # Add methods=['GET', 'POST'] to allow both GET and POST requests
def register():
    if request.method == 'POST':
        # Retrieve form data
        full_name = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        dob = request.form['dob']
        gender = request.form['gender']
        
        # Create user object
        user = {
            'full_name': full_name,
            'email': email,
            'password': password,
            'dob': dob,
            'gender': gender
        }
        
        # Add user to user_array
        user_array.append(user)
        
        # Redirect to login page
        return redirect(url_for('login'))
    else:
        # Handle GET request (render the register page)
        return render_template('register.html')


@app.route('/addpost', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        category = request.form['category']
        post_id = generate_post_id()
        # Add date_posted logic here if needed
        new_post = {'id': post_id ,'author': author, 'title': title, 'content': content, 'date_posted': 'April 6, 2024', 'category': category, 'email': session['login_email']}  # Dummy date for demonstration
        posts.insert(0,new_post)
        return redirect(url_for('home'))
    else:
        return render_template('add_post.html', title='Add Post')

@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    # Find the post with the given post_id and remove it from the posts list
    for i, post in enumerate(posts):
        if post['id'] == post_id:
            del posts[i]
            break  # Stop searching after deleting the post
    return redirect(url_for('mypost'))  # Redirect to mypost route after deleting the post

@app.route('/enhance')
def enhance():
    return render_template('enhance.html')

if __name__ == '__main__':
    app.run(debug=True)
