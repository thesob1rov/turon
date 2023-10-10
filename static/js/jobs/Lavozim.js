
let box_img = document.querySelectorAll('.img'),
    img_edit = document.querySelectorAll('.edit_icon'),
    title = document.querySelectorAll('.big_box_icon h1'),
    job_img = document.querySelectorAll('.big_box_icon img'),
    job_text = document.querySelectorAll('.inner_text p'),
    text = document.querySelectorAll('.inner_text'),
    circle = document.querySelector('.circle'),
    registratsiya = document.querySelector('.registratsiya'),
    registratsiya_left_img = document.querySelector('.registratsiya_left_img'),
    registratsiya_left = document.querySelector('.registratsiya_left'),
    registratsiya_file = document.querySelector('.registratsiya_file'),
    registratsiya_block = document.querySelector('.registratsiya_block'),
    registratsiya_title = document.querySelector('.registratsiya_title'),
    registratsiya_button = document.querySelector('.registratsiya_button button'),
    registratsiya_delete = document.querySelector('.registratsiya_button a'),
    registratsiya_close = document.querySelector('.registratsiya_close'),
    modal_input = document.querySelector('.registratsiya_top input'),
    modal_textarea = document.querySelector('.registratsiya_top textarea'),
    big = document.querySelectorAll('.big_box');

box_img.forEach((item, index) => {
        item.addEventListener('click', () => {
            box_img[index].classList.toggle('rotate')
            console.log(text[index].style.height)
            text[index].style.height = +text[index].getBoundingClientRect().height === 0 ? text[index].scrollHeight - 10 + "px" : 0 + "px"
        })
    }
)
img_edit.forEach((item, index) => {
    item.addEventListener('click', () => {
        registratsiya.classList.add('register_active')
        registratsiya_title.innerText = "MA'LUMOT O'ZGARTIRISH"
        registratsiya_block.action = `/edit_info/${job_img[index].dataset.info_id}`
        registratsiya_left_img.style.backgroundImage = `url(${job_img[index].src})`
        modal_input.value = title[index].innerText
        modal_textarea.value = job_text[index].innerText
        registratsiya_button.innerText = "Change"
        registratsiya_delete.classList.remove('non_active')
        registratsiya_delete.href = `/delete_info/${job_img[index].dataset.info_id}`

    })
})

circle.addEventListener('click', () => {
    registratsiya.classList.add('register_active')
    registratsiya_title.innerText = "MA'LUMOT QO'SHISH"
    registratsiya_left_img.style.backgroundImage = ""
    modal_input.value = ""
    modal_textarea.value = ""
    registratsiya_block.action = `/infos/${circle.dataset.type_id}`
    registratsiya_button.innerText = "Add"
    registratsiya_delete.classList.add('non_active')
})
registratsiya_close.addEventListener('click', () => {
    registratsiya.classList.remove('register_active')
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

