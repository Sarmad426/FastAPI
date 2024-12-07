const API_URL = "http://127.0.0.1:8000";

// Fetch and display tweets
document.addEventListener("DOMContentLoaded", async () => {
    const tweetsContainer = document.getElementById("tweets");
    if (tweetsContainer) {
        try {
            const response = await fetch(`${API_URL}/tweets/`);
            const tweets = await response.json();

            tweets.forEach(tweet => {
                const tweetDiv = document.createElement("div");
                tweetDiv.className = "tweet";

                tweetDiv.innerHTML = `
          <p>${tweet.text}</p>
          ${tweet.image_filename
                        ? `<img src="${API_URL}${tweet.image_filename}" alt="Tweet Image" class='post-img'>`
                        : ""
                    }
        `;
                tweetsContainer.appendChild(tweetDiv);
            });
        } catch (error) {
            console.error("Error fetching tweets:", error);
        }
    }
});

// Handle form submission
const tweetForm = document.getElementById("tweet-form");
if (tweetForm) {
    tweetForm.addEventListener("submit", async event => {
        event.preventDefault();

        const formData = new FormData(tweetForm);
        try {
            const response = await fetch(`${API_URL}/tweets/`, {
                method: "POST",
                body: formData,
            });
            if (response.ok) {
                alert("Tweet posted successfully!");
                window.location.href = "index.html";
            } else {
                alert("Failed to post tweet.");
            }
        } catch (error) {
            console.error("Error posting tweet:", error);
        }
    });
}
