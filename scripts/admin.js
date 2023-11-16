const addLibrary = document.getElementById("add-library");
const deleteLibrary = document.getElementById("delete-library");
const updateList = document.getElementById("update-library-list");
const logOut = document.getElementById("admin-logout");

addLibrary.addEventListener("submit", addLibraryScript);
deleteLibrary.addEventListener("submit", deleteLibraryScript);
updateList.addEventListener("click", updateListScript);
logOut.addEventListener("click", logOutScript);

function addLibraryScript(event) {
    const selection = document.getElementById("library-select");

    var choice = selection.value;
    var source;

    // 0 indicates that no option was selected
    if (choice == 0) {
        return;
    }
    else if (choice == 1) {
        source = StackOverflow
        // Run webcrawler and get json result
    }
    else if (choice == 2) {
        source = GangofFour
        // Run webcrawler and get json result
    }
    // Send json result to machine learning to get formatted design patterns

    // Send formatted results to database with source and collection
}
function deleteLibraryScript(event) {
    const input = document.getElementById("library-source");

    var source = input.value;

    // Ignore if no info is entered
    if (source == "Library Name" || source == null) {
        return;
    }
    else {
        // Send request to database to remove design patterns with selected source
    }
}
function updateListScript(event) {
    // Send request to database for all design patterns stored
    // Send each design pattern to list with id = library-list
}
function logOutScript(event) {
    // Put developer home page URL here
    window.location.replace("");
}
