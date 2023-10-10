let change = document.querySelector('.change_all'), ellipsis = document.querySelector('.ellipsis'),
    change_edit = document.querySelector('.change_edit'), change_exit = document.querySelector('.change_exit'),
    edit = document.querySelector('.edit'), edit_user_btn = document.querySelector('.edit_user_btn'),
    edit_lock_btn = document.querySelector('.edit_lock_btn'), lock_form = document.querySelector('.lock_form'),
    passwords = document.querySelectorAll('.password'), password1 = document.querySelector('#password1'),
    checkbox = document.querySelector('.checkbox'), password2 = document.querySelector('#password2'),
    error_length = document.querySelector('.error_length'), error_match = document.querySelector('.error_match'),
    user_form = document.querySelector('.user_form'), main = document.querySelector('.main'),
    main_box = document.querySelector('.main_box');

ellipsis.addEventListener('click', () => {
    if (change.style.display === "flex") {
        change.style.display = "none"
    } else {
        change.style.display = "flex"
    }
})

main.addEventListener('click', (event) => {
    if (event.target === main) {
        change.style.display = "none"
    }
})

main_box.addEventListener('click', (event) => {
    console.log(event.target)
    if (event.target === document.querySelector('.main_about') || (event.target === document.querySelector('.main_profile' ))) {
        change.style.display = "none"
    }
})


change_edit.addEventListener('click', () => {
    edit.style.display = "flex"
})

edit_user_btn.addEventListener('click', () => {
    user_form.style.display = "flex"
    edit_user_btn.classList.add('active_color')
    edit_lock_btn.classList.remove('active_color')
})
edit_lock_btn.addEventListener('click', () => {
    lock_form.style.display = "flex"
    user_form.style.display = "none"
    edit_lock_btn.classList.add('active_color')
    edit_user_btn.classList.remove('active_color')
})


checkbox.addEventListener('change', function () {
    passwords.forEach(password => {
        if (checkbox.checked === true) {
            password.type = "text";
        } else {
            password.type = "password";
        }
    })
})

password1.addEventListener('input', () => {
    if (password1.value.length < 8) {
        error_length.style.display = "block"
    } else {
        error_length.style.display = "none"
        comparePassword()
    }
})

function comparePassword() {
    if (password2.value !== password1.value) {
        error_match.style.display = "block"
    } else {
        error_match.style.display = "none"
    }
}

password2.addEventListener('input', () => {
    comparePassword()
})



