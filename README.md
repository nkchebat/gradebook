GRADEBOOK


YOUTUBE LINK
https://youtu.be/c_Wh8iB6I7s


ACCESS INSTRUCTIONS

To access Gradebook, simply download all the submitted files from Gradescope and put them all in a folder named "gradebook". From there, create a folder named "templates" in the "gradebook" folder and put all files that end with ".html" in the "templates" folder. Then, create another folder named "static" within the "gradebook" folder and put the "styles.css" file, the "favicon.ico" file, the "bootstrap.min.css" file, and the "app.js" file in the "static" folder. Now your folder is all set up. Next, put the "gradebook" folder containing all the files for Gradebook in your codespace, perhaps by dragging and dropping it there. After the folder is in your codespace, use "cd" in the terminal to change directory and navigate to the "gradebook" folder containing the files for Gradebook. Once you have accessed the folder, the rightmost statement the terminal presents should be "gradebook/ $". You can now run the website by typing "flask run" into the terminal and hitting enter, which will provide a link in your terminal that will take you to the Gradebook website.


OVERVIEW

Gradebook is a website designed for users, specifically students, to keep track of their grades. There are 3 main components to Gradebook:

    GRADES
    CLASSES
    ASSIGNMENTS

Each component can be accessed following registration, which requires a first name, username, and password


NAVIGATION

The navigation bar found at the top of the screen after successful login has a logout option and each of the three components of the website as dropdown menus: grades, classes, and assignments. Under each you will find the following:

    GRADES: CURRENT GRADES, PAST GRADES
    CLASSES: ADD A CLASS, REMOVE A CLASS, ARCHIVE A CLASS
    ASSIGNMENTS: ADD AN ASSIGNMENT, REMOVE AN ASSIGNMENT, VIEW ASSIGNMENTS

Each of these navigation options is detailed below


GRADES

There are two components to grades: current grades and past grades

    CURRENT GRADES

    Current grades is the homepage of the website. It displays to the user a table with each of that user's current (unarchived) classes, as well as their current grade in the class as a percentage rounded to two decimal places. These grades are calculated assuming 100 percent in each category of a class that has no current assignments entered into it (an intentional choice explained in DESIGN.md). For instance, when a class has no assignments entered into it, it is considered to be 100%, as each category of the course has no assignments entered for it.

    PAST GRADES

    Past grades allows you to view courses you have archived. Archived courses are courses that you have completed and are now part of your transcript. You may see your final grade in the course as a percentage rounded to two decimal places, as well as the name of the course.


CLASSES

There are three components to classes: add a class, remove a class, and archive a class

    ADD A CLASS

    Add a class is where you will begin your journey with gradebook. Here you will enter the name and details of a course you are taking. Alongside the name, you will enter the categories of the course, with each category being the weighted components of the course. For instance, tests, quizzes, attendance, etc. will be weighted differently in most courses. Here you will specify what percentage of your grade is composed by each component, with the website allowing you to enter up to 9 components in a course. Of course, all percentages must be integers greater than 0 and the sun of all the components must be 100, as that would account for 100% of your grade. If you accidentally press the "add another category" button, you can remove the extra added category using the "remove last category" button.

    REMOVE A CLASS

    If you would like to remove a class from your gradebook, you can use the remove a class page. Here you will simply select the course you would like removed from a dropdown button and with the press of the "remove" button that course, all its assignments, and all details pertaining to the course will be completely removed from your gradebook.

    ARCHIVE A CLASS

    The archive a class page is used to place a current course in your past courses, presumably after completing a course so that you may still retain a history of your final grades in past courses. To archive a course, simply select the current course you would like to archive from the dropdown and then proceed to press the "archive" button. You will then be redirected to the past courses page, which will now include the course that you archived.


ASSIGNMENTS

There are three components to assignments: add an assignment, drop an assignment, and view assignments

    ADD AN ASSIGNMENT

    To add an assignment to your gradebook, simply navigate to the add an assignment page, which will first ask you to select the course you would like to add your assignment to. After selecting the course from the dropdown and submitting your selection, you will then be asked to enter the details of the assignment. Required are an assignment type, assignment name, points awarded, and points possible. To select an assignment type use the dropdown, which will have provided all the categories of the course you selected to add the assignment to. Then, you may enter in any assignment name but must make sure not to reuse the same assignment name for multiple assignments within the same course. Points awarded and points possible must be positive integers, and points awarded may exceed points possible to account for any extra credit the user may have earned.

    DROP AN ASSIGNMENT

    To drop an assignment from your gradebook, simply navigate to the drop an assignment page, which will first ask you to select the course you would like to drop your assignment from. After selecting the course from the dropdown and submitting your selection, you will then be given a dropdown to choose from all the assignments that you have entered for that course. After selecting the assignment you would like removed, simply press the "drop assignment" button and that assignment will be entirely removed from the selected course. Your grade will instantly be updated reflecting the drop in the assignment and you will no longer be able to view the assignment in the view assignments page.

    VIEW ASSIGNMENTS

    To view your assignments for a course, simply navigate to the view assignments page, which will first ask you to select the course you would like to view assignments for. After selecting the course from the dropdown and submitting your selection, you will then be provided a table that shows you the details of all assignments you have entered for the selected course. The table will show the assignment name, the category of the course it falls under (type), the points earned on the assignment, the points available on the assignment, and the score percentage earned on the assignment.