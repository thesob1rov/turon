let room_box = document.querySelector('.overlay'), add_btn = document.querySelector('.room_btn'),
    x = document.querySelector('.x_mark'), name = document.querySelector('.room_name'),
    count = document.querySelector('.count'), teacher_id = document.querySelector('.teacher_id'),
    overlay_add = document.querySelector('.overlay_add');

add_btn.addEventListener('click', () => {
    room_box.classList.add('active_overlay')
})

room_box.addEventListener('click', (event) => {
    if (event.target === room_box) {
        room_box.classList.remove('active_overlay')
    }
})
x.addEventListener('click', () => {
    room_box.classList.remove('active_overlay')
})
