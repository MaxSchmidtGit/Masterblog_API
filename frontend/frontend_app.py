# Import necessary modules from Flask
from flask import Flask, render_template

# Create a new Flask application instance
app = Flask(__name__)

# Define a route for the root URL ("/") of the web application
@app.route('/', methods=['GET'])
def home():
    """
    This function handles GET requests to the root URL ("/").
    It returns the rendered HTML template "index.html" to display the homepage.
    """
    return render_template("index.html")  # Render the "index.html" file located in the "templates" directory

# Main entry point to run the Flask application
if __name__ == '__main__':
    # Run the Flask development server on the specified host and port
    app.run(host="0.0.0.0", port=5001, debug=True)  # Enable debug mode for detailed error messages
