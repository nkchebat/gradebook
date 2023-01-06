from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import grade, login_required, apology, check_class, check_positive_integer, recalculate

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["grade"] = grade

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///gradebook.db")


@app.route("/")
@login_required
def index():
    """Show Current Grades"""

    # Return home page with username and the names and grades of the user's current classes
    return render_template("index.html", name=db.execute("SELECT name FROM users WHERE id = ?;", session["user_id"])[0]["name"],
                           classes=db.execute("SELECT name, grade FROM classes WHERE user_id = ? AND current = 1;", session["user_id"]))


@app.route("/past")
@login_required
def past():
    """Show Past Grades"""

    # Return past grades page with the user's non-current classes
    return render_template("past.html", name=db.execute("SELECT name FROM users WHERE id = ?;", session["user_id"])[0]["name"],
                           classes=db.execute("SELECT name, grade FROM classes WHERE user_id = ? AND current = 0;", session["user_id"]))


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add A Class"""

    if request.method == "POST":

        # Retrieve all form entries; put categories into dictionary
        class_name = request.form.get("class_name")
        categories = {
            'category1_name': request.form.get("category1_name").strip(),
            'category1': request.form.get("category1"),
            'category2_name': request.form.get("category2_name").strip(),
            'category2': request.form.get("category2"),
            'category3_name': request.form.get("category3_name").strip(),
            'category3': request.form.get("category3"),
            'category4_name': request.form.get("category4_name").strip(),
            'category4': request.form.get("category4"),
            'category5_name': request.form.get("category5_name").strip(),
            'category5': request.form.get("category5"),
            'category6_name': request.form.get("category6_name").strip(),
            'category6': request.form.get("category6"),
            'category7_name': request.form.get("category7_name").strip(),
            'category7': request.form.get("category7"),
            'category8_name': request.form.get("category8_name").strip(),
            'category8': request.form.get("category8"),
            'category9_name': request.form.get("category9_name").strip(),
            'category9': request.form.get("category9")}

        # Ensure class name, category 1 name, and category 1 percentage are entered
        if not categories['category1'] or not categories['category1_name'] or not class_name:
            return apology("Class must be named and requires at least one category")

        # Ensure all categories are either empty (except category 1) or integers > 0 and add up to 100; if category empty, category_name must also be
        total = 0
        names = []
        end_of_entered = False
        for i in range(1, 10):

            # Get this iterations category and name from the dictionary
            key = 'category' + str(i)
            category = categories[key]
            category_name = categories[key + '_name']

            # If end_of_entered is true, ensure they did not enter in a category after leaving a previous category blank
            if end_of_entered == True:
                if category != "" or category_name != "":
                    return apology("Enter categories in order from top to bottom")
                else:
                    continue

            # If category unentered and name unentered (except for 1), continue; if name entered but category not, issue apology
            if i != 1:
                if category == "":
                    if category_name == "":
                        end_of_entered = True
                        continue
                    else:
                        return apology("Must enter a proper percentage for all named categories")

            # Ensure no two categories have the same name
            if category_name in names:
                return apology("Each Category Must Have A Unique Name")
            else:
                names.append(category_name)

            # Check if category is not a digit or not greater than 0
            if not check_positive_integer(category):
                return apology("Percentages must be positive integers")

            # If it passes all checks thus far add category to total
            total += int(category)

        # Ensure total equals 100
        if total != 100:
            return apology("Percentages must add up to 100")

        # Ensure they have not already used this name for a class
        if db.execute("SELECT id FROM classes WHERE user_id = ? AND name = ? AND current = 1;", session["user_id"], class_name):
            return apology("Class name already used")

        # Enter class into database with name and user association
        db.execute("INSERT INTO classes (user_id, name, grade, current) VALUES (?,?,100, 1);", session["user_id"], class_name)

        # Enter class info into database
        db.execute("INSERT INTO class_info (class_id, category1, category1_name, category2, category2_name, category3, \
            category3_name, category4, category4_name, category5, category5_name, category6, category6_name, category7, \
            category7_name, category8, category8_name, category9, category9_name) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",
                   db.execute("SELECT id FROM classes WHERE name = ? and user_id = ?;", class_name, session["user_id"])[0]["id"],
                   categories['category1'], categories['category1_name'], categories['category2'], categories['category2_name'],
                   categories['category3'], categories['category3_name'], categories['category4'], categories['category4_name'],
                   categories['category5'], categories['category5_name'], categories['category6'], categories['category6_name'],
                   categories['category7'], categories['category7_name'], categories['category8'], categories['category8_name'],
                   categories['category9'], categories['category9_name'])

        # Redirect to home page
        return redirect("/")

    else:
        return render_template("add.html")


@app.route("/remove", methods=["GET", "POST"])
@login_required
def remove():
    """Remove A Class"""

    if request.method == "POST":

        # Retrieve name of the class they want removed
        remove_class = request.form.get("remove_class")

        # Ensure a class was properly entered and found in database
        if not check_class(remove_class):
            return apology("Class Not Found")

        # After passing the check, get the class id and store in variable
        remove_class_id = db.execute("SELECT id FROM classes WHERE user_id = ? AND name = ?;",
                                     session["user_id"], remove_class)[0]["id"]

        # Drop the class_info, assignments, and class they requested for drop from the database
        db.execute("DELETE FROM class_info WHERE class_id = ?;", remove_class_id)
        db.execute("DELETE FROM assignments WHERE class_id = ?;", remove_class_id)
        db.execute("DELETE FROM classes WHERE name = ? AND user_id = ?;", remove_class, session["user_id"])

        # Redirect to home page
        return redirect("/")

    # Return remove page with user's current classes
    else:
        return render_template("remove.html", classes=db.execute("SELECT name FROM classes WHERE user_id = ? AND current = 1;", session["user_id"]))


@app.route("/archive", methods=["GET", "POST"])
@login_required
def archive():
    """Archive A Class"""

    if request.method == "POST":

        # Retrieve class the user wanted archived
        archive_class = request.form.get("archive_class")

        # Ensure a class was properly entered and found in database
        if not check_class(archive_class):
            return apology("Class Not Found")

        # Set the current value of the class they want to archive to 0
        db.execute("UPDATE classes SET current = 0 WHERE user_id = ? AND name = ?;", session["user_id"], archive_class)

        # Redirect to past classes page
        return redirect('/past')

    # Return archive page with user's current classes
    else:
        return render_template("archive.html", classes=db.execute("SELECT name FROM classes WHERE user_id = ? AND current = 1;", session["user_id"]))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?;", request.form.get("username").strip())

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register the user"""

    if request.method == "POST":

        # Retrieve name, username, password, and retype
        name = request.form.get("register_name").strip()
        username = request.form.get("register_username").strip()
        password = request.form.get("register_password")
        retype = request.form.get("register_retype")

        # Ensure they have entered a name, username, and password, and the password is equal to the retype
        if name and username and password and retype == password:

            # Ensure username not already taken
            if db.execute("SELECT id FROM users WHERE username = ?;", username):
                return apology("Username taken")

            # Enter the user into the database with their password hash
            db.execute("INSERT INTO users (name, username, password) VALUES (?,?,?);",
                       name, username, generate_password_hash(password))

            # Redirect to login page
            return redirect("/login")

        # User left field blank or password does not equal retype
        else:
            return apology("Fill out all fields and ensure password and retyped password are the same")

    else:
        return render_template("register.html")


@app.route("/assignment", methods=["GET", "POST"])
@login_required
def assignment():
    """Choose A Class To Add Assignment"""

    if request.method == "POST":

        # Retrieve name of the class they want to add an assignment to
        assignment_class = request.form.get("assignment_class")

        # Ensure a class was properly entered and found in database
        if not check_class(assignment_class):
            return apology("Class Not Found")

        # After passing the check, get the class id and store in variable
        chosen_class = db.execute("SELECT id FROM classes WHERE user_id = ? AND name = ?;",
                                  session["user_id"], assignment_class)[0]["id"]

        # Return page with categories of chosen class in a dropdown
        return render_template("assignmented.html", chosen_class=chosen_class, assignment_class=assignment_class,
                               categories=db.execute("SELECT * FROM class_info WHERE class_id = ?;", chosen_class)[0])

    # Return assignment page with user's current classes
    else:
        return render_template("assignment.html", classes=db.execute("SELECT name FROM classes WHERE user_id = ? AND current = 1;", session["user_id"]))


@app.route("/assignmented", methods=["POST"])
@login_required
def assignmented():
    """Add An Assignment"""

    # Retrieve all info submitted through form
    class_id = request.form.get("chosen_class")
    assignment_type = request.form.get("assignment_type")
    assignment_name = request.form.get("assignment_name").strip()
    score_numerator = request.form.get("score_numerator")
    score_denominator = request.form.get("score_denominator")

    # Get categories for this class from the database
    categories = db.execute("SELECT * FROM class_info WHERE class_id = ?;", class_id)[0]

    # Ensure assignment name entered and hasn't been used for a previous assignment in this class
    if not assignment_name:
        return apology("Assignment Name Missing")
    elif db.execute("SELECT * FROM assignments WHERE class_id = ? and name = ?", class_id, assignment_name):
        return apology("Assignment Name Already Used For This Class")

    # Ensure score numerator is float or int >= 0
    numerator_check = score_numerator.replace('.','',1)
    if not numerator_check.isdigit() or not int(numerator_check) >= 0:
        return apology("Numerator must be number greater than or equal to 0")

    # Ensure score denominator is float or int > 0
    if not check_positive_integer(score_denominator.replace('.','',1)):
        return apology("Denominator must be positive number")

    # Ensure assignment type entered and exists in database for this class
    if not assignment_type or assignment_type not in categories.values():
        return apology("Assignment Type Not Found")

    # Add assignment to the database
    db.execute("INSERT INTO assignments(class_id, name, type, score_numerator, score_denominator) VALUES (?,?,?,?,?)",
               class_id, assignment_name, assignment_type, score_numerator, score_denominator)

    # Recalculate and update grade
    recalculate(class_id, categories)

    # Redirect to home page
    return redirect("/")


@app.route("/view", methods=["GET", "POST"])
@login_required
def view():
    """View Class Assignments"""

    if request.method == "POST":

        # Retrieve class name
        view_name = request.form.get("view_class")

        # Ensure a class was properly entered and found in database
        if not check_class(view_name):
            return apology("Class Not Found")

        # Return viewed page for selected class with assignments
        return render_template("viewed.html", name=view_name,
                               assignments=db.execute("SELECT name, type, score_numerator, score_denominator FROM assignments WHERE \
                                        class_id = (SELECT id FROM classes WHERE name = ? AND user_id = ?);", view_name, session["user_id"]))

    # Return view page with user's current classes
    else:
        return render_template("view.html", classes=db.execute("SELECT name FROM classes WHERE user_id = ? AND current = 1;", session["user_id"]))


@app.route("/drop", methods=["GET", "POST"])
@login_required
def drop():
    """Choose A Class To Drop An Assignment From"""

    if request.method == "POST":

        # Retrieve name of the class they want to add an assignment to
        drop_class = request.form.get("drop_class")

        # Ensure a class was properly entered and found in database
        if not check_class(drop_class):
            return apology("Class Not Found")

        # After passing the check, get the class id and store in variable
        selected_class = db.execute("SELECT id FROM classes WHERE user_id = ? AND name = ?;",
                                    session["user_id"], drop_class)[0]["id"]

        # Return page with assignments of chosen class in a dropdown
        return render_template("dropped.html", selected_class=selected_class, drop_class=drop_class,
                               assignments=db.execute("SELECT name FROM assignments WHERE class_id = ?;", selected_class))

    # Return assignment page with user's current classes
    else:
        return render_template("drop.html", classes=db.execute("SELECT name FROM classes WHERE user_id = ? AND current = 1;", session["user_id"]))


@app.route("/dropped", methods=["POST"])
@login_required
def dropped():
    """Drop An Assignment"""

    # Retrieve all info submitted through form
    class_id = request.form.get("selected_class")
    assignment = request.form.get("assignment")

    # Ensure assignment entered and found in database
    if not assignment or not db.execute("SELECT id FROM assignments WHERE class_id = ? AND name = ?", class_id, assignment):
        return apology("Assignment Not Found")

    # Remove assignment from the database
    db.execute("DELETE FROM assignments WHERE class_id = ? AND name = ?", class_id, assignment)

    # Recalculate and update grade
    recalculate(class_id, db.execute("SELECT * FROM class_info WHERE class_id = ?;", class_id)[0])

    # Redirect to home page
    return redirect("/")