const submitDesignProblem = document.getElementById("design-problem-form");
const goToLogin = document.getElementById("admin-login");

submitDesignProblem.addEventListener("submit", submitDesignProblemScript);
goToLogin.addEventListener("click", goToLoginScript);

function submitDesignProblemScript(event) {
    const problem = document.getElementById("design-problem").value;
    var collection = document.getElementById("collection-select").value;
    var source = document.getElementById("library-select").value;

    // 0 indicates that no collection was selected
    if (collection <= 0) {
        return;
    }
    else {

    }
    // Below shows how to output to the pattern list
    const word = "Test";

    document.getElementById('pattern-list').innerHTML += ('<li>' + word + '</li>');
}
function goToLoginScript(event) {
    // Put admin login page URL here
    window.location.replace("");
}