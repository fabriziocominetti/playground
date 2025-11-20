# English Premier League Results Analysis

This project is a simple Python application designed to load and process English Premier League match results. It serves as a learning exercise for setting up a modern Python project environment using `uv`, `pytest`, and `ruff`.

## Project Structure

The project follows the standard `src` layout to separate the main application code from other development files like tests and configuration.

```
py_epl_results/
├── .venv/
├── data/
│   └── results.csv
├── src/
│   └── py_epl_results/
│       ├── __init__.py
│       └── main.py
├── tests/
│   └── test_main.py
├── pyproject.toml
└── README.md
```

## Setup and Installation

Follow these steps to set up the project locally. This project uses `uv` for fast dependency and environment management.

1.  **Clone the Repository**
    ```sh
    git clone <your-repository-url>
    cd py_epl_results
    ```

2.  **Install `uv`**
    If you don't have `uv` installed, you can install it via `pip`:
    ```sh
    pip install uv
    ```

3.  **Create and Activate Virtual Environment**
    Setup `uv`
    ```sh
    uv init py_epl_results
    ```
    Activate the virtual environment. On macOS/Linux:
    ```sh
    source .venv/bin/activate
    ```
    Add necessary dependencies:
    ```sh
    uv add pandas pytest ruff ...
    ```

## Usage

The main script loads the dataset from the `data` directory and prints the first few rows to the console.

To run the script, execute the following command from the project root directory:
```sh
python src/py_epl_results/main.py
```

## Running Tests

This project uses `pytest` for unit testing. The tests ensure that the core functionality, such as data loading, works as expected.

To run the test suite, make sure your virtual environment is active and run the following command from the project root:
```sh
pytest
```

## Code Quality

Code quality is maintained using `ruff`, an extremely fast Python linter and formatter.

*   **Check for issues:**
    ```sh
    ruff check .
    ```

*   **Automatically fix issues:**
    ```sh
    ruff check . --fix
    ```

*   **Format the code:**
    ```sh
    ruff format .
    ```