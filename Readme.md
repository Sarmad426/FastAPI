# Fast API

FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. It is designed for quick development with an emphasis on both performance and ease of use, making it ideal for building APIs, particularly those that are data-driven. FastAPI is built on top of Starlette for the web parts and Pydantic for data validation, which allows it to provide high speed and powerful data handling.

**What Makes FastAPI stand out:**

What makes FastAPI stand out is its automatic generation of OpenAPI and JSON Schema documentation, making it easy for developers to create and maintain clear, interactive API documentation. It also offers built-in support for asynchronous programming, enabling the development of highly concurrent systems. FastAPI's focus on type hints improves code quality and editor support, while its performance is comparable to frameworks like Node.js, making it one of the fastest Python web frameworks available.

**Suitable for AI:**

FastAPI is particularly well-suited for AI development due to its support for asynchronous programming, which is vital for handling multiple requests concurrently, especially in AI-driven applications that demand high performance and low latency. Its strong typing and validation features also help ensure the integrity of data passing through APIs, which is critical in AI models where data quality significantly impacts outcomes.

1. **Microsoft** - Utilizes FastAPI in various internal projects, particularly for building APIs in machine learning and AI services.

2. **Uber** - Uses FastAPI for some of its backend systems, particularly those requiring high performance and reliability.

3. **Netflix** - Employs FastAPI for managing some of its internal APIs, benefiting from its speed and automatic documentation.

4. **OpenAI** - Leverages FastAPI for building efficient and scalable API services, crucial for deploying AI models that require quick response times and handling high loads.

## Poetry

Poetry is a Python dependency management and packaging tool that simplifies project setup by managing dependencies, virtual environments, and package publishing all in one tool. It creates a `pyproject.toml` file to manage dependencies, allowing for precise version control and reducing conflicts.

**Better than `Anaconda`**

Unlike Anaconda, which is a broader platform for data science with a focus on managing environments and packages across various languages, Poetry is lightweight, Python-specific, and more focused on application development rather than data science workflows. Poetry's simplicity and tight integration with the Python ecosystem make it a better choice for developers who need streamlined, efficient dependency management and virtual environments, without the additional overhead of Anaconda’s broader tooling.

## Setting up a FastAPI Project with Poetry

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
poetry add fastapi "uvicorn[standard]"
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

## Step 13: Open the URLs

Open the following URLs in your browser:

- <http://127.0.0.1:8000>
