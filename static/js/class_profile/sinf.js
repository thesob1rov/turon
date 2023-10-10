let i = document.querySelector('.icon_img_i'), btn = document.querySelector('.btn'),
    x = document.querySelectorAll('.x i'), delete_btn = document.querySelector('.delete_btn'),
    exchange = document.querySelector('.exchange'), check = document.querySelectorAll('.check input'),
    move_btn = document.querySelector('.move'),
    add = document.querySelector('.add_background'),
    change = document.querySelector('.change'), change_overlay = document.querySelector('.change_overlay'),
    radio_class = document.querySelectorAll('.radio'),
    ellipsis = document.querySelector('.ellipsis_overlay'),
    change_btn = document.querySelector('.change_btn');

i.addEventListener('click', () => {
    ellipsis.classList.toggle('active_ellipsis')
    // ellipsis.style.display = "flex"
})
change_btn.addEventListener('click', () => {
    change.classList.toggle('active_edit')
})

window.addEventListener("click", (event) => {
    if (ellipsis.style.display === "flex") {
        if (event.target !== window) {
            ellipsis.style.display = "none"
        }
    }

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
    if (e.target === change) {
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
    move_btn.style.display = "initial"
})


let delete_type = document.querySelector('.delete_type'), reason = document.querySelector('.reason'),
    change_overlay_btn = document.querySelector('.change_overlay_btn');
let info = {}

x.forEach(item => {
    item.addEventListener("click", () => {
        change_overlay.style.display = "flex"
        info = {
            student_id: item.dataset.id,
            class_id: item.dataset.class_id
        }
        console.log(info)
    })
})
change_overlay.addEventListener('click', (event) => {
    if (event.target === change_overlay) {
        change_overlay.style.display = "none"
    }
})

change_overlay_btn.addEventListener("click", () => {
    change_overlay.style.display = "none"
    const sure = confirm("Siz bu studentni ochirmoqchimisz?")
    console.log(info.delete_type)
    const new_info = {
        ...info,

        delete_type: delete_type.value,
        reason: reason.value
    }
    info = new_info
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

move_btn.addEventListener('click', () => {
    add.style.display = "flex"
})

add.addEventListener('click', (event) => {
    if (event.target === add) {
        add.style.display = "none"
    }
})
const send_class = document.querySelector('.send_class');


let students = []

let info_class = {}
check.forEach(item => {
    item.addEventListener('change', () => {
        if (item.checked) {
            info_class = {
                students: students
            }
            students.push(item.dataset.id)
        }
    })
})

radio_class.forEach(item => {
    item.addEventListener('change', () => {
        if (item.checked) {
            const new_info_class = {
                ...info_class,
                class_id: item.dataset.id
            }
            info_class = new_info_class
        }
    })
})

send_class.addEventListener('click', () => {
    add.style.display = "none"
    fetch("/transfer_students_in_class", {
        method: "POST", body: JSON.stringify({
            "info_class": info_class
        }), headers: {
            'Content-type': 'application/json'
        }
    })
})


let delete_menu_class = document.querySelector('.delete_btn_class'),
    delete_class = document.querySelector('.delete_class'),
    delete_type_class = document.querySelector('.change_overlay2_box select'),
    reason_class = document.querySelector('.reason_class'),
    change_overlay2 = document.querySelector('.change_overlay2');


delete_menu_class.addEventListener('click', () => {
    change_overlay2.style.display = "flex"
})


change_overlay2.addEventListener('click', (event) => {
    if (event.target === change_overlay2) {
        change_overlay2.style.display = "none"
    }
})

delete_class.addEventListener("click", () => {
    change_overlay2.style.display = "none"
    const info_del_class = {
        class_id: delete_class.dataset.id,
        delete_type: delete_type_class.value,
        reason: reason_class.value
    }


    fetch("/delete_class", {
        method: "POST", body: JSON.stringify({
            "info": info_del_class
        }), headers: {
            'Content-type': 'application/json'
        }
    })
    window.location.replace(
        "/classes",
    );
})