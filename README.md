# Item Catalog
### Udacity Full Stack Nanodegree Project

This project will display a list of items stored in a SQLite database. Google authenticated users have the ability to create, edit, and delete any items they add to the catalog.

To get the project running, follow these steps:

## Step 1.)
Install `pypugjs` using `pip`: `pip install pypugjs`
Note: This is the only dependency that should not already be installed on the Udacity supplied Vagrant VM.

## Step 2.)
Populate the database by navigating to `/db` in a terminal and running `python db_setup.py`.

## Step 3.)
Navigate back to the project root folder and run the webserver: `python main.py`

## Step 4.)
Open a browser and navigate to `http://localhost:8080`

You should now have the application up and running. The functionality of the app should be pretty straightforward. You can login with your Google account and add, delete, and edit items as you please.