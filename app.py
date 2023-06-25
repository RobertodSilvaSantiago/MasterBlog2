from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

DATA_FILE = "data.json"


def get_data_from_json():
    """Gets a dict from the json data file"""
    with open(DATA_FILE, 'r') as file:
        return json.load(file)


def save_data_to_json(data):
    """Saves provided dict to the json data file"""
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)


def fetch_post_by_id(id_, blog_posts):
    """Returns post based on provided id"""
    for post in blog_posts:
        if post["id"] == id_:
            return post


def add_or_update_post(post_id, form_dict, blog_posts):
    """Adds or updates a single post and saves the new/updated data to the json file"""
    post = fetch_post_by_id(post_id, blog_posts)
    if post is None:
        post = {'id': post_id}
        blog_posts.append(post)
    post.update(form_dict)
    save_data_to_json(blog_posts)


@app.route('/')
def index():
    """Homepage route"""
    blog_posts = get_data_from_json()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Add new post func if method is GET shows form to add a new post
    If method is POST, adds the post to the data file"""
    blog_posts = get_data_from_json()
    if request.method == 'POST':
        id_ = len(blog_posts) + 1
        add_or_update_post(id_, request.form, blog_posts)
        return redirect("/")
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Deletes a post from the data file"""
    blog_posts = get_data_from_json()
    post = fetch_post_by_id(post_id, blog_posts)
    if post is None:
        return "Post not found", 404
    blog_posts.remove(post)
    save_data_to_json(blog_posts)
    return redirect("/")


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Update post if method is GET shows form with current post data
    If method is POST, updates the post to the data file"""
    blog_posts = get_data_from_json()
    post = fetch_post_by_id(post_id, blog_posts)
    if post is None:
        return "Post not found", 404
    if request.method == 'POST':
        add_or_update_post(post_id, request.form, blog_posts)
        return redirect("/")
    return render_template('update.html', post=post)


@app.route('/like/<int:post_id>')
def like(post_id):
    """Increments the number of likes for a post"""
    blog_posts = get_data_from_json()
    post = fetch_post_by_id(post_id, blog_posts)
    if post is not None:
        post['likes'] = post.get('likes', 0) + 1
        save_data_to_json(blog_posts)
    return redirect("/")


if __name__ == "__main__":
    # Launch the Flask dev server
    app.run(host="0.0.0.0", port=5000, debug=True)
