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
        info = {
            student_id: item.dataset.id,
            flow_id: item.dataset.flow_id
        }
        const sure = confirm("Siz bu studentni ochirmoqchimisz?")
        console.log(info.delete_type)
        if (sure) {
            fetch("/delete_student_in_flow", {
                method: "POST", body: JSON.stringify({
                    "info": info
                }), headers: {
                    'Content-type': 'application/json'
                }
            })
        }
        console.log(info)
    })
})
change_overlay.addEventListener('click', (event) => {
    if (event.target === change_overlay) {
        change_overlay.style.display = "none"
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

let info_flow = {}
check.forEach(item => {
    item.addEventListener('change', () => {
        if (item.checked) {
            info_flow = {
                students: students
            }
            students.push(item.dataset.id)
        }
    })
})

radio_class.forEach(item => {
    item.addEventListener('change', () => {
        if (item.checked) {
            const new_info_flow = {
                ...info_flow,
                flow_id: item.dataset.id,
                old_flow_id: send_class.dataset.id
            }
            info_flow = new_info_flow
        }
    })
})

send_class.addEventListener('click', () => {
    console.log(info_flow)
    add.style.display = "none"
    fetch("/transfer_students_in_flow", {
        method: "POST", body: JSON.stringify({
            "info_flow": info_flow
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

    const info_del_flow = {
        flow_id: delete_class.dataset.id,
    }
    fetch("/delete_flow", {
        method: "POST", body: JSON.stringify({
            "info": info_del_flow
        }), headers: {
            'Content-type': 'application/json'
        }
    })
    window.location.replace(
        "/flows",
    );
})


