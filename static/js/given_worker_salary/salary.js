let salary = document.querySelector('.salary'), icon = document.querySelector('.money'),
    send_salary = document.querySelector('.salary_btn'), salary_money = document.querySelector('.salary_money'),
    radio = document.querySelectorAll('.radio'), radio2 = document.querySelectorAll('.radio2'),
    reason = document.querySelector('.reason'), account_types = document.querySelectorAll('.account_types'),
    delete_btn = document.querySelectorAll('.fa-trash'), top2 = document.querySelector('.top2'),
    salary2 = document.querySelector('#salary'), salary_main = document.querySelector('.salary_main'),
    button = document.querySelector('.top2 button');


account_types.forEach(item => {
    item.addEventListener('click', () => {
        salary2.style.display = 'flex'
        button.addEventListener('click', () => {
            info = {
                worker_salary_inDay_id: item.dataset.id, account_type_id: 0
            }
            radio2.forEach(item => {
                if (item.checked) {
                    info.account_type_id = item.dataset.id
                }
            })
            fetch('/change_worker_salary_account_type', {
                method: "POST", body: JSON.stringify({
                    "info": info
                }), headers: {
                    'Content-type': 'application/json'
                }
            })
            window.location.reload(true)
        })
    })
})

icon.addEventListener('click', () => {
    salary.style.display = "flex"
})
salary.addEventListener('click', (event) => {
    if (event.target === salary) {
        salary.style.display = "none"
    }
})
salary2.addEventListener('click', (event) => {
    if (event.target === salary2) {
        salary2.style.display = "none"
    }
})

send_salary.addEventListener("click", () => {
    info = {
        money: salary_money.value, worker_salary_id: send_salary.dataset.id, reason: reason.value, account_type_id: "",
    }
    radio.forEach(item => {
        if (item.checked) {
            info.account_type_id = item.dataset.id
        }
    })
    fetch('/given_worker_salary', {
        method: "POST", body: JSON.stringify({
            "info": info
        }), headers: {
            'Content-type': 'application/json'
        }
    })
    salary.style.display = "none"
    window.location.reload()
})

delete_btn.forEach(item => {
    item.addEventListener("click", () => {
        info = {
            given_salary_id: item.dataset.id
        }
        const question = confirm("Berilgan oylikni ochirmoqchimisiz ?")
        if (question === true) {
            fetch('/delete_worker_given_salary', {
                method: "POST", body: JSON.stringify({
                    "info": info
                }), headers: {
                    'Content-type': 'application/json'
                }
            })
            window.location.reload()
        }
    })
})