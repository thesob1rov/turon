let i = document.querySelector('.icon_img_i'), btn = document.querySelector('.btn'),
    x = document.querySelectorAll('.x i'), delete_btn = document.querySelector('.delete_btn'),
    exchange = document.querySelector('.exchange'), check = document.querySelectorAll('.check i'),
    change = document.querySelector('.change');

i.addEventListener('click', () => {
    change.classList.add('active')
})


console.log(x)
delete_btn.addEventListener('click', () => {
    x.forEach(item => {
        if (item.style.display === "flex") {
            item.style.display = "none"
        } else {
            item.style.display = "flex"
        }
    })

})
exchange.addEventListener('click', () => {

    check.forEach(item => {
        if (item.style.display === "flex") {
            item.style.display = "none"
        } else {
            item.style.display = "flex"
        }
    })

})