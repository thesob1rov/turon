let select = document.querySelector('.select'),
    wednesday = document.querySelector('.wednesday'),
    monday = document.querySelector('.monday'),
    friday = document.querySelector('.friday'),
    thursday = document.querySelector('.thursday'),
    tuesday = document.querySelector('.tuesday'),
    main_table = document.querySelectorAll('.main_table');


function start() {
    console.log(main_table)
    main_table[0].classList.add("active_table")
}

start()

function remove() {
    main_table.forEach(item => {
        item.classList.remove("active_table")
    })
}

select.addEventListener("change", () => {
    main_table.forEach(item => {
        if (select.value === item.classList[1]) {
            remove()
            item.classList.add("active_table")
        }
    })
})
