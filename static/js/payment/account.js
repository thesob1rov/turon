let input_one = document.querySelector('.input_one'), table = document.querySelector('.table'),
    delButton = document.querySelectorAll('.delButton'), input_two = document.querySelector('.input_two'),
    button_student = document.querySelector('.button_student'), button_cost = document.querySelector('.button_cost'),
    buttons = document.querySelectorAll('.pay_buttons button'), button = '', balance = document.querySelector('.h1');


function search() {
    if (input_one.value && input_two.value) {
        fetch('/search', {
            method: 'POST', body: JSON.stringify({
                'input_one': input_one.value,
                'input_two': input_two.value,
                'type_request': input_one.dataset.type,
                'button': button
            }), headers: {
                'Content-type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(response => {

                table.innerHTML = ''
                for (let i = 0; i < response['payments'].length; i++) {
                    table.innerHTML += `<tr>
                                <td>${i + 1}</td>
                                <td>${response['payments'][i].name}</td>
                                <td>${response['payments'][i].surname}</td>
                                <td>${response['payments'][i].payed}</td>
                                <td>${response['payments'][i].account_type_name}</td>
                                <td>${response['payments'][i].date}</td>
                                <td><i class="fa-solid fa-trash delButtonPay" style="color: red"
                                       data-id="${response['payments'][i].id}" data-type="${input_one.dataset.type}"></i></td>
                            </tr>`

                }
                balance.innerText = `Jami summa ${response['balance']}`


            })
    } else if (input_one.value === '' && input_two.value === '') {
        fetch('/search', {
            method: 'POST', body: JSON.stringify({
                'input_one': null, 'input_two': null, 'type_request': input_one.dataset.type, 'button': button
            }), headers: {
                'Content-type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(response => {

                table.innerHTML = ''
                for (let i = 0; i < response['payments'].length; i++) {
                    if (input_one.dataset.type !== 'co') {
                        table.innerHTML += `<tr>
                                <td>${i + 1}</td>
                                <td>${response['payments'][i].name}</td>
                                
                                <td>${response['payments'][i].surname}</td>
                                <td>${response['payments'][i].payed}</td>
                                <td>${response['payments'][i].account_type_name}</td>
                                <td>${response['payments'][i].date}</td>
                                <td><i class="fa-solid fa-trash delButtonPay" style="color: red"
                                       data-id="${response['payments'][i].id}" data-type="${input_one.dataset.type}"></i></td>
                            </tr>`
                    } else {
                        table.innerHTML += `<tr>
                                <td>${i + 1}</td>
                                <td>${response['payments'][i].name}</td>
                                <td>${response['payments'][i].payed}</td>
                                <td>${response['payments'][i].account_type_name}</td>
                                <td>${response['payments'][i].date}</td>
                                <td><i class="fa-solid fa-trash delButtonPay" style="color: red"
                                       data-id="${response['payments'][i].id}" data-type="${input_one.dataset.type}"></i></td>
                            </tr>`
                    }


                }
                balance.innerText = `Jami summa ${response['balance']}`


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
        button = item.innerText
        search()
    })
})


delButton.forEach(trash => {
    trash.addEventListener("click", () => {
        const confirm_question = confirm("Siz bu tolovni ochirmoqchimisiz?")
        if (confirm_question === true) {
            fetch('/delete_object', {
                method: "POST", body: JSON.stringify({
                    "id": trash.dataset.id, 'type': trash.dataset.type
                }), headers: {
                    'Content-type': 'application/json'
                }
            })
                .then(response => response.json())
                .then(resp => {
                    if (resp['status'] === true) {
                        window.location.href = `/collection/${trash.dataset.type}/`;
                    }
                })
        }
    })
})

