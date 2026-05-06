// Function that runs once the window is fully loaded
window.onload = function() {
    // Attempt to retrieve the API base URL from the local storage
    var savedBaseUrl = localStorage.getItem('apiBaseUrl');
    // If a base URL is found in local storage, load the posts
    if (savedBaseUrl) {
        document.getElementById('api-base-url').value = savedBaseUrl;
        loadPosts();
    }
}

// Function to fetch all the posts from the API and display them on the page
function loadPosts() {
    // Retrieve the base URL from the input field and save it to local storage
    var baseUrl = document.getElementById('api-base-url').value;
    localStorage.setItem('apiBaseUrl', baseUrl);

    // Retrieve sorting parameters
    var sortField = document.getElementById('sort-field').value;
    var sortDirection = document.getElementById('sort-direction').value;

    var url = baseUrl + '/posts';
    var params = [];
    if (sortField) params.push('sort=' + sortField);
    if (sortDirection) params.push('direction=' + sortDirection);
    
    if (params.length > 0) {
        url += '?' + params.join('&');
    }

    // Use the Fetch API to send a GET request to the /posts endpoint
    fetch(url)
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw err; });
            }
            return response.json();
        })
        .then(data => {  // Once the data is ready, we can use it
            if (Array.isArray(data)) {
                displayPosts(data);
            } else {
                console.error('Data is not an array:', data);
                alert('Expected an array of posts, but got something else.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error loading posts: ' + (error.error || error.message || 'Check console for details'));
        });
}

// Function to handle searching posts
function searchPosts() {
    var baseUrl = document.getElementById('api-base-url').value;
    var title = document.getElementById('search-title').value;
    var content = document.getElementById('search-content').value;
    var author = document.getElementById('search-author').value;
    var date = document.getElementById('search-date').value;

    var url = baseUrl + '/posts/search';
    var params = [];
    if (title) params.push('title=' + encodeURIComponent(title));
    if (content) params.push('content=' + encodeURIComponent(content));
    if (author) params.push('author=' + encodeURIComponent(author));
    if (date) params.push('date=' + encodeURIComponent(date));

    if (params.length > 0) {
        url += '?' + params.join('&');
    }

    fetch(url)
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw err; });
            }
            return response.json();
        })
        .then(data => {
            if (Array.isArray(data)) {
                displayPosts(data);
            } else {
                console.error('Data is not an array:', data);
                alert('Expected an array of posts, but got something else.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error searching posts: ' + (error.error || error.message || 'Check console for details'));
        });
}

// Helper function to display posts in the container
function displayPosts(data) {
    // Clear out the post container first
    const postContainer = document.getElementById('post-container');
    postContainer.innerHTML = '';

    // For each post in the response, create a new post element and add it to the page
    data.forEach(post => {
        const postDiv = document.createElement('div');
        postDiv.className = 'post';
        postDiv.innerHTML = `
            <h2>${post.title}</h2>
            <p>${post.content}</p>
            <div class="meta">By ${post.author} on ${post.date}</div>
            <button onclick="deletePost(${post.id})">Delete</button>
        `;
        postContainer.appendChild(postDiv);
    });
}

// Function to send a POST request to the API to add a new post
function addPost() {
    // Retrieve the values from the input fields
    var baseUrl = document.getElementById('api-base-url').value;
    var postTitle = document.getElementById('post-title').value;
    var postContent = document.getElementById('post-content').value;
    var postAuthor = document.getElementById('post-author').value;
    var postDate = document.getElementById('post-date').value;

    // Use the Fetch API to send a POST request to the /posts endpoint
    fetch(baseUrl + '/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            title: postTitle, 
            content: postContent,
            author: postAuthor,
            date: postDate
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw err; });
        }
        return response.json();
    })
    .then(post => {
        console.log('Post added:', post);
        // Clear input fields
        document.getElementById('post-title').value = '';
        document.getElementById('post-content').value = '';
        document.getElementById('post-author').value = '';
        document.getElementById('post-date').value = '';
        loadPosts(); // Reload the posts after adding a new one
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error adding post: ' + (error.error || error.message || 'Unknown error'));
    });
}

// Function to send a DELETE request to the API to delete a post
function deletePost(postId) {
    var baseUrl = document.getElementById('api-base-url').value;

    // Use the Fetch API to send a DELETE request to the specific post's endpoint
    fetch(baseUrl + '/posts/' + postId, {
        method: 'DELETE'
    })
    .then(response => {
        console.log('Post deleted:', postId);
        loadPosts(); // Reload the posts after deleting one
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error deleting post: ' + (error.error || error.message || 'Check console for details'));
    });
}
