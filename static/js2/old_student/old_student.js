let btn = document.querySelector('.btn'),
    filter_btn = document.querySelector('.filter_btn'), double = document.querySelector('.double'),
    filter = document.querySelector('.filter');


filter_btn.addEventListener('click', () => {
    if (double.style.display === "none") {
        double.style.display = "flex"
        filter.style.display = "none"
    } else {
        double.style.display = "none"
        filter.style.display = "flex"
    }
})




let number = document.querySelector('.class_number'),
    from = document.querySelector('.from'),
    to = document.querySelector('.to'),
    filter_form = document.querySelector('.form_filter'),
    tbody = document.querySelector('.tbody'),
    class_number = document.querySelector('.create_class_number'),
    join = document.querySelector('.join'),
    language_type = document.querySelector('.language_type');


filter_form.addEventListener('click', () => {
    const info = {
        class_number: number.value,
        from: from.value,
        to: to.value,
        language_type: language_type.value
    }
    fetch('/filter_student_old', {
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
        })
})

