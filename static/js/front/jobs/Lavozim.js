let box = document.querySelectorAll('.img'),
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

box.forEach((item, index) => {
        item.addEventListener('click', () => {
            box[index].classList.toggle('rotate')
            console.log(text[index].style.height)
            text[index].style.height = +text[index].getBoundingClientRect().height === 0 ? text[index].scrollHeight - 10 + "px" : 0 + "px"
        })
    }
)