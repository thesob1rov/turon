let password_icon = document.querySelector('.password_icon'),
    password = document.querySelector('.password');

password_icon.addEventListener('click', () => {
    if (password.type === "password") {
        password.type = "text"
        password_icon.className = "fa-solid fa-eye-slash password_icon"
    } else {
        password.type = "password"
        password_icon.className = "fa-solid fa-eye password_icon"
    }
})
