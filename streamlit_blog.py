import streamlit as st
import sqlite3

# Function to create a new SQLite3 database and table for blog posts
def create_database():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS posts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT NOT NULL,
                 content TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Function to create a new SQLite3 database and table for user accounts
def create_user_database():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Function to register a new user
def register_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

# Function to authenticate a user
def authenticate_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user

# Function to add a new post to the database
def add_post(title, content):
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
    conn.commit()
    conn.close()

# Function to edit an existing post in the database
def edit_post(post_id, title, content):
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute("UPDATE posts SET title=?, content=? WHERE id=?", (title, content, post_id))
    conn.commit()
    conn.close()

# Function to delete a post from the database
def delete_post(post_id):
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute("DELETE FROM posts WHERE id=?", (post_id,))
    conn.commit()
    conn.close()

# Function to retrieve all posts from the database
def get_all_posts():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts")
    posts = c.fetchall()
    conn.close()
    return posts

# Function to retrieve a single post by its ID from the database
def get_post_by_id(post_id):
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE id=?", (post_id,))
    post = c.fetchone()
    conn.close()
    return post

# Streamlit interface for user registration
def registration():
    st.title("User Registration")
    username = st.text_input("Enter username:")
    password = st.text_input("Enter password:", type="password")
    if st.button("Register"):
        if username and password:
            create_user_database()
            register_user(username, password)
            st.success("Registration successful! Please login.")
        else:
            st.warning("Please enter both username and password.")

# Streamlit interface for user login
def login():
    st.title("User Login")
    username = st.text_input("Enter username:")
    password = st.text_input("Enter password:", type="password")
    if st.button("Login"):
        if username and password:
            user = authenticate_user(username, password)
            if user:
                st.success(f"Welcome, {username}!")
                st.session_state.logged_in = True
            else:
                st.error("Invalid username or password.")
        else:
            st.warning("Please enter both username and password.")

# Streamlit interface for user logout
def logout():
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.success("You have been logged out.")

# Streamlit interface
def main():
    st.title("Simple Blog with Streamlit and SQLite3")

    # Create database if not exists
    create_database()

    # Sidebar
    st.sidebar.header("Menu")
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        menu_choice = st.sidebar.selectbox("Select operation", ("Add Post", "Edit Post", "Delete Post", "View Posts", "Logout"))
    else:
        menu_choice = st.sidebar.selectbox("Select operation", ("Login", "Register"))

    if menu_choice == "Register":
        registration()
    elif menu_choice == "Login":
        login()
    elif menu_choice == "Logout":
        logout()
    elif menu_choice == "Add Post" and st.session_state.logged_in:
        st.header("Add New Post")
        title = st.text_input("Enter title:")
        content = st.text_area("Enter content:")
        if st.button("Add Post"):
            if title and content:
                add_post(title, content)
                st.success("Post added successfully!")
            else:
                st.warning("Please enter both title and content.")

    elif menu_choice == "Edit Post" and st.session_state.logged_in:
        st.header("Edit Post")
        post_id = st.number_input("Enter post ID to edit:")
        if post_id:
            post = get_post_by_id(post_id)
            if post:
                st.write(f"Current Title: {post[1]}")
                new_title = st.text_input("Enter new title:", value=post[1])
                st.write(f"Current Content: {post[2]}")
                new_content = st.text_area("Enter new content:", value=post[2])
                if st.button("Update Post"):
                    edit_post(post_id, new_title, new_content)
                    st.success("Post updated successfully!")
            else:
                st.warning("Post not found.")

    elif menu_choice == "Delete Post" and st.session_state.logged_in:
        st.header("Delete Post")
        post_id = st.number_input("Enter post ID to delete:")
        if st.button("Delete Post"):
            if post_id:
                post = get_post_by_id(post_id)
                if post:
                    delete_post(post_id)
                    st.success("Post deleted successfully!")
                else:
                    st.warning("Post not found.")
            else:
                st.warning("Please enter post ID.")

    elif menu_choice == "View Posts":
        st.header("All Posts")
        posts = get_all_posts()
        if posts:
            for post in posts:
                st.write(f"**Title:** {post[1]}")
                st.write(f"**Content:** {post[2]}")
                st.write("---")
        else:
            st.info("No posts found.")

if __name__ == "__main__":
    main()
