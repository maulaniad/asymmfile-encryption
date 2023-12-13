const formHandle = document.getElementById('form');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const verifyPasswordInput = document.getElementById('verify-password');
const errorMessageElement = document.getElementById('message');

function handlePasswordChange() {
    const password = passwordInput.value;
    const verifyPassword = verifyPasswordInput.value;

    if (password !== verifyPassword) {
        errorMessageElement.classList.add('text-red-500');
        errorMessageElement.textContent = 'Passwords not match';
    } else {
        errorMessageElement.classList.remove('text-red-500');
        errorMessageElement.textContent = '';
    }
}

function handleSubmit(event) {
    event.preventDefault();
    const password = passwordInput.value;
    const verifyPassword = verifyPasswordInput.value;

    if (password !== verifyPassword) {
        alert("Passwords do not match. Please check again.");
    } else {
        formHandle.submit();
    }
}

function emailCheck() {
    const email = emailInput.value;

    $.ajax({
        url: '/validate_email/',
        type: 'POST',
        data: { 'email': email },
        dataType: 'json',
        success: function (data) {
            $(emailInput).removeClass('text-red-500 text-green-500')
                .addClass(data.status === true ? 'text-red-500' : 'text-green-500');
        },
        error: function (xhr, errmsg, err) {
            console.log("Status: " + xhr.status);
        }
    });
}

verifyPasswordInput.addEventListener('input', handlePasswordChange);
passwordInput.addEventListener('input', handlePasswordChange);
formHandle.addEventListener('submit', handleSubmit);
// emailInput.addEventListener('input', emailCheck);
