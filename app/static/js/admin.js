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
    fetch('/list', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then(response => response.json())
        .then(data => {
            let resultList = document.getElementById('library-list'); // Get the existing <ul> element
            resultList.innerHTML = ''; // Clear existing content

            data.forEach(item => {
                // item[0] is the digital library source, item[1] is the last updated date
                // \xa0 spaces out the text
                let listItem = `<li>Digital Library Source: ${item[0]} \xa0\xa0\xa0\xa0 Last Updated: ${item[1].toFixed(2)}</li>`; // Create list item
                resultList.innerHTML += listItem; // Append list item to <ul>
            });
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}
function logOutScript(event) {
    window.location.href = "/adminlogin";
}
