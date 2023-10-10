let big_edit = document.querySelector('.big_edit'),
    registratsiya = document.querySelector('.registratsiya'),
    circle = document.querySelector('.circle'),
    big_mini1_box_img = document.querySelector('.big_mini1_box_img'),
    big_mini1_text = document.querySelector('.big_mini1_text'),
    big_mini_active = document.querySelector('.li_active'),
    registratsiya_left_img = document.querySelector('.registratsiya_left_img'),
    registratsiya_left = document.querySelector('.registratsiya_left'),
    registratsiya_file = document.querySelector('.registratsiya_file'),
    registratsiya_block = document.querySelector('.registratsiya_block'),
    registratsiya_title = document.querySelector('.registratsiya_title'),
    modal_input = document.querySelector('.registratsiya_top input'),
    modal_textarea = document.querySelector('.registratsiya_top textarea'),
    registratsiya_button = document.querySelector('.registratsiya_button button'),
    registratsiya_delete = document.querySelector('.registratsiya_button a'),
    menu_item = document.querySelectorAll('.big_mini_list_li li'),
    registratsiya_close = document.querySelector('.registratsiya_close');
registratsiya_left.addEventListener('click', () => {
    registratsiya_file.click()
})
registratsiya_file.addEventListener('change', () => {
    const [file] = registratsiya_file.files
    if (file) {
        registratsiya_left_img.style.backgroundImage = `url(${URL.createObjectURL(file)})`
    }
})
if (big_edit) {
    big_edit.addEventListener('click', () => {
        registratsiya.classList.add('big_active')
        registratsiya_title.innerText = "MA'LUMOT O'ZGARTIRISH"
        registratsiya_block.action = `/edit_info/${big_mini_active.dataset.info_id}`
        registratsiya_left_img.style.backgroundImage = `url(${big_mini1_box_img.src})`
        modal_input.value = big_mini_active.innerText
        modal_textarea.value = big_mini1_text.innerText
        registratsiya_button.innerText = "Change"
        registratsiya_delete.classList.remove('non_active')

    })
}
registratsiya_close.addEventListener('click', () => {
    registratsiya.classList.remove('big_active')
})
if (circle) {
    circle.addEventListener('click', () => {
        registratsiya.classList.add('big_active')
        registratsiya_title.innerText = "MA'LUMOT QO'SHISH"
        registratsiya_left_img.style.backgroundImage = ""
        modal_input.value = ""
        modal_textarea.value = ""
        if (big_mini_active){
            registratsiya_block.action = `/get_about_profile/${circle.dataset.type_id}/${big_mini_active.dataset.info_id}`
        }

        registratsiya_button.innerText = "Add"
        if (registratsiya_delete){
            registratsiya_delete.classList.add('non_active')
        }

    })
}
var splide = new Splide('.splide', {
    type: 'loop', focus: "center", // padding: '5rem',
    // perPage: 3,
    breakpoints: {
        1024: {
            perPage: 5,

        }, 768: {
            perPage: 2,

        }, 640: {
            perPage: 1,

        }, 576: {
            perPage: 1
        }
    },
});

splide.mount();