document.addEventListener("DOMContentLoaded", function () {
    var messageElement = document.getElementById('error');

    var urlParams = new URLSearchParams(window.location.search);
    var loginStatus = urlParams.get('login_status');
    var registrationStatus = urlParams.get('register_status');

    if (loginStatus === "WRONG_PASSWORD") {
        messageElement.textContent = "Wrong password. Please try again.";
    } else if (loginStatus === "BAD") {
        messageElement.textContent = "Either it's server's fault or you entered a dirty data. Please try again.";
    } else if (loginStatus === "USER_DOES_NOT_EXIST") {
        messageElement.textContent = "The User you entered, is not registered in the database.";
    } else if (registrationStatus == "BAD") {
        messageElement.textContent = "Registration failed. Please fill the data properly and try again.";
    } else if (registrationStatus == "OK") {
        messageElement.classList.add("text-green-500")
        messageElement.textContent = "Registration successful. Please login with your credentials.";
    }
    setTimeout(() => {
        messageElement.textContent = '';
    }, 5000); // 5000 milidetik (5 detik)
});
