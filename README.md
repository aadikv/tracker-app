# Tracker App

## Setup

1. Create a Firebase project and download the `firebase-adminsdk.json` file.
2. Create a database file named `expiration_tracker.db` in the root directory.
3. Run `python database_setup.py` to create the database.
4. Run `python app.py` to start the app.

## Usage

1. Upload an image of an item to the `/api/upload` endpoint.
2. The app will detect the expiration date and save it to the database.
3. The app will send a notification to the device token provided in the request.  The notification will be sent one week before the expiration date.  If the item is not found in the database, the app will return an error.  If the item is found, the app will return the expiration date.  The expiration date will be in the format `YYYY-MM-DD`.
