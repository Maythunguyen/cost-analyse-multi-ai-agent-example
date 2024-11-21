### Prerequisites

Ensure you have the following software installed:

- **Python**: Version 3.7 or higher.
- **pip**: Python package manager.
- **Virtual Environment**: Recommended to isolate the project's dependencies.

2. **Create a Virtual Environment**
    python3 -m venv venv
3. **Activate the virtual environment:**
    On macOS and Linux: source venv/bin/activate
    On Windows: venv\Scripts\activate

## Install Dependencies
    pip install -r requirements.txt
## Set Up Environment Variables
    touch .env

## Start the Application
   uvicorn main:app --reload

   


