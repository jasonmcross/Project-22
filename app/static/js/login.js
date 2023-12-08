const adminLogin = document.getElementById("submit-login");
const goBack = document.getElementById("go-back");

adminLogin.addEventListener("click", loginScript);
goBack.addEventListener("click", goBackScript);

function loginScript(event) {
    const user = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    window.location.href = "/adminhome";
}
function goBackScript(event) {
    window.location.href = "/";
}
