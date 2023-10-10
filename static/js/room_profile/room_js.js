let icon_menu_room = document.querySelector('.room_icon'),
    box_room = document.querySelector('.box_change'),
    overlay_room = document.querySelector('.overlay_room'),
    x = document.querySelector('#x'),
    delete_box = document.querySelector('.delete'),
    trash = document.querySelector('#trash'),
    no = document.querySelector('#no'),
    change = document.querySelector('#change');


icon_menu_room.addEventListener('click', () => {
    box_room.classList.toggle("change_active")
})
change.addEventListener('click', () => {
    overlay_room.classList.add('change_active')
})

x.addEventListener('click', () => {
    overlay_room.classList.remove('change_active')
})

trash.addEventListener('click', () => {
    delete_box.classList.add('delete_active')
})

no.addEventListener('click', () => {
    delete_box.classList.remove('delete_active')
})

delete_box.addEventListener('click', (event) => {
    if (event.target === delete_box) {
        delete_box.classList.remove('delete_active')
    }
})

overlay_room.addEventListener('click', (event) => {
    if (event.target === overlay_room) {
        overlay_room.classList.remove('change_active')
    }
})