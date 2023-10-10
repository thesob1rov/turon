let hamburger = document.querySelector('.hamburger'),
    page = document.querySelector('.x'),
    section_block = document.querySelector('.section_block'),
    all = document.querySelector('.home'),
    icon = document.querySelectorAll('.fa-chevron-right'),
    box = document.querySelectorAll('.box_mini');


hamburger.addEventListener('click', () => {

    page.style.display = 'flex'
    hamburger.style.display = 'none'
    all.classList.toggle('active')
    section_block.classList.toggle('block_active')

})
page.addEventListener('click', () => {
    hamburger.style.display = 'flex'
    page.style.display = 'none'
    all.classList.toggle('active')
    section_block.classList.toggle('block_active')
})

// icon.forEach((item,index) => {
//         item.addEventListener('click', () => {
//             box[index].classList.toggle('active_inside')
//         })
//     }
// )