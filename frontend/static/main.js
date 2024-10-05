// Function that runs once the window is fully loaded
window.onload = function() {
    // Attempt to retrieve the API base URL from the local storage
    var savedBaseUrl = localStorage.getItem('apiBaseUrl');

    // If a base URL is found in local storage, set it in the input field and load the posts
    if (savedBaseUrl) {
        document.getElementById('api-base-url').value = savedBaseUrl;
        loadPosts();  // Call the function to load posts when a base URL is present
    }
}

// Function to fetch all the posts from the API and display them on the page
function loadPosts() {
    // Retrieve the base URL from the input field and save it to local storage
    var baseUrl = document.getElementById('api-base-url').value;
    localStorage.setItem('apiBaseUrl', baseUrl);  // Store the base URL for future use

    // Use the Fetch API to send a GET request to the /posts endpoint
    fetch(baseUrl + '/posts')
        .then(response => response.json())  // Parse the JSON data from the response
        .then(data => {  // Once the data is ready, iterate through the list of posts
            // Clear out the post container before displaying new posts
            const postContainer = document.getElementById('post-container');
            postContainer.innerHTML = '';

            // For each post in the response, create a new post element and add it to the page
            data.forEach(post => {
                // Create a new div for each post and set its class for styling
                const postDiv = document.createElement('div');
                postDiv.className = 'post';

                // Set the inner HTML of the post div, including title, content, and a delete button
                postDiv.innerHTML = `
                    <h2>${post.title}</h2>
                    <p>${post.content}</p>
                    <button onclick="deletePost(${post.id})">Delete</button>
                `;

                // Append the newly created post div to the post container
                postContainer.appendChild(postDiv);
            });
        })
        .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}

// Function to send a POST request to the API to add a new post
function addPost() {
    // Retrieve the values for the new post from the input fields
    var baseUrl = document.getElementById('api-base-url').value;
    var postTitle = document.getElementById('post-title').value;
    var postContent = document.getElementById('post-content').value;

    // Use the Fetch API to send a POST request to the /posts endpoint with the new post data
    fetch(baseUrl + '/posts', {
        method: 'POST',  // Specify the HTTP method as POST
        headers: { 'Content-Type': 'application/json' },  // Set the request headers for JSON data
        body: JSON.stringify({ title: postTitle, content: postContent })  // Send the post data as JSON
    })
    .then(response => response.json())  // Parse the JSON data from the response
    .then(post => {
        console.log('Post added:', post);  // Log the new post to the console
        loadPosts();  // Reload the list of posts after adding a new one
    })
    .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}

// Function to send a DELETE request to the API to delete a post
function deletePost(postId) {
    // Retrieve the base URL from the input field
    var baseUrl = document.getElementById('api-base-url').value;

    // Use the Fetch API to send a DELETE request to the specific post's endpoint
    fetch(baseUrl + '/posts/' + postId, {
        method: 'DELETE'  // Specify the HTTP method as DELETE
    })
    .then(response => {
        console.log('Post deleted:', postId);  // Log the ID of the deleted post to the console
        loadPosts();  // Reload the list of posts after deleting one
    })
    .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}
