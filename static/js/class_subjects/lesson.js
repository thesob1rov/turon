let lesson = document.querySelectorAll('.lesson_box'), save_btn = document.querySelector('.save_btn'),
    active_lesson = document.querySelectorAll('.lesson_box.active_color');

lesson.forEach(item => {
    item.addEventListener('click', () => {
        item.classList.toggle('active_color')
    })

})

const info = {
    class_id: "", subjects: [],
    remove_subject: []
}
active_lesson.forEach(item => {
    item.addEventListener("click", () => {
        info.remove_subject.push(item.dataset.id)
    })
})

save_btn.addEventListener('click', () => {
    let className = "lesson_box active_color"
    info.class_id = save_btn.dataset.id
    lesson.forEach(item => {
        if (item.classList.value === className) {
            info.subjects.push(item.dataset.id)
        }
    })
    fetch('/add_class_subjects', {
        method: "POST", body: JSON.stringify({
            "info": info
        }), headers: {
            'Content-type': 'application/json'
        }
    })
})

