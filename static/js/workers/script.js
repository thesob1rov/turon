let teacher_circle = document.querySelector('.teacher_circle'),
    registratsiya_close = document.querySelector('.registratsiya_close'),
    registratsiya = document.querySelector('.registratsiya'),
    edit = document.querySelectorAll('.edit'),
    teacher_img = document.querySelectorAll('.teacher_img img'),
    name = document.querySelectorAll('.name'),
    surname = document.querySelectorAll('.surname'),
    teacher_information = document.querySelectorAll('.teacher_information p'),
    job = document.querySelectorAll('.job'),
    registratsiya_block = document.querySelector('.registratsiya_block'),
    registratsiya_left = document.querySelector('.registratsiya_left'),
    registratsiya_file = document.querySelector('.registratsiya_file'),
    registratsiya_left_img = document.querySelector('.registratsiya_left_img'),
    modal_name = document.querySelector('.modal_name'),
    modal_surname = document.querySelector('.modal_surname'),
    modal_job = document.querySelectorAll('.modal_job option'),
    modal_textarea = document.querySelector('.registratsiya_top textarea'),
    registratsiya_title = document.querySelector('.registratsiya_title'),
    registratsiya_button = document.querySelector('.registratsiya_button button'),
    registratsiya_delete = document.querySelector('.registratsiya_delete');
edit.forEach((item, index) => {
    item.addEventListener('click', () => {
        modal_name.value = name[index].innerText
        modal_surname.value = surname[index].innerText
        modal_textarea.value = teacher_information[index].innerText
        registratsiya_delete.classList.remove('non_active')
        registratsiya_delete.href = `/delete_worker/${item.dataset.worker_id}`
        registratsiya.style.display = "flex"
        registratsiya_left_img.style.backgroundImage = `url(${teacher_img[index].src})`
        modal_job.forEach(item => {
            if (item.innerText === job[index].innerText) {
                item.classList.add('active_option')
            }
        })
        registratsiya_block.action = `/edit_worker/${item.dataset.worker_id}`
        registratsiya_title.innerText = "MA'LUMOT O'ZGARTIRISH"
        registratsiya_button.innerText = "Change"
    })
})
teacher_circle.addEventListener('click', () => {
    registratsiya.style.display = "flex"
    registratsiya_block.action = `/workers`
    registratsiya_delete.classList.add('non_active')
    modal_name.value = ""
    modal_surname.value = ""
    modal_textarea.value = ""
    registratsiya_left_img.style.backgroundImage = ""
    modal_job.forEach(item => {
        item.classList.remove('active_option')
    })
    registratsiya_title.innerText = "MA'LUMOT QO'SHISH"
    registratsiya_button.innerText = "Add"

})
registratsiya_close.addEventListener('click', () => {
    registratsiya.style.display = "none"
})
registratsiya_left.addEventListener('click', () => {
    registratsiya_file.click()
})
registratsiya_file.addEventListener('change', () => {
    const [file] = registratsiya_file.files
    if (file) {
        registratsiya_left_img.style.backgroundImage = `url(${URL.createObjectURL(file)})`
    }
})

