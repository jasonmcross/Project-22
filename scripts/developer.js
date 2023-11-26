const submitDesignProblem = document.getElementById("problem-form");
const goToLogin = document.getElementById("admin-login");

submitDesignProblem.addEventListener("click", submitDesignProblemScript);
goToLogin.addEventListener("click", goToLoginScript);

function submitDesignProblemScript() {
    const problem = document.getElementById("design-problem").value;
    var collection = document.getElementById("collection-select").value;
    var source = document.getElementById("library-select").value;

    fetch('/mediator', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ description: problem }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerText = JSON.stringify(data, null, 2);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
function goToLoginScript(event) {
    window.location.replace("../newpages/admin-login.html");
}
