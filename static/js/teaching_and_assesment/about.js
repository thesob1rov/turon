let teach_btn = document.querySelectorAll('.teach_btn'),
    teach_container = document.querySelector(".teach_container"),
    teach_overlay = document.querySelector('.teach_overlay'),
    teach_overlay_box = document.querySelector('.teach_overlay_box'),
    teach_box = document.querySelectorAll('.teach_box'),
    ellipsis = document.querySelectorAll('.teach_icon'),
    circle = document.querySelector('.circle'),
    lear_more = document.querySelectorAll('.lear_more'),
    title = document.querySelectorAll('.title'),
    info_img = document.querySelectorAll('.info_img'),
    content = document.querySelectorAll('.content'),
    contentModal = document.querySelector('.teach_information'),
    titleModal = document.querySelector('.head'),
    imgModal = document.querySelector('.img'),
    information = document.querySelector('.information'),
    change_btn = document.querySelectorAll('.change_btn'),
    information2 = document.querySelector('.information2'),
    change_title_inp = document.querySelector('.change_title_inp'),
    change_content_inp = document.querySelector('.change_content_inp'),
    change_form = document.querySelector('.change_form'),
    box_change = document.querySelectorAll('.box_change');

teach_btn.forEach(item => {
    item.addEventListener('click', () => {
        teach_overlay.style.display = "flex"
    })
})
let indexCount;
ellipsis.forEach((item, index) => {
    item.addEventListener('click', () => {
        console.log(box_change[index].style.display.name)
        let style = window.getComputedStyle(box_change[index], false),
            url = style.display;
        if (url === "flex") {
            box_change[index].style.display = "none"
        } else {
            box_change[index].style.display = "flex"
        }
    })
})
circle.addEventListener('click', () => {
    information.style.display = "flex"
})
information.addEventListener("click", (e) => {
    if (e.target === information) {
        information.style.display = "none"
    }
})
teach_overlay.addEventListener("click", (e) => {
    if (e.target === teach_overlay) {
        teach_overlay.style.display = "none"
    }
})


lear_more.forEach((more, index) => {
    more.addEventListener("click", () => {
        titleModal.innerText = title[index].innerText
        contentModal.innerText = content[index].innerText
        imgModal.style.background = `url(${info_img[index].src})`
    })
})


// teach_btn.forEach(item => {
//     item.addEventListener('click', (event) => {
//         if(event.target === teach_overlay){
//             teach_overlay.style.display = "flex"
//             teach_container.style.opacity = "0"
//         }
//         teach_overlay.style.display = "none"
//     })
// })

change_btn.forEach((item, index) => {
    item.addEventListener("click", () => {
        information2.style.display = "flex"
        change_title_inp.value = title[index].innerText
        change_content_inp.value = content[index].innerText
        change_form.action = `edit_teach_asses/${item.dataset.id}`
    })
})

information2.addEventListener("click", (e) => {
    if (e.target === information2){
        information2.style.display = "none"
    }
})