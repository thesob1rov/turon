let create = document.querySelector('.create'), x = document.querySelector('.x'),
    filter_btn = document.querySelector('.filter_btn'), double = document.querySelector('.double'),
    filter = document.querySelector('.filter'), add = document.querySelector('.add'),
    next = document.querySelector('.next'), filter_form = document.querySelector('.form_filter'),
    class_number = document.querySelector('.class_number'), select = document.querySelector('.select'),
    tbody = document.querySelector('.tbody')


const search = document.querySelector('.search');
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
    const info = {
        subject_id: select.value, search: search.value
    }
    fetch('/filter_teacher', {
        method: "POST", body: JSON.stringify({
            "info": info
        }), headers: {
            'Content-type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(resp => {

            tbody.innerHTML = ''
            const item = resp['filtered_users']
            for (const i in resp ['filtered_teachers']) {
                if (item[i].classes === "true") {
                    tbody.innerHTML += `<tr>
                            <td></td>
                            <td><a href="/teacher_profile_info/${item[i].id}"><img
                                    src="${item[i].image}" alt=""></a></td>
                            <td>${item[i].name}</td>
                            <td>${item[i].surname}</td>
                            <td>${item[i].age}</td>
                            <td>${item[i].number}</td>
                            <td></td>
                        </tr>`
                } else {
                    tbody.innerHTML += `<tr>
                            <td></td>
                            <td><a href="/teacher_profile_info/${item[i].id}"><img
                                    src="${info.image}" alt=""></a></td>
                            <td>${item[i].name}</td>
                            <td>${item[i].surname}</td>
                            <td>${item[i].age}</td>
                            <td>${item[i].number}</td>
                            <td>
                                <a href="/delete_teacher/${item[i].teacher_id}">
                                    <i class="fa-solid fa-trash" style="color: red"></i>
                                </a>
                            </td>
                        </tr>`
                }
            }
        })
})


search.addEventListener('input', () => {
    fetch('/search_teacher', {
        method: "POST", body: JSON.stringify({
            "search": search.value
        }), headers: {
            'Content-type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(resp => {

            tbody.innerHTML = ''
            const item = resp['filtered_users']
            for (const i in resp['filtered_users']) {

                // tbody.innerHTML = ''
                if (item[i].classes === "true") {
                    number = +i + 1
                    tbody.innerHTML += `<tr>
                            <td>${number}</td>
                            <td><a href="/teacher_profile_info/${item[i].id}"><img
                                    src="${item[i].image}" alt=""></a></td>
                            <td>${item[i].name}</td>
                            <td>${item[i].surname}</td>
                            <td>${item[i].age}</td>
                            <td>${item[i].number}</td>
                            <td></td>
                        </tr>`
                } else {
                    console.log(i)
                    number = +i + 1
                    tbody.innerHTML += `<tr>
                            <td>${number}</td>
                            <td><a href="/teacher_profile_info/${item[i].id}"><img
                                    src="${item[i].image}" alt=""></a></td>
                            <td>${item[i].name}</td>
                            <td>${item[i].surname}</td>
                            <td>${item[i].age}</td>
                            <td>${item[i].number}</td>
                            <td>
                                <a href="/delete_teacher/${i.teacher_id}">
                                    <i class="fa-solid fa-trash" style="color: red"></i>
                                </a>
                            </td>
                        </tr>`
                }
            }
        })
})
