let filter_btn = document.querySelector('.pay_filter_btn'), filter_form = document.querySelector('.filter'),
    search = document.querySelector('.pay_search input'), pay_double = document.querySelector('.pay_double'),
    account_type = document.querySelector('.account_type'), year = document.querySelector('.year'),
    month = document.querySelector('.month'), day = document.querySelector('.day'),
    section = document.querySelector('.pay'), search_filter = document.querySelector('.form_filter'),
    index = document.querySelector('.payment'), pay_list = document.querySelector('.pay_list'),
    cost_list = document.querySelector('.cost_list'), add = document.getElementById('add'),
    plus = document.querySelector('.harajat_plus_circle'), radio = document.querySelectorAll('.radio'),
    nameInput = document.querySelector('.nameInput'), paginate = document.querySelector('.pay_next'),
    input_type_id = document.querySelector('.input_type_id'), payedInput = document.querySelector('.payedInput'),
    select = document.querySelector('.select'), tbody = document.querySelector('tbody');

paginate.classList.add('active_paginate')
if (section.dataset.type === 'pay') {
    search.addEventListener('input', () => {
        console.log(search.value)
        if (search.value) {
            paginate.classList.remove('active_paginate')
        } else {
            paginate.classList.add('active_paginate')
            window.location.href = '/all_payments/pay/1';
        }
        fetch('/search_pay', {
            method: "POST", body: JSON.stringify({
                "search": search.value
            }), headers: {
                'Content-type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(resp => {
                tbody.innerHTML = ''
                for (let i = 0; i < resp['filtered_pay'].length; i++) {
                    tbody.innerHTML += `<tr>
                                <td>${i + 1}</td>
                                <td>${resp['filtered_pay'][i].name}</td>
                                <td>${resp['filtered_pay'][i].surname}</td>
                                <td>${resp['filtered_pay'][i].payed}</td>
                                <td>${resp['filtered_pay'][i].account_type_name}</td>
                                <td>${resp['filtered_pay'][i].date}</td>
                                <td><i class="fa-solid fa-trash delButtonPay" style="color: red"
                                       data-id="${resp['filtered_pay'][i].id}"></i></td>
                            </tr>`
                }

            })
    })
} else if (section.dataset.type === 'cost') {
    search.addEventListener('input', () => {
        if (search.value) {
            paginate.classList.remove('active_paginate')
        } else {
            paginate.classList.add('active_paginate')
            window.location.href = '/all_payments/cost/1';
            // search.click
        }
        fetch('/search_cost', {
            method: "POST", body: JSON.stringify({
                "search": search.value
            }), headers: {
                'Content-type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(resp => {
                console.log(resp)
                tbody.innerHTML = ''
                for (let i = 0; i < resp['filtered_cost'].length; i++) {
                    tbody.innerHTML += `<tr>
                                <td>${i + 1}</td>
                                <td>${resp['filtered_cost'][i].name}</td>
                                <td>${resp['filtered_cost'][i].payed}</td>
                                <td>${resp['filtered_cost'][i].account_type_name}</td>
                                <td>${resp['filtered_cost'][i].date}</td>
                                <td><i class="fa-solid fa-trash delButtonPay" style="color: red"
                                       data-id="${resp['filtered_cost'][i].id}"></i></td>
                            </tr>`
                }

            })
    })
}
input_type_id.style.display = 'none'
radio.forEach(item => {
    item.addEventListener('click', () => {
        input_type_id.value = item.dataset.id
    })
})

select.addEventListener('change', () => {
    if (select.value === 'payOption') {
        window.location.href = '/all_payments/pay/1';
    } else if (select.value === 'costOption') {
        window.location.href = '/all_payments/cost/1';
    }
})


plus.addEventListener('click', () => {
    index.classList.add('active')
})
index.addEventListener('click', (e) => {
    if (e.target === index) {
        index.classList.remove('active')
    }

})

filter_btn.addEventListener('click', () => {
    if (filter_form.style.display === "none") {
        filter_form.style.display = "flex"
        search.style.display = "none"
        pay_double.style.width = `${12}%`
    } else {
        filter_form.style.display = "none"
        search.style.display = "flex"
        pay_double.style.width = `${50}%`
    }
})

search_filter.addEventListener('click', () => {
    const info = {
        account_type_id: account_type.value, year: year.value, month: month.value
    }
    fetch('/filter_payments', {
        method: "POST", body: JSON.stringify({
            "info": info
        }), headers: {
            'Content-type': 'application/json'
        }
    })
    // .then(response => response.json())
    // .then(resp => {
    //
    //     tbody.innerHTML = ''
    //     for (const info of resp['filter_student']) {
    //
    //         // tbody.innerHTML = ''
    //         tbody.innerHTML += `<tr>
    //                     <td></td>
    //                     <td><a href="/student_profile/${info.id}"><img
    //                             src="${info.image}" alt=""></a></td>
    //                     <td>${info.name}</td>
    //                     <td>${info.surname}</td>
    //                     <td>${info.age}</td>
    //                     <td>class</td>
    //                     <td>${info.number}</td>
    //                     <td><input class="checkbox" type="checkbox" data-id="${info.id}"></td>
    //                 </tr>`
    //     }
    //     students_check()
    // })
})
