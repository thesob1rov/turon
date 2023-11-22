let salary = document.querySelector('.salary'),
    icon = document.querySelector('.money'),
    send_salary = document.querySelector('.salary_btn'),
    salary_money = document.querySelector('.salary_money'),
    radio = document.querySelectorAll('.radio'),
    reason = document.querySelector('.reason'),
    delete_btn = document.querySelectorAll('.fa-trash'),
    salary_main = document.querySelector('.salary_main');
icon.addEventListener('click', () => {
    salary.style.display = "flex"
})
salary.addEventListener('click', (event) => {
    if (event.target === salary) {
        salary.style.display = "none"
    }
})

send_salary.addEventListener("click", () => {
    info = {
        money: salary_money.value,
        teacher_salary_id: send_salary.dataset.id,
        reason: reason.value,
        account_type_id: "",
    }
    radio.forEach(item => {
        if (item.checked) {
            info.account_type_id = item.dataset.id
        }
    })
    fetch('/given_teacher_salary', {
        method: "POST", body: JSON.stringify({
            "info": info
        }), headers: {
            'Content-type': 'application/json'
        }
    })
    new_date.classList.remove('active_box')
    window.location.reload()
})

delete_btn.forEach(item => {
    item.addEventListener("click", () => {
        info = {
            given_salary_id: item.dataset.id,
            teacher_salary_id: send_salary.dataset.id,
        }
        const question = confirm("Berilgan oylikni ochirmoqchimisiz ?")
        if (question === true) {
            console.log(info)
            fetch('/delete_teacher_given_salary', {
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