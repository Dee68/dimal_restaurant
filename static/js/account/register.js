const usernameField = document.querySelector('#usernameField');
const feedbackArea = document.querySelector(".invalid-feedback");
const usernameSuccess = document.querySelector(".usernameSuccess");

const registerForm = document.querySelector("#regform");
const emailField = document.querySelector('#emailField');
const emailFeedBack = document.querySelector('.emailFeedback');
const emailSuccess = document.querySelector(".emailSuccess");
const signup = document.querySelector(".signup");

usernameField.addEventListener('keyup', (e) => {
    const usernameVal = e.target.value;
    usernameField.classList.remove("is-invalid");
    feedbackArea.style.display = 'none';
    usernameSuccess.textContent = `Checking ${usernameVal}`;
    if (usernameVal.length > 0) {
        fetch('/account/validate-username', {
            body: JSON.stringify({ 'username': usernameVal }),
            method: 'POST'
        }).then(res => res.json()).then(data => {
            usernameSuccess.style.display = 'none';
            if (data.username_error) {
                signup.disabled = true;
                usernameField.classList.add('is-invalid');
                feedbackArea.style.display = 'block';
                feedbackArea.innerHTML = `<p>${data.username_error}</p>`;
            } else {
                signup.disabled = false;
            }

        });

    }


});


emailField.addEventListener('keyup', (e) => {
    let regex = new RegExp('[a-z0-9]+@[a-z]+\.[a-z]{2,3}');
    const emailVal = e.target.value;
    emailField.classList.remove("is-invalid");
    emailFeedBack.style.display = 'none';
    emailSuccess.textContent = `Checking ${emailVal}`;
    if (emailVal.length > 0) {
        fetch("/account/validate-email", {
            body: JSON.stringify({ "email": emailVal }),
            method: "POST",
        }).then(res => res.json()).then((data) => {
            emailSuccess.style.display = 'none';
            if (data.email_error) {
                signup.disabled = true;
                emailField.classList.add("is-invalid");
                emailFeedBack.style.display = 'block';
                emailFeedBack.innerHTML = `<p>${data.email_error}</p>`;
            } else {
                signup.disabled = false;
            }
        });
    }
});