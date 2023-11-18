let salary = document.querySelector('.oylik'),
    new_box = document.querySelector('.new'),
    plus = document.querySelector('.plus'),
    setting = document.querySelector('.setting'),
    month_id = document.querySelector(".month_id"),
    new_salary_money = document.querySelector('.new_salary_money'),
    send_new_salary_type = document.querySelector(".new_salary_type button")

setting.addEventListener('click', () => {
    new_box.classList.add('active_box')
})

new_box.addEventListener('click', (event) => {
    if (event.target === new_box) {
        new_box.classList.remove('active_box')
    }
})


send_new_salary_type.addEventListener("click", () => {
    info = {
        worker_id: send_new_salary_type.dataset.id,
        new_salary_money: new_salary_money.value
    }
    fetch('/set_worker_salary', {
        method: "POST", body: JSON.stringify({
            "info": info
        }), headers: {
            'Content-type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(resp => {
             new_box.classList.remove('active_box')
             window.location.reload()
         })

})