let i = document.querySelector('.icon_img_i'), btn = document.querySelector('.btn'),
    x = document.querySelectorAll('.x i'), delete_btn = document.querySelector('.delete_btn'),
    exchange = document.querySelector('.exchange'), check = document.querySelectorAll('.check i'),
    change = document.querySelector('.change');

i.addEventListener('click', () => {
    change.classList.add('active_edit')
})

delete_btn.addEventListener('click', () => {
    x.forEach(item => {
        if (item.style.display === "flex") {
            item.style.display = "none"
            console.log('kjbn')
        } else {
            item.style.display = "flex"
            clearActiveCheck()
        }
    })
})


change.addEventListener('click', (e) => {
    if (e.target === change){
        change.classList.remove('active_edit')
    }
})


function clearActiveCheck() {
    check.forEach(checked => {
        checked.style.display = "none"
    })

}

function clearActiveX() {
    x.forEach(x => {
        x.style.display = "none"
    })

}

exchange.addEventListener('click', () => {
    check.forEach(checked => {
        if (checked.style.display === "flex") {
            checked.style.display = "none"
            console.log("kjbkj")
        } else {
            checked.style.display = "flex"
            clearActiveX()
        }
    })
})

x.forEach(item => {
    item.addEventListener("click", () => {
        console.log("ds")
        const sure = confirm("Siz bu studentni ochirmoqchimisz?")
        const info = {
            student_id: item.dataset.id,
            class_id: item.dataset.class_id
        }
        console.log(info)
        if (sure) {
            fetch("/delete_student_in_class", {
                method: "POST", body: JSON.stringify({
                    "info": info
                }), headers: {
                    'Content-type': 'application/json'
                }
            })
        }
    })
})
