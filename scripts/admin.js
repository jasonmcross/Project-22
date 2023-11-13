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

    // 0 indicates that no option was selected
    if (choice == 0) {
        return;
    }
    else {
        
    }
}
function deleteLibraryScript(event) {
    const input = document.getElementById("library-id");

    var id = input.value;

    // Ignore invalid ID values
    if (id <= 0) {
        return;
    }
    else {
        
    }
}
function updateListScript(event) {
    // Below shows how to output to the library list
    const word = "Test";

    document.getElementById('library-list').innerHTML += ('<li>' + word + '</li>');
}
function logOutScript(event) {
    // Put developer home page URL here
    window.location.replace("");
}