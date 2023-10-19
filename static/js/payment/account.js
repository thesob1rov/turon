let input_one = document.querySelector('.input_one'), table_first = document.querySelector('.table_first'),
    table_second = document.querySelector('.table_second'), input_two = document.querySelector('.input_two'),
    button_student = document.querySelector('.button_student'),
    button_cost = document.querySelector('.button_cost'),
    buttons = document.querySelectorAll('.pay_buttons button'), button = '',
    balance = document.querySelector('.info_item'), balance_h1 = document.querySelector('.h1');

table_first.classList.add('active_paginate')
button_student.addEventListener('click', () => {
    table_first.classList.add('active_paginate')
    table_second.classList.remove('active_paginate')
})
button_cost.addEventListener('click', () => {
    table_first.classList.remove('active_paginate')
    table_second.classList.add('active_paginate')
})

function search() {
    if (input_one.value && input_two.value) {
        fetch('search', {
            method: 'POST', body: JSON.stringify({
                'input_one': input_one.value, 'input_two': input_two.value, 'button': button
            }), headers: {
                'Content-type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(response => {
                table_first.innerHTML = ''
                table_second.innerHTML = ''
                for (let i = 0; i < response['payments'].length; i++) {
                    table_first.innerHTML += `<tr>
                                <td>${i + 1}</td>
                                <td>${response['payments'][i].name}</td>
                                <td>${response['payments'][i].surname}</td>
                                <td>${response['payments'][i].payed}</td>
                                <td>${response['payments'][i].account_type_name}</td>
                                <td>${response['payments'][i].date}</td>
                                <td><i class="fa-solid fa-trash delButtonPay" style="color: red"
                                       data-id="${response['payments'][i].id}"></i></td>
                            </tr>`

                }
                for (let i = 0; i < response['cost'].length; i++) {
                    table_second.innerHTML += `<tr>
                                <td>${i + 1}</td>
                                <td>${response['cost'][i].name}</td>
                                <td>${response['cost'][i].payed}</td>
                                <td>${response['cost'][i].account_type_name}</td>
                                <td>${response['cost'][i].date}</td>
                                <td><i class="fa-solid fa-trash delButtonPay" style="color: red"
                                       data-id="${response['cost'][i].id}"></i></td>
                            </tr>`

                }
                balance.innerText = `Jami summa ${response['balance']}`
                balance_h1.innerText = `Jami summa ${response['balance']}`
            })
    }
}

input_one.addEventListener('change', () => {
    search()
})
input_two.addEventListener('change', () => {
    search()
})

buttons.forEach((item, index) => {
    item.addEventListener('click', () => {
        if (input_one.value && input_two.value) {
            button = item.innerText
            search()
        }
    })
})



