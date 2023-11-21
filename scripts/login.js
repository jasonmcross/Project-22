const adminLogin = document.getElementById("login-form");
const goBack = document.getElementById("go-back");

adminLogin.addEventListener("submit", loginScript);
goBack.addEventListener("click", goBackScript);

function loginScript(event) {
    const user = document.getElementById("username").value;
    const password = document.getElementById("password").value;


}
function goBackScript(event) {
    // Put developer home page URL here
    window.location.replace("");
}