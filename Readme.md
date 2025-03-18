# Fast API

FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. FastAPI is built on top of **Starlette** for the web parts and Pydantic for data validation, which allows it to provide high speed and powerful data handling.

**What Makes FastAPI stand out:**

What makes FastAPI stand out is its automatic generation of **OpenAPI** and **JSON** Schema documentation, making it easy for developers to create and maintain clear, interactive API documentation. It also offers built-in support for asynchronous programming, enabling the development of highly concurrent systems. FastAPI's focus on type hints improves code quality and editor support, while its performance is comparable to frameworks like *Node.js*, making it one of the fastest Python web frameworks available.

**Suitable for AI:**

FastAPI is particularly well-suited for AI development due to its support for asynchronous programming, which is vital for handling multiple requests concurrently, especially in AI-driven applications that demand high performance and low latency. Its strong typing and validation features also help ensure the integrity of data passing through APIs, which is critical in AI models where data quality significantly impacts outcomes.

## Setting up a FastAPI Project with Poetry

### Poetry

Poetry is a Python dependency management and packaging tool that simplifies project setup by managing dependencies, virtual environments, and package publishing all in one tool. It creates a `pyproject.toml` file to manage dependencies, allowing for precise version control and reducing conflicts.

## Step 1: Install pipx

- Open your terminal.
- Install pipx using pip:

```bash
python -m pip install --user pipx
```

## Step 2: Ensure pipx's binary directory is in your PATH

Run the following command to ensure pipx's binary directory is in your PATH:

```bash
python -m pipx ensurepath
```

## Step 3: Restart your terminal

Restart your terminal to apply the PATH update.

## Step 4: Install Poetry

Run the command:

```bash
pipx install poetry
```

## Step 5: Check the version of Poetry

To check the version, run:

```bash
poetry --version
```

## Step 6: Create a new project

Create a new project with Poetry:

```bash
poetry new poetry-class --name poetryclass
```

## Step 7: Navigate to the project folder

Open the subfolder inside the parent folder, in this case `poetryclass`.

## Step 8: Create a main.py file

Create a new file named `main.py`.

## Step 9 (Optional): Check the Python version

To check the version of Python, run:

```bash
poetry run python --version
```

## Step 10: Add FastAPI and Uvicorn

Run the command:

```bash
poetry add fastapi[standard] "uvicorn[standard]"
```

## Step 10a (Optional): Check packages in pyproject.toml

Optionally, check the packages inside the `pyproject.toml` file.

## Step 11: Write the hello world code in main.py

```python
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

## Step 12: Run the server

Run the server using Poetry:

```bash
poetry run uvicorn main:app --reload
```

OR

```bash
uvicorn main:app --reload
```

## Step 13: Open the URLs

Open the following URLs in your browser:

- <http://127.0.0.1:8000> to view the hello world message.
- <http://127.0.0.1:8000/docs> to view the interactive API documentation.

### Learning Roadmap

- Introduction to FastAPI
- Creating API Endpoints
- Path and Query Parameters
- Request and Response Models
- Dependency Injection
- Asynchronous Programming
- Middleware
- Security and Authentication
- Handling CORS (Cross-Origin Resource Sharing)
- Database Integration
- WebSockets
- Testing
- Deployment
- API Documentation
- Rate Limiting and Throttling
- Logging and Monitoring
- Graphql Integration
- Caching
- API Gateway integration
- Event driven architecture
- Error Handling and Validation

### Other Repositories

**Python**. <https://github.com/Sarmad426/Python>

**Python Projects**. <https://github.com/Sarmad426/Python-projects>

Learn **DSA** with python. <https://github.com/Sarmad426/DSA-Python>

Learn **AI** and **Data Science**. <https://github.com/Sarmad426/AI>

Learn **Generative AI**. <https://github.com/Sarmad426/Generative-AI>
