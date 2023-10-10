let btn = document.querySelector('.btn'), create = document.querySelector('.create'), x = document.querySelector('.x'),
    filter_btn = document.querySelector('.filter_btn'), double = document.querySelector('.double'),
    filter = document.querySelector('.filter')
add_btn = document.querySelector('.add_btn'), add = document.querySelector('.add'), next = document.querySelector('.next'),
    create_bnt = document.querySelector('.create_bnt');

btn.addEventListener('click', () => {
    create.classList.add('create_active')
    // add.style.display = "none"
    // next.style.display = "flex"
})
create_bnt.addEventListener('click', () => {
    create.classList.remove('create_active')
    // add.style.display = "none"
    // next.style.display = "flex"
})
x.addEventListener('click', () => {
    create.classList.remove('create_active')
})
create.addEventListener('click', (event) => {
    if (event.target === create) {
        create.classList.remove('create_active')
    }
    add.style.display = "none"
})


filter_btn.addEventListener('click', () => {
    if (double.style.display === "none") {
        double.style.display = "flex"
        filter.style.display = "none"
    } else {
        double.style.display = "none"
        filter.style.display = "flex"
    }
})


add_btn.addEventListener('click', () => {
    if (add.style.display === "flex") {
        // next.style.display = "flex"
        add.style.display = "none"
    } else {
        // next.style.display = "none"
        add.style.display = "flex"
    }
})