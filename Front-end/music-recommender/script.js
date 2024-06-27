document
  .getElementById("recommendation-form")
  .addEventListener("submit", async function (event) {
    event.preventDefault();

    const age = document.getElementById("age").value;
    const gender = document.getElementById("gender").value;

    const responseElement = document.getElementById("response");
    responseElement.style.display = "none";

    try {
      const response = await fetch("http://127.0.0.1:8000/recommend", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ age: age, gender: gender }),
      });

      const result = await response.json();
      console.log(result);
      responseElement.textContent = result;
      responseElement.style.display = "block";
    } catch (error) {
      responseElement.textContent = "An error occurred. Please try again.";
      responseElement.style.display = "block";
    }
  });
