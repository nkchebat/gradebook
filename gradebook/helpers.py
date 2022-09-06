import os
import requests
import urllib.parse

from cs50 import SQL
from flask import redirect, render_template, request, session
from functools import wraps

db = SQL("sqlite:///gradebook.db")


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def grade(value):
    """Format value as grade"""
    return f"{value:,.2f}%"


def check_class(input):
    """Check a class input was entered and found in database"""

    # If input is none or empty return False; Or if class not found in database return False
    if input is None or not input or not db.execute("SELECT * FROM classes WHERE user_id = ? AND name = ?", session["user_id"], input):
        return False

    # If it passes the check, return True
    return True


def check_positive_integer(input):
    """Check if a string is a positive integer"""

    # If input is not a digit or its value is not greater than 0 return False
    if not input.isdigit() or not int(input) > 0:
        return False

    # If it passes the check, return True
    return True


def recalculate(class_id, categories):
    """Recalculate and update grade"""

    grade = 0
    for i in range(1, 10):

        # Get key and category name for this iteration
        key = "category" + str(i)
        category_name = categories[key + "_name"]

        # Iterate through each category until we reach one that they did not input into
        if category_name == "":
            break

        # Get the weight of the category
        weight = categories[key] / 100

        # Get the sum of all the points earned and points possible in this category
        scores = db.execute("SELECT SUM(score_numerator), SUM(score_denominator) FROM assignments WHERE class_id = ? AND type = ?",
                            class_id, category_name)[0]

        # If there are no assignments of that type, give that type 100 percent and continue
        if scores["SUM(score_numerator)"] is None:
            grade += weight
            continue

        # Multiply the weight by the points earned / points possible; add it to the overall grade
        grade += weight * (scores["SUM(score_numerator)"]/scores["SUM(score_denominator)"])

    # Update grade in database
    db.execute("UPDATE classes SET grade = ? WHERE id = ?;", grade * 100, class_id)

    return 0