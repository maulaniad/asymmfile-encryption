document.addEventListener("DOMContentLoaded", function () {
    // Temukan elemen dengan ID 'message'
    var messageElement = document.getElementById('message');

    // Periksa apakah parameter login_status ada dalam URL dan bernilai WRONG_PASSWORD
    var urlParams = new URLSearchParams(window.location.search);
    var loginStatus = urlParams.get('login_status');

    if (loginStatus === "WRONG_PASSWORD") {
        // Set teks pada elemen
        messageElement.textContent = "Wrong password. Please try again.";
    }
    setTimeout(function () {
        messageElement.style.display = 'none';
    }, 3000); // 3000 milidetik (3 detik)
});