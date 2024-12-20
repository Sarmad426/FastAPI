const API_URL = "http://127.0.0.1:8000";
const postsTableBody = document.querySelector("#posts-table tbody");

// Dialog Elements
const updateDialog = document.getElementById("update-dialog");
const deleteDialog = document.getElementById("delete-dialog");

// Update Form Elements
const updateForm = document.getElementById("update-form");
const updateText = document.getElementById("update-text");
const updateImage = document.getElementById("update-image");
let currentPostId = null;

// Delete Dialog Buttons
const cancelDeleteButton = document.getElementById("cancel-delete");
const confirmDeleteButton = document.getElementById("confirm-delete");

// Initialize Dashboard
document.addEventListener("DOMContentLoaded", loadPosts);

/**
 * Fetch and display all posts in the table.
 */
async function loadPosts() {
    postsTableBody.innerHTML = ""; // Clear existing posts
    try {
        const response = await fetch(`${API_URL}/tweets/`);
        const posts = await response.json();

        posts.forEach(post => renderPostInTable(post));
    } catch (error) {
        console.error("Error loading posts:", error);
    }
}

/**
 * Render a single post as a table row.
 * @param {Object} post - The post object.
 */
function renderPostInTable(post) {
    const row = document.createElement("tr");

    row.innerHTML = `
      
      <td title="${post.text}">${post.text}</td>
      <td>${post.image_filename ? `<img src="${API_URL}${post.image_filename}" alt="Post Image" class='post-img'>` : "No Image"}</td>
      <td>
        <button class="update-btn action-btn update"
        style='padding:8px;'
        onclick="openUpdateDialog(${post.id}, '${post.text}')">Update</button>
        <button class="action-btn delete"
        style='padding:8px;'
        onclick="openDeleteDialog(${post.id})">Delete</button>
      </td>
    `;

    postsTableBody.appendChild(row);
}

/**
 * Open the update dialog for a specific post.
 * @param {number} postId - The ID of the post to update.
 * @param {string} postText - The current text of the post.
 */
function openUpdateDialog(postId, postText) {
    currentPostId = postId;
    updateText.value = postText;
    updateDialog.classList.add("active"); // Show the dialog
}

/**
 * Close the update dialog.
 */
function closeUpdateDialog() {
    currentPostId = null;
    updateForm.reset(); // Clear the form
    updateDialog.classList.remove("active"); // Hide the dialog
}

// Attach event listener to the cancel button inside the update dialog
document.getElementById("cancel-update").addEventListener("click", closeUpdateDialog);

/**
 * Submit the updated post.
 */
updateForm.addEventListener("submit", async event => {
    event.preventDefault();

    if (!currentPostId) return;

    const formData = new FormData();
    formData.append("text", updateText.value);

    // Add image only if a file is selected
    if (updateImage.files[0]) {
        formData.append("image", updateImage.files[0]);
    }

    try {
        const response = await fetch(`${API_URL}/tweets/${currentPostId}/`, {
            method: "PUT",
            body: formData,
        });

        if (response.ok) {
            alert("Post updated successfully!");
            closeUpdateDialog();
            loadPosts(); // Reload posts to reflect changes
        } else {
            alert("Failed to update the post. Please try again.");
        }
    } catch (error) {
        console.error("Error updating post:", error);
    }
});

/**
 * Open the delete confirmation dialog for a specific post.
 * @param {number} postId - The ID of the post to delete.
 */
function openDeleteDialog(postId) {
    currentPostId = postId;
    deleteDialog.classList.add("active"); // Show the dialog
}

/**
 * Close the delete confirmation dialog.
 */
function closeDeleteDialog() {
    currentPostId = null;
    deleteDialog.classList.remove("active"); // Hide the dialog
}

// Cancel and confirm delete actions
cancelDeleteButton.addEventListener("click", closeDeleteDialog);
confirmDeleteButton.addEventListener("click", async () => {
    if (!currentPostId) return;

    try {
        const response = await fetch(`${API_URL}/tweets/${currentPostId}/`, {
            method: "DELETE",
        });

        if (response.ok) {
            alert("Post deleted successfully!");
            closeDeleteDialog();
            loadPosts();
        } else {
            alert("Failed to delete the post.");
        }
    } catch (error) {
        console.error("Error deleting post:", error);
    }
});
