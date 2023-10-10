let create = document.querySelector('.create'), x = document.querySelector('.x'),
    filter_btn = document.querySelector('.filter_btn'), double = document.querySelector('.double'),
    filter = document.querySelector('.filter'),
    add = document.querySelector('.add'),
    next = document.querySelector('.next'),
    filter_form = document.querySelector('.form_filter'),
    class_number = document.querySelector('.class_number'),
    select = document.querySelector('.select'),
    tbody = document.querySelector('.tbody')

filter_btn.addEventListener('click', () => {


    if (double.style.display === "none") {
        double.style.display = "flex"
        filter.classList.remove('active_filter')
    } else {
        double.style.display = "none"
        filter.classList.add('active_filter')
    }

})

filter_form.addEventListener('click', () => {
    const subject_id = select.value
    fetch('/filter_teacher', {
        method: "POST", body: JSON.stringify({
            "subject_id": subject_id
        }), headers: {
            'Content-type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(resp => {

            tbody.innerHTML = ''
            for (const info of resp ['filtered_teachers']) {

                tbody.innerHTML += `<tr>
                            <td></td>
                            <td><a href="/teacher_profile_info/${info.id}"><img
                                    src="${info.image}" alt=""></a></td>
                            <td>${info.name}</td>
                            <td>${info.surname}</td>
                            <td>${info.age}</td>
                            <td>class</td>
                            <td>${info.number}</td>
                        </tr>`
            }
            students_check()
        })
})