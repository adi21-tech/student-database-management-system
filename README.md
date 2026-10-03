# Student Database Management System

A web app I built with Flask and SQLite to manage student records. You log in, and then you can add, search, update and delete students.

## What it does
- Login page so only authorized users can get in
- Add, update and delete student records
- Search students by name, roll number, year or marks
- Filter students by branch
- Sort the list by name, roll number, year or marks
- Uses parameterized queries to keep the database safe from SQL injection

## Built with
Python, Flask, SQLite, HTML

## Files
- `app.py` is the main Flask app
- `students.db` is the SQLite database
- `templates/` has the HTML pages

## Run it yourself
```
pip install flask
python app.py
```
Then open `http://127.0.0.1:5000` in your browser.

## What I learned
How a Flask app connects to a database, how login works, and why parameterized queries matter for security.

## Next steps
- Hash passwords for login
- Export student records to a file
- Better page design

Made by Adithyatejas B Tejas
