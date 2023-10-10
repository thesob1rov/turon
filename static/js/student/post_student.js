let creat = document.querySelector('.create_bnt'),
    class_name = document.querySelector('.class_name'),
    teacher_id = document.querySelector('.teacher_id'),
    number = document.querySelector('.class_number'),
    from = document.querySelector('.from'),
    to = document.querySelector('.to'),
    filter_form = document.querySelector('.form_filter'),
    tbody = document.querySelector('.tbody'),
    radio = document.querySelectorAll('.radio'),
    class_number = document.querySelector('.create_class_number'),
    join = document.querySelector('.join'),
    language_type = document.querySelector('.language_type'),
    creat_language_type = document.querySelector('.creat_language_type');
let students = []

const search = document.querySelector('.search');
filter_form.addEventListener('click', () => {
    const info = {
        class_number: number.value,
        from: from.value,
        to: to.value,
        language_type: language_type.value,
        search: search.value
    }
    fetch('/filter_student', {
        method: "POST", body: JSON.stringify({
            "info": info
        }), headers: {
            'Content-type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(resp => {

            tbody.innerHTML = ''
            for (const info of resp['filter_student']) {

                // tbody.innerHTML = ''
                tbody.innerHTML += `<tr>
                            <td></td>
                            <td><a href="/student_profile/${info.id}"><img
                                    src="${info.image}" alt=""></a></td>
                            <td>${info.name}</td>
                            <td>${info.surname}</td>
                            <td>${info.age}</td>
                            <td>class</td>
                            <td>${info.number}</td>
                            <td><input class="checkbox" type="checkbox" data-id="${info.id}"></td>
                        </tr>`
            }
            students_check()
        })


})

function students_check() {
    let checkboxes = document.querySelectorAll('.checkbox');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {

            if (checkbox.checked) {
                const student_id = checkbox.dataset.id

                students.push(student_id)
            }
        })
    })
}

students_check()

const color = document.querySelector('.color');
creat.addEventListener('click', () => {

    const class_info = {
        name: class_name.value,
        teacher_id: teacher_id.value,
        students: students,
        class_number: class_number.value,
        color: color.value,
        creat_language_type: creat_language_type.value
    }
    console.log(class_info)
    fetch('/creat_class', {
        method: "POST", body: JSON.stringify({
            "class_info": class_info
        }), headers: {
            'Content-type': 'application/json'
        }
    })
})

let class_id = 0;
radio.forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        if (checkbox.checked) {
            console.log(checkbox.dataset.id)
            class_id = checkbox.dataset.id
        }
    })
})
console.log(join)
join.addEventListener('click', () => {
    console.log('adc')
    const join_class = {
        class_id: class_id,
        students: students
    }
    console.log(join_class)
    fetch('/join_class', {
        method: "POST", body: JSON.stringify({
            "join_class": join_class
        }), headers: {
            'Content-type': 'application/json'
        }
    })
})


search.addEventListener('input', () => {
    fetch('/search_not_student_in_class', {
        method: "POST", body: JSON.stringify({
            "search": search.value
        }), headers: {
            'Content-type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(resp => {

            tbody.innerHTML = ''
            for (const info of resp['filtered_users']) {

                // tbody.innerHTML = ''
                tbody.innerHTML += `<tr>
                            <td></td>
                            <td><a href="/student_profile/${info.id}"><img
                                    src="${info.image}" alt=""></a></td>
                            <td>${info.name}</td>
                            <td>${info.surname}</td>
                            <td>${info.age}</td>
                            <td>${info.number}</td>
                            <td>${info.language}</td>
                            <td><input class="checkbox" type="checkbox" data-id="${info.id}"></td>
                        </tr>`
            }
            students_check()
        })
})


let trashs = document.querySelectorAll('.fa-trash');

trashs.forEach(trash => {
    trash.addEventListener("click", () => {
        const confirm_question = confirm("Siz bu o'quvchini ochirmoqchimisiz?")
        if (confirm_question === true) {
            fetch('/delete_student', {
                method: "POST", body: JSON.stringify({
                    "id": trash.dataset.id
                }), headers: {
                    'Content-type': 'application/json'
                }
            })
                .then(function (response) {
                    return response.json()
                })
                .then(function (res) {
                    window.location.reload()
                })
        }
    })
})
