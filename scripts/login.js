const adminLogin = document.getElementById("submit-login");
const goBack = document.getElementById("go-back");

adminLogin.addEventListener("click", loginScript);
goBack.addEventListener("click", goBackScript);

function loginScript(event) {
    const user = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    window.location.replace("../newpages/admin-home.html");
}
function goBackScript(event) {
    window.location.replace("../newpages/developer-home.html");
}
