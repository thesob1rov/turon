let btn = document.querySelector('.btn'), create = document.querySelector('.create'), x = document.querySelector('.x'),
    filter_btn = document.querySelector('.filter_btn'), double = document.querySelector('.double'),
    filter = document.querySelector('.filter'),
    add_btn = document.querySelector('.add_btn'), add = document.querySelector('.add'),
    next = document.querySelector('.next'),
    form_filter = document.querySelector('.form_filter'),
    class_number = document.querySelector('.class_number');


btn.addEventListener('click', () => {
    create.classList.add('active')
})
x.addEventListener('click', () => {
    create.classList.remove('active')
})
create.addEventListener('click', (event) => {
    if (event.target === create) {
        create.classList.remove('active')
    }
    add.style.display = "none"
})

filter_btn.addEventListener('click', () => {


    if (double.style.display === "none") {
        double.style.display = "flex"
        filter.classList.remove('active_filter')
    } else {
        double.style.display = "none"
        filter.classList.add('active_filter')
    }

})

// add_btn.addEventListener('click', () => {
//     create.classList.remove('active')
//     if (next.style.display === "none") {
//         next.style.display = "flex"
//         add.classList.remove('active_add')
//     } else {
//         next.style.display = "none"
//         add.classList.add('active_add')
//     }
// })


add_btn.addEventListener('click', () => {
    if (add.style.display === "flex") {
        next.style.display = "flex"
        add.style.display = "none"
    } else {
        next.style.display = "none"
        add.style.display = "flex"
    }
})