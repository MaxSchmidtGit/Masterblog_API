# Import necessary modules from Flask and CORS
from flask import Flask, jsonify, request
from flask_cors import CORS

# Initialize Flask application
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) for the entire application
CORS(app)  # This will allow cross-origin requests from any domain

# Hardcoded list of blog posts with initial values
POSTS = [
    {"id": 1, "title": "a post", "content": "This c is the first post."},
    {"id": 2, "title": "b post", "content": "This a is the second post."},
    {"id": 3, "title": "c post", "content": "This b is the third post."},
]

@app.route('/api/posts', methods=['GET', 'POST', 'PUT'])
def get_posts():
    """
    Endpoint to handle GET, POST, and PUT requests for blog posts.
    - GET: Returns the list of posts. Supports sorting based on 'title' or 'content' and direction 'asc' or 'desc'.
    - POST: Adds a new blog post with unique 'id', 'title', and 'content'.
    - PUT: Updates an existing blog post based on 'id'. Supports updating 'title' and/or 'content'.
    """

    if request.method == 'GET':
        # Handle GET requests
        sort = request.args.get('sort')  # Retrieve the 'sort' parameter from the request
        direction = request.args.get('direction')  # Retrieve the 'direction' parameter ('asc' or 'desc')
        
        # If no sorting parameters are provided, return all posts unsorted
        if sort is None or direction is None:
            return jsonify(POSTS)
        else:
            # Sort posts by 'title' or 'content' based on the provided parameters
            if sort == 'title':
                sorted_list = sorted(POSTS, key=lambda x: x['title'])
                if direction == 'desc':
                    sorted_list.reverse()
                return jsonify(sorted_list)
            else:
                sorted_list = sorted(POSTS, key=lambda x: x['content'])
                if direction == 'desc':
                    sorted_list.reverse()
                return jsonify(sorted_list)

    elif request.method == 'POST':
        # Handle POST requests to add a new blog post
        data = request.get_json()  # Get the request data in JSON format
        title = data.get('title')  # Extract 'title' from the JSON data
        content = data.get('content')  # Extract 'content' from the JSON data
        
        # Check if both 'title' and 'content' are provided
        if title is None or content is None:
            error_message = {'error': 'All data fields must be provided'}
            return jsonify(error_message), 400  # Return error message with status code 400
        
        # Generate a unique ID by iterating through a range until an unused ID is found
        id_list = [post['id'] for post in POSTS]
        for number in range(10000000):
            if number not in id_list:
                unique_id = number
                break

        # Create a new post and add it to the list
        new_post = {"id": unique_id, "title": title, "content": content}
        POSTS.append(new_post)
        return jsonify(new_post)

    elif request.method == 'PUT':
        # Handle PUT requests to update an existing blog post
        data = request.get_json()  # Get the request data in JSON format
        post_id = int(request.args.get('id'))  # Retrieve the 'id' parameter from the request
        
        # Search for the post with the matching 'id'
        for index, post in enumerate(POSTS):
            if post['id'] == post_id:
                edit_post = post
                del POSTS[index]  # Remove the old post to update it later
                break
            # If no post is found, return an error message
            if POSTS[index]['title'] == POSTS[-1]['title']:
                return jsonify({'error': f'Post with id: {post_id} could not be found'}), 400

        # Update 'title' and/or 'content' fields if provided in the data
        if 'title' in data:
            edit_post['title'] = data['title']
        if 'content' in data:
            edit_post['content'] = data['content']

        # Re-add the updated post to the list and return it
        POSTS.append(edit_post)
        return jsonify(edit_post)
    
@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete(post_id):
    """
    Endpoint to delete a blog post by its unique ID.
    - DELETE: Removes a post from the list based on the provided 'post_id'.
    """

    for index, post in enumerate(POSTS):
        if post['id'] == post_id:
            del POSTS[index]  # Delete the post with the matching ID
            return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200
    return jsonify({'error': f'Post with id: {post_id} could not be found'}), 400

@app.route('/api/posts/search')
def search():
    """
    Endpoint to search for posts based on 'title' or 'content'.
    - GET: Returns a list of posts that match the search criteria.
    """

    title_search = request.args.get('title')  # Retrieve 'title' parameter from the request
    content_search = request.args.get('content')  # Retrieve 'content' parameter from the request
    matches = []  # Initialize a list to store matching posts

    # Use empty strings if no search parameters are provided
    if title_search is None:
        title_search = ""
    if content_search is None:
        content_search = ""

    # Check each post to see if both 'title' and 'content' contain the search parameters
    for post in POSTS:
        if content_search in post['content'] and title_search in post['title']:
            matches.append(post)

    return jsonify(matches)  # Return the list of matching posts


if __name__ == '__main__':
    # Run the application on the specified host and port
    app.run(host="0.0.0.0", port=5002, debug=True)
