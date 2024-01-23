# Google Calendar Integration

## Overview

This project is a Python implementation of a calendar application using the Google Calendar API. It provides functionalities to authenticate with Google, create, delete, and retrieve events from the Google Calendar.

## Prerequisites

- Python 3.x installed.
- `pip` installed for package management.

## Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/your-repository.git
    ```

2. **Install required packages:**

    ```bash
    pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
    ```

3. **Configure Google API credentials:**

    - Go to the [Google Developer Console](https://console.developers.google.com/).
    - Create a new project.
    - Enable the Google Calendar API for the project.
    - Download the JSON credentials file and save it as `client_secret_google.json` in the project directory.

4. **Run the application:**

    ```bash
    python your_script.py
    ```

## Classes and Functions

### `GoogleAuthentification` Class

- `__init__(self, credentials_path="client_secret_google.json", token_path="token.json", SCOPE=["https://www.googleapis.com/auth/calendar"])`: Initializes the authentication object.
- `get_credentials(self)`: Initiates the OAuth 2.0 flow to obtain user credentials.

### `GoogleCalendar` Class

- `__init__(self, credentials)`: Initializes the Google Calendar object with the provided credentials.
- `build_services(self)`: Builds and returns the Google Calendar API service.
- `create_event(self, summary, start_time, end_time, location=None)`: Creates a new event on the Google Calendar.
- `delete_event(self, event_id)`: Deletes an event from the Google Calendar using its ID.
- `get_events(self)`: Retrieves upcoming events from the Google Calendar.


