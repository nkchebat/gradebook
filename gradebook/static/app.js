// Retrieve all the elements from the add page and store in elements array
var elements = [];
for (var i = 1; i < 17; i++) {
    elements.push(document.getElementById(i.toString()));
}

// When add button is clicked reveal the next two in the array; set alert when they try to hit past 9
var iterations = 0;
var alert = document.getElementById("alert");
document.getElementById("add").addEventListener('click', function(e){
    // If they try to add more than 9 set alert
    if (iterations > 15) {
        alert.innerHTML = "You may not add more than 9 categories";
        alert_container.style.display = 'block';
    }
    // This ensures the alert for remove (if they attempted to remove past 1) will go away if they click add
    else {
        alert_container.style.display = 'none';
    }
    // Reveal the next two elements in the array for a new category
    for (var i = 0; i < 2; i++) {
        elements[i + iterations].style.display = 'block';
    }
    iterations += 2
});

// When remove button is clicked remove the previous 2; set alert when they try to go less than 1
document.getElementById("remove").addEventListener('click', function(e){
    // If they try to remove the first category, set alert
    if (iterations < 2) {
        alert.innerHTML = "You must have at least 1 category";
        alert_container.style.display = 'block';
    }
    // This ensures the alert for add (if they attempted to add past 9) will go away if they click remove
    else {
        alert_container.style.display = 'none';
    }
    // Remove the last two elements displayed for a category
    for (var i = 1; i < 3; i++) {
        elements[iterations - i].value = '';
        elements[iterations - i].style.display = 'none';
    }
    iterations -= 2
});

// When they close the alert, make it go away
document.getElementById("alert_close").addEventListener('click', function(e){
    alert_container.style.display = 'none';
});