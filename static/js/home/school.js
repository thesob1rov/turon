let menu = document.querySelector('.menu'), menu_icon = document.querySelector('.menu_icon');

menu_icon.addEventListener('click', () => {
    menu.style.top = "-60rem"
})
menu_icon.addEventListener('click', () => {
    menu.classList.toggle('menu_active')
    if (menu_icon.className === "fa-solid fa-xmark icon") {
        menu_icon.className = "fa-solid fa-bars icon"
    } else {
        menu_icon.className = "fa-solid fa-xmark icon"
        menu.style.top = "8rem"
    }
})
