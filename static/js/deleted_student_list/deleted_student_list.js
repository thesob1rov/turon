let
    filter_btn = document.querySelector('.filter_btn'), double = document.querySelector('.double'),
    filter = document.querySelector('.filter');

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
    language_type = document.querySelector('.language_type');
filter_btn.addEventListener('click', () => {
    if (double.style.display === "none") {
        double.style.display = "flex"
        filter.style.display = "none"
    } else {
        double.style.display = "none"
        filter.style.display = "flex"
    }
})


const search = document.querySelector('.search');
filter_form.addEventListener('click', () => {
    const info = {
        class_number: number.value,
        from: from.value,
        to: to.value,
        language_type: language_type.value,
        search: search.value
    }
    fetch('/filter_delete_student', {
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
                            <td>${info.number}</td>
                            <td>${info.language}</td>
                            <td><i class="fa-solid fa-trash" style="color: red" data-id="${info.student}"></i></td>
                        </tr>`
            }
            return_students()

        })
})


function return_students() {

    let trashs = document.querySelectorAll('.fa-trash');
    trashs.forEach(trash => {
        trash.addEventListener("click", () => {
            const confirm_question = confirm("Siz bu oquvchini qaytarmoqchimmisiz ?")
            if (confirm_question === true) {
                fetch('/return_students', {
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
}

return_students()


search.addEventListener('input', () => {
    fetch('/search_delete_student', {
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
                            <td><i class="fa-solid fa-trash" style="color: red" data-id="${info.student}"></i></td>
                        </tr>`
            }
            return_students()
        })

})