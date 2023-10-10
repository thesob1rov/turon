let circle = document.querySelector(".vakansiya_circle"),
    modal = document.querySelector(".registratsiya"),
    registratsiya_block = document.querySelector('.registratsiya_block'),
    edit = document.querySelectorAll('.edit'),
    registratsiya_delete = document.querySelector('.registratsiya_delete'),
    registratsiya_left = document.querySelector('.registratsiya_left'),
    select_modal = document.querySelectorAll('.registratsiya_top .jobs'),
    textArea_modal = document.querySelector('.registratsiya_top textarea'),
    job_title = document.querySelectorAll('.job_title'),
    vacation_text = document.querySelectorAll('.vacation_text'),
    registratsiya_title = document.querySelector('.registratsiya_title'),
    registratsiya_button = document.querySelector('.registratsiya_button button'),
    close_modal = document.querySelector(".registratsiya_close");
registratsiya_left.style.display = "none"
circle.addEventListener("click", () => {
    modal.style.display = "flex"
    registratsiya_block.action = '/vacation'
    registratsiya_delete.classList.add('non_active')
    select_modal.forEach(item => {
        item.classList.remove('active_option')
    })
    textArea_modal.value = ''
    registratsiya_title.innerText = "MA'LUMOT QO'SHISH"
    registratsiya_button.innerText = "Add"
})
close_modal.addEventListener("click", () => {
    modal.style.display = "none"
})
edit.forEach((item, index) => {
    item.addEventListener('click', () => {
        modal.style.display = "flex"
        registratsiya_delete.classList.remove('non_active')
        registratsiya_delete.href = `/delete_vacation/${item.dataset.vacation_id}`
        registratsiya_block.action = `/edit_vacation/${item.dataset.vacation_id}`
        console.log(registratsiya_block.action)
        textArea_modal.value = vacation_text[index].innerText;
        select_modal.forEach(item => {
            if (item.innerText === job_title[index].innerText) {
                item.classList.add('active_option')
            }
        })
        registratsiya_title.innerText = "MA'LUMOT O'ZGARTIRISH"
        registratsiya_button.innerText = "Change"
    })
})