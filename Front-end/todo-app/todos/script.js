document.addEventListener("DOMContentLoaded", () => {
  const todoContainer = document.getElementById("todo-container");

  // Fetch todos and display them
  fetch("http://127.0.0.1:8000")
    .then((response) => response.json())
    .then((todos) => {
      todos.forEach((todo) => {
        const todoItem = document.createElement("div");
        todoItem.className = `todo-item ${todo.completed ? "completed" : ""}`;
        todoItem.dataset.id = todo.id;

        const todoTitle = document.createElement("span");
        todoTitle.className = "todo-title";
        todoTitle.textContent = todo.title;

        const todoActions = document.createElement("div");
        todoActions.className = "todo-actions";

        const editButton = document.createElement("button");
        editButton.innerHTML = "&#9998;"; // Edit icon (✎)
        editButton.addEventListener("click", () => openEditModal(todo));

        const deleteButton = document.createElement("button");
        deleteButton.innerHTML = "&#128465;"; // Delete icon (🗑️)
        deleteButton.addEventListener("click", () => openDeleteModal(todo.id));

        todoActions.appendChild(editButton);
        todoActions.appendChild(deleteButton);

        todoItem.appendChild(todoTitle);
        todoItem.appendChild(todoActions);

        todoContainer.appendChild(todoItem);
      });
    })
    .catch((error) => console.error("Error fetching todos:", error));

  // Delete Modal Logic
  const deleteModal = document.getElementById("delete-modal");
  const deleteClose = document.getElementById("delete-close");
  const confirmDelete = document.getElementById("confirm-delete");
  const cancelDelete = document.getElementById("cancel-delete");
  let todoIdToDelete = null;

  function openDeleteModal(id) {
    todoIdToDelete = id;
    deleteModal.style.display = "block";
  }

  deleteClose.onclick = () => {
    deleteModal.style.display = "none";
  };

  cancelDelete.onclick = () => {
    deleteModal.style.display = "none";
  };

  confirmDelete.onclick = () => {
    fetch(`http://127.0.0.1:8000/delete/todo/${todoIdToDelete}`, {
      method: "DELETE",
    }).then((response) => {
      if (response.ok) {
        document
          .querySelector(`.todo-item[data-id='${todoIdToDelete}']`)
          .remove();
        deleteModal.style.display = "none";
      } else {
        console.error("Error deleting todo");
      }
    });
  };

  // Edit Modal Logic
  const editModal = document.getElementById("edit-modal");
  const editClose = document.getElementById("edit-close");
  const editForm = document.getElementById("edit-form");
  let todoIdToEdit = null;

  function openEditModal(todo) {
    todoIdToEdit = todo.id;
    editForm.title.value = todo.title;
    editForm.completed.value = todo.completed ? "true" : "false";
    editModal.style.display = "block";
  }

  editClose.onclick = () => {
    editModal.style.display = "none";
  };

  editForm.onsubmit = (e) => {
    e.preventDefault();
    const updatedTodo = {
      title: editForm.title.value,
      completed: editForm.completed.value === "true",
    };

    fetch(`http://127.0.0.1:8000/edit/todo/${todoIdToEdit}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updatedTodo),
    })
      .then((response) => response.json())
      .then((updatedTodo) => {
        const todoItem = document.querySelector(
          `.todo-item[data-id='${todoIdToEdit}']`
        );
        todoItem.querySelector(".todo-title").textContent = updatedTodo.title;
        todoItem.className = `todo-item ${
          updatedTodo.completed ? "completed" : ""
        }`;
        editModal.style.display = "none";
      })
      .catch((error) => console.error("Error updating todo:", error));
  };

  // Close modals when clicking outside
  window.onclick = (event) => {
    if (event.target === deleteModal) {
      deleteModal.style.display = "none";
    }
    if (event.target === editModal) {
      editModal.style.display = "none";
    }
  };
});
