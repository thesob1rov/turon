let button = document.querySelectorAll('.click'),
    click = document.querySelector('.box_click'),
    back = document.querySelector('.ariza_backround'),
    ariza_form = document.querySelector('.ariza_text'),
    request_pdf = document.querySelector('.request_pdf'),
    pdf_file = document.querySelector('.pdf_file'),
    pdf_icon = document.querySelector('.pdf_icon'),
    main = document.querySelector('.ariza');
button.forEach((item, index) => {
    item.addEventListener('click', () => {
        main.classList.add('active')
        ariza_form.action = `/send_request/${item.dataset.vacation_id}`

    })
})
click.addEventListener('click', () => {
    main.classList.remove('active')


})
main.addEventListener('click', (event) => {
    if (event.target === main) {
        main.classList.remove('active')
    }
})
request_pdf.addEventListener('click', () => {
    pdf_file.click()
})
pdf_file.addEventListener('change', () => {
    if (!pdf_file.value) {
        pdf_icon.className = "fa-solid fa-x"
    }else {
        pdf_icon.className = "fa-solid fa-check"
    }
})