let subject_overlay = document.querySelector('.subject_overlay'),
    subject_overlay_add = document.querySelector('.subject_overlay_add'),
    x = document.querySelector('.subject_overlay_x'),
    x_add = document.querySelector('.subject_overlay_add_x'),
    btn = document.querySelector('.subject_add'),
    trash = document.querySelectorAll('.subject_change'),
    edit = document.querySelectorAll('.subject_edit'),
    edit_subject_id = 0,
    get_btn = document.querySelector('.get'),
    change_subject = document.querySelector('.change_subject'),
    subject_title = document.querySelectorAll('.subject_title');

edit.forEach((item, index) => {
    item.addEventListener('click', () => {
        subject_overlay.style.display = "flex"
        edit_subject_id = item.dataset.id
        change_subject.value = subject_title[index].innerText
    })
})

get_btn.addEventListener("click", () => {
    const info = {
        subject_id: edit_subject_id,
        subject_name: change_subject.value
    }
    fetch('/change_subjects', {
        method: "POST", body: JSON.stringify({
            "info": info
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
})


x.addEventListener('click', () => {
    subject_overlay.style.display = "none"
})
x_add.addEventListener('click', () => {
    subject_overlay_add.style.display = "none"
})
subject_overlay.addEventListener('click', (event) => {
    if (event.target === subject_overlay) {
        subject_overlay.style.display = "none"
    }
})

btn.addEventListener('click', () => {
    subject_overlay_add.style.display = "flex"
})

trash.forEach((item, index) => {
    item.addEventListener('click', () => {
        fetch('/delete_subjects', {
            method: "POST", body: JSON.stringify({
                "info": item.dataset.id
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
    })
})

