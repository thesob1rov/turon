let creat = document.querySelector('.create_bnt'),
    class_name = document.querySelector('.class_name'),
    teacher_id = document.querySelector('.teacher_id'),
    number = document.querySelector('.class_number'),
    from = document.querySelector('.from'),
    to = document.querySelector('.to'),
    filter_form = document.querySelector('.form_filter'),
    tbody = document.querySelector('.tbody'),
    radio = document.querySelectorAll('.radio'),
    subject_id = document.querySelector('.subject_id'),
    join = document.querySelector('.join'),
    language_type = document.querySelector('.language_type'),
    creat_language_type = document.querySelector('.creat_language_type');

let classes = []

const search = document.querySelector('.search');
filter_form.addEventListener('click', () => {
    const info = {
        class_number: number.value,
        from: from.value,
        to: to.value,
        language_type: language_type.value,
        search: search.value
    }
    fetch('/filter_student_for_flow', {
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
            classes_check()
        })
})

function classes_check() {
    let checkboxes = document.querySelectorAll('.checkbox');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            if (checkbox.checked) {
                const class_id = checkbox.dataset.id
                classes.push(class_id)
            }
        })
    })
}

classes_check()

creat.addEventListener('click', () => {
    const flow_info = {
        name: class_name.value,
        teacher_id: teacher_id.value,
        subject_id: subject_id.value,
        classes: classes
    }
    console.log(flow_info)
    fetch('/creat_flow', {
        method: "POST", body: JSON.stringify({
            "flow_info": flow_info
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
        classes: classes
    }
    console.log(join_class)
    fetch('/join_flow', {
        method: "POST", body: JSON.stringify({
            "join_class": join_class
        }), headers: {
            'Content-type': 'application/json'
        }
    })
})


search.addEventListener('input', () => {
    fetch('/search_not_student_for_flow', {
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
