let teacher = document.querySelector('#teacher_list'), subject = document.querySelector('#subject_list'),
    teacher_btn = document.querySelector('#teacher'), subject_btn = document.querySelector('#subject'),
    room = document.querySelector('#room_list')
room_btn = document.querySelector('#room');

teacher_btn.addEventListener('click', () => {
    teacher.classList.add('active_var')
    subject.classList.remove('active_var')
    room.classList.remove('active_var')
    teacher_btn.style.background = " #111f4c"
    subject_btn.style.background = " #adadad"
    room_btn.style.background = " #adadad"

})
subject_btn.addEventListener('click', () => {
    subject.classList.add('active_var')
    teacher.classList.remove('active_var')
    room.classList.remove('active_var')
    subject_btn.style.background = " #111f4c"
    teacher_btn.style.background = " #adadad"
    room_btn.style.background = " #adadad"
})

room_btn.addEventListener('click', () => {
    room.classList.add('active_var')
    teacher.classList.remove('active_var')
    subject.classList.remove('active_var')
    room_btn.style.background = " #111f4c"
    subject_btn.style.background = " #adadad"
    teacher_btn.style.background = " #adadad"
})


const class_number = document.querySelectorAll('.fan'),
    container_direction = document.querySelectorAll('.container_direction');

function startTable() {
    class_number[0].classList.toggle("active_class")
    container_direction[0].classList.toggle("active_table")
}

startTable()
class_number.forEach((classs, index) => {
    classs.addEventListener("click", () => {
        classs.classList.toggle("active_class")
        container_direction[index].classList.toggle("active_table")
    })
})

let subjects = document.querySelectorAll(".subjects"), subject_container = document.querySelector(".subject_container"),
    teachers = document.querySelectorAll('.teachers'), rooms = document.querySelectorAll('.rooms');

const drop = document.querySelectorAll(".zone-1");


let draggedElem, roomId, subjectId, teacherId, isDropped, currentElem


function createBox() {

    const box = document.querySelectorAll(".time_subject")
    box.forEach(item => {
        item.addEventListener("dragstart", dragStart)
    })
}

function removeBoxes() {
    const box = document.querySelectorAll(".time_subject")


    box.forEach(item => {
        item.removeEventListener("dragstart", dragStart)
    })


}

function dragStart() {
    roomId = this.getAttribute("data-roomId")
    teacherId = this.getAttribute("data-teacherId")
    subjectId = this.getAttribute("data-subjectId")
    isDropped = this.getAttribute("data-isDropped")
    draggedElem = this.cloneNode(true)

    if (isDropped === "true") {
        currentElem = this
    }

    window.addEventListener('drop', handleDrop);

}


window.addEventListener("dragover", (e) => {
    event.preventDefault()
})


function handleDrop(ev) {
    ev.preventDefault();

    window.removeEventListener('drop', handleDrop);

    if (!ev.target.classList.contains("drop") && isDropped === "true" && !ev.target.classList.contains("time_subject")) {


        if (roomId) currentElem.parentElement.removeAttribute("data-roomId")
        if (subjectId) currentElem.parentElement.removeAttribute("data-subjectId")
        if (teacherId) currentElem.parentElement.removeAttribute("data-teacherId")

        let removedElement
        let removedBox
        let removedText
        let removedDay
        removedElement = currentElem.getAttribute("data-lessonId")
        if (currentElem.getAttribute("data-subjectId")) {
            removedBox = currentElem.getAttribute("data-subjectId")
            removedText = "subject"
        }
        if (currentElem.getAttribute("data-teacherId")) {
            removedBox = currentElem.getAttribute("data-teacherId")
            removedText = "teacher"
        }
        if (currentElem.getAttribute("data-roomId")) {
            removedBox = currentElem.getAttribute("data-roomId")
            removedText = "room"
        }
        if (currentElem.parentElement.getAttribute("data-dayId")) {
            removedDay = currentElem.parentElement.getAttribute("data-dayId")
        }
        let info = {
            lesson_id: removedElement,
            item: removedBox,
            text: removedText,
            time_table_day_id: removedDay
        }
        fetch('/delete_item_in_lesson', {
            method: "POST", body: JSON.stringify({
                "info": info
            }), headers: {
                'Content-type': 'application/json'
            }
        })
        console.log(info)
        currentElem.remove()
        isDropped = null
        currentElem = null
    }


}

createBox()


drop.forEach(item => {
    item.addEventListener("dragover", (e) => {
        event.preventDefault()
    })
})


drop.forEach(item => {
    item.addEventListener("drop", () => {

        const itemRoomId = item.getAttribute("data-roomId")
        const itemSubjectId = item.getAttribute("data-subjectId")
        const itemTeacherId = item.getAttribute("data-teacherId")

        const isRoom = roomId ? itemRoomId !== roomId && !itemRoomId : null
        const isSubject = subjectId ? itemSubjectId !== subjectId && !itemSubjectId : null
        const isTeacher = teacherId ? itemTeacherId !== teacherId && !itemTeacherId : null

        removeBoxes()
        if (isRoom || isSubject || isTeacher) {
            const elem = draggedElem
            elem.setAttribute("data-isDropped", true)

            item.append(elem)

            const elements = item.querySelectorAll(".time_subject")
            sortElement(elements, item)

            if (roomId) item.setAttribute(`data-roomId`, roomId)
            if (subjectId) item.setAttribute(`data-subjectId`, subjectId)
            if (teacherId) item.setAttribute(`data-teacherId`, teacherId)

        }
        roomId = null
        subjectId = null
        teacherId = null
        draggedElem = null
        createBox()
        postTimetable(item)
    })
})

const sortAndMap = (arr = []) => {
    const copy = arr.slice();
    const sorter = (a, b) => {
        return a['index'] - b['index'];
    };
    copy.sort(sorter);
    const res = copy.map(({item, index}) => {
        return item;
    });
    return res;
};


function sortElement(list, elem) {

    let indexes = []

    indexes = Array.prototype.slice.call(list).map(item => {
        const itemRoomId = item.getAttribute("data-roomId")
        const itemSubjectId = item.getAttribute("data-subjectId")
        const itemTeacherId = item.getAttribute("data-teacherId")

        if (itemRoomId) {
            return {
                item, index: 0
            }
        }
        if (itemSubjectId) {
            return {
                item, index: 1
            }
        }
        if (itemTeacherId) {
            return {
                item, index: 2
            }
        }

    })
    elem.innerHTML = ""
    sortAndMap(indexes).map(item => {
        elem.append(item)
    })

}

function postTimetable(item) {


    const room_id = item.getAttribute("data-roomId")
    const subject_id = item.getAttribute("data-subjectId")
    const teacher_id = item.getAttribute("data-teacherId")
    const class_id = item.getAttribute("data-classId")
    const day_id = item.getAttribute("data-dayId")
    const lesson_time = item.getAttribute("data-timeId")

    if (room_id && subject_id && teacher_id) {
        console.log("true")

        let info = {
            class_id,
            day_id,
            room_id,
            subject_id,
            teacher_id,
            lesson_time,
        }
        if (item.getAttribute("data-lessonId")) {
            let lesson_id = item.getAttribute("data-lessonId")
            info.lesson_id = lesson_id
        } else {
            info.lesson_id = ""
        }
        console.log(info)
        fetch('/creat_table', {
            method: "POST", body: JSON.stringify({
                "info": info
            }), headers: {
                'Content-type': 'application/json'
            }
        })
            .then(function (response) {
                return response.json()
            })
            .then(function (res) {
                console.log(res["status"])
                if (res) {
                    const message = document.querySelector('.message ')
                    const messageText = document.querySelector('.message h4')
                    message.classList.add("active_message")
                    messageText.style.color = res["status"]["color"]
                    messageText.innerText = res["status"]["text"]
                    message.style.boxShadow = `0 0 10px 3px ${res["status"]["color"]}`
                }
                const message = document.querySelector('.message ')
                setTimeout(function () {
                    message.classList.remove("active_message")
                }, 4000)
            })
    }
}

