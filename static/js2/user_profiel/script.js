let icon = document.querySelector('.ellipsis'),
    box = document.querySelector('.change');
icon.addEventListener('click', () => {
    if (box.style.display === "none") {
        box.style.display = "flex"
    } else {
        box.style.display = "none"
    }

})