const submitDesignProblem = document.getElementById("design-problem-form");
const goToLogin = document.getElementById("admin-login");

submitDesignProblem.addEventListener("submit", submitDesignProblemScript);
goToLogin.addEventListener("click", goToLoginScript);

function submitDesignProblemScript(event) {
    event.preventDefault();
    const problem = document.getElementById("design-problem").value;
    var collection = document.getElementById("collection-select").value;
    var source = document.getElementById("library-select").value;

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ description: problem }),
    })
        .then(response => response.json())
        .then(data => {
            let resultList = document.getElementById('pattern-list'); // Get the existing <ul> element
    resultList.innerHTML = ''; // Clear existing content

    data.forEach(item => {
        // item[0] is the pattern name, item[1] is the probability
        // \xa0 spaces out the text
       let listItem = `<li>Design Problem: ${item[0]} \xa0\xa0\xa0\xa0 Cosine Similarity Score: ${item[1].toFixed(2)}</li>`; // Create list item
        resultList.innerHTML += listItem; // Append list item to <ul>
    });
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}
function goToLoginScript(event) {
    window.location.replace("../newpages/admin-login.html");
}
