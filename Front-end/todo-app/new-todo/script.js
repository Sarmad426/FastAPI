document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("todo-form");
    const popup = document.getElementById("popup");

    form.onsubmit = (e) => {
        e.preventDefault();

        const title = document.getElementById("title").value;
        const completed = document.getElementById("completed").value === "true";

        const todo = {
            title,
            completed
        };

        fetch("http://127.0.0.1:8000/new/todo", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(todo)
        })
        .then(response => response.json())
        .then(data => {
            if (data.id) {
                showPopup("Todo added successfully!", false);
                form.reset();
            } else {
                throw new Error("Failed to add todo");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            showPopup("Error adding todo. Please try again.", true);
        });
    };

    function showPopup(message, isError) {
        popup.textContent = message;
        popup.className = isError ? "popup error" : "popup";
        popup.style.display = "block";
        setTimeout(() => {
            popup.style.display = "none";
        }, 3000);
    }
});
