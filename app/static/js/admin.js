const updateLibrary = document.getElementById("update-library");
const deleteLibrary = document.getElementById("delete-library");
const updateList = document.getElementById("update-library-list");
const logOut = document.getElementById("admin-logout");

updateLibrary.addEventListener("click", updateLibraryScript);
deleteLibrary.addEventListener("click", deleteLibraryScript);
updateList.addEventListener("click", updateListScript);
logOut.addEventListener("click", logOutScript);

function updateLibraryScript(event) {
    const selection = document.getElementById("library-select");

    var choice = selection.value;

    // 0 indicates that no option was selected
    if (choice == 0) {
        return;
    }
    else {
        fetch('/updateLibrary', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',

            },
            body: JSON.stringify({ description: choice }),
        })
            .then(response => response.json())
    }
}
function deleteLibraryScript(event) {
    const input = document.getElementById("library-source");

    var source = input.value;

    // Ignore if no info is entered
    if (source == "Library Name" || source == null) {
        return;
    }
    else {
        
    }
}
function updateListScript(event) {
    fetch('/get-sources')
    .then(response => response.json())
    .then(files => {
        const dropdown = document.getElementById('library-list');
        files.forEach(file => {
            const fileNameWithoutExtension = file.replace(/\.[^/.]+$/, "");
             const option = fileNameWithoutExtension;
             dropdown.innerHTML += `<li>Digital Library Source: ${option} \xa0\xa0\xa0\xa0</li>`
        });
    })
    .catch(error => console.error('Error:', error));
}
function logOutScript(event) {
    window.location.href = "/adminlogin";
}
