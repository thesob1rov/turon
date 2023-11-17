let salary = document.querySelector('.oylik'),
    new_box = document.querySelector('.new'),
    new_date = document.querySelector('.new_date'),
    plus = document.querySelector('.plus'),
    setting = document.querySelector('.setting'),
    radio_old = document.querySelector('.radio_old'),
    radio_new = document.querySelector('.radio_new'),
    send_worked_days = document.querySelector(".send_worked_days"),
    month_id = document.querySelector(".month_id"),
    new_salary_type = document.querySelector(".new_salary_type"),
    new_salary_name = document.querySelector('.new_salary_name'),
    new_salary_money = document.querySelector('.new_salary_money'),
    send_new_salary_type = document.querySelector(".new_salary_type button"),
    select_salary_type = document.querySelector(".select_salary_type"),
    send_select_salary_type = document.querySelector(".select_salary_type button"),
    select_type = document.querySelector(".select_salary_type select"),
    worked_days = document.querySelector('.days');

setting.addEventListener('click', () => {
    new_box.classList.add('active_box')
})
plus.addEventListener('click', () => {
    new_date.classList.add('active_box')
})
new_box.addEventListener('click', (event) => {
    if (event.target === new_box) {
        new_box.classList.remove('active_box')
    }
})
new_date.addEventListener('click', (event) => {
    if (event.target === new_date) {
        new_date.classList.remove('active_box')
    }
})

send_worked_days.addEventListener("click", () => {
    info = {
        worked_days: worked_days.value,
        teacher_salary_id: month_id.value
    }
    fetch('/enter_teacher_worked_days', {
        method: "POST", body: JSON.stringify({
            "info": info
        }), headers: {
            'Content-type': 'application/json'
        }
    })
    worked_days.value = ""
    month_id.value = ""
    new_date.classList.remove('active_box')
    window.location.reload()
})

radio_old.addEventListener("change", () => {
    select_salary_type.style.display = "flex"
    new_salary_type.style.display = "none"
})

radio_new.addEventListener("change", () => {
    select_salary_type.style.display = "none"
    new_salary_type.style.display = "flex"
})

send_select_salary_type.addEventListener("click", () => {
    info = {
        teacher_id: send_select_salary_type.dataset.id,
        salary_type_id: select_type.value
    }
    fetch('/enter_teacher_salary_type', {
        method: "POST", body: JSON.stringify({
            "info": info
        }), headers: {
            'Content-type': 'application/json'
        }
    })
    new_date.classList.remove('active_box')
    window.location.reload()
})

send_new_salary_type.addEventListener("click", () => {
    info = {
        teacher_id: send_select_salary_type.dataset.id,
        salary_type_name: new_salary_name.value,
        new_salary_money: new_salary_money.value
    }
    fetch('/create_teacher_salary_type', {
        method: "POST", body: JSON.stringify({
            "info": info
        }), headers: {
            'Content-type': 'application/json'
        }
    })
    new_date.classList.remove('active_box')
    window.location.reload()
})