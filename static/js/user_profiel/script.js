let menu = document.querySelector('.ellipsis'), box_menu = document.querySelector('.change');
menu.addEventListener('click', () => {
    if (box_menu.style.display === "none") {
        box_menu.style.display = "flex"
    } else {
        box_menu.style.display = "none"
    }
})