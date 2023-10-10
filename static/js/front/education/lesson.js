let title = document.querySelectorAll('.lessons_lesson_title'), box = document.querySelectorAll('.lessons_lesson'),
    information = document.querySelectorAll('.lessons_information');


box.forEach((item, index) => {
    item.addEventListener('mouseenter', () => {
        information[index].classList.add('active')
    })
})
box.forEach((item, index) => {
    item.addEventListener('mouseleave', () => {
        information[index].classList.remove('active')
    })
})
title.forEach((item, index) => {
    item.addEventListener('click', () => {
        information[index].classList.add('active')
    })

})
let icon = document.querySelectorAll('.icon'),
    x = document.querySelectorAll('.x'),
    box2 = document.querySelectorAll('.certificats_information');

icon.forEach((item,index) => {
    item.addEventListener('click', () => {
        box2[index].classList.add('active')
    })
})
x.forEach((x_mark,index)=>{
    x_mark.addEventListener('click',()=>{
        box2[index].classList.remove('active')
    })
})
var splide = new Splide('.splide', {
    type: 'loop', focus: "center", // padding: '5rem',
    // perPage: 3,
    breakpoints: {
        1024: {
            perPage: 5,

        }, 767: {
            perPage: 2,

        }, 640: {
            perPage: 1,

        }, 576: {
            perPage: 1
        }
    },
});

splide.mount();