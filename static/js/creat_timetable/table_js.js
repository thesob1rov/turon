let teacher = document.querySelector('#teacher_list'), subject = document.querySelector('#subject_list'),
    teacher_btn = document.querySelector('#teacher'), subject_btn = document.querySelector('#subject'),
    room = document.querySelector('#room_list'), table = document.querySelector('.table'),
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
    container_direction = document.querySelectorAll('.container_direction'),
    main_container = document.querySelector('.main_container');

function startTable() {
    class_number[0].classList.toggle("active_class")
    container_direction[0].classList.toggle("active_table")
}

startTable()

class_number.forEach((classs, index) => {
    classs.addEventListener("click", () => {
        if (index !== 0) {
            classs.classList.toggle("active_class")
        }
        const new_container_direction = document.querySelectorAll('.container_direction');
        if (classs.dataset.active === "true" && classs.classList.value === "fan") {
            console.log("uje yoqilgan")
            new_container_direction.forEach(item => {
                if (item.dataset.contid === `${index}`) {
                    console.log('aa')
                    item.remove()
                }
            })
            // new_container_direction[index].remove()
        } else {
            if (index !== 0) {
                classs.setAttribute("data-active", "true")
                fetch(`/get_time_table`, {
                    method: "POST", body: JSON.stringify({
                        "class_id": classs.dataset.id
                    }), headers: {
                        'Content-type': 'application/json'
                    }
                })
                    .then(function (response) {
                        return response.json()
                    })
                    .then(function (res) {
                        console.log(res)
                        const container_direction = document.createElement("div")
                        container_direction.classList.add("container_direction")
                        container_direction.getAttribute("data-contId")
                        container_direction.setAttribute("data-contId", index)
                        const time_two = document.createElement("div")
                        time_two.classList.add("time_two")
                        const time_table = document.createElement("div")
                        time_table.classList.add("time_table")
                        const table = document.createElement("table")
                        table.classList.add("table")
                        const caption = document.createElement("caption")
                        if (res[0]["class"]["color"] === "green") {
                            caption.style.backgroundColor = "green"
                        } else {
                            caption.style.backgroundColor = "blue"
                        }
                        caption.classList.add("caption")
                        caption.innerHTML = `${res[0]["class"]["class_number"]} ${res[0]["class"]["color"]}`
                        table.append(caption)
                        const tr = document.createElement("tr")
                        const days = document.createElement("th")
                        days.innerHTML += "Hafta kunlari"
                        days.rowSpan = "2"
                        tr.append(days)
                        const tr2 = document.createElement("tr")
                        for (let t = 0; t < res[0]["times"].length; t++) {
                            const td = document.createElement("th")
                            const td2 = document.createElement("th")
                            td.innerHTML += res[0]["times"][t]["time_count"]
                            tr2.append(td)
                            td2.innerHTML += `${res[0]["times"][t]["start"]} ${res[0]["times"][t]["end"]}`
                            tr.append(td2)
                        }
                        table.append(tr)
                        table.append(tr2)
                        let trs = []
                        for (let i = 0; i < res.length; i++) {

                            let lessons = []

                            const lessonsData = res[i].lessons
                            const td = document.createElement("td")
                            td.innerHTML = res[i]["day"]["name"]
                            lessons.push(td)
                            for (let o = 0; o < lessonsData.length; o++) {


                                const td = document.createElement("td")
                                td.getAttribute("data-dayId")
                                td.setAttribute(`data-dayId`, res[i]["day"]["id"])
                                if (lessonsData[o]["lesson_id"]) {
                                    td.getAttribute("data-lessonId")
                                    td.setAttribute(`data-lessonId`, lessonsData[o]["lesson_id"])
                                }
                                td.getAttribute("data-classId")
                                td.setAttribute(`data-classId`, res[0]["class"]["id"])
                                td.getAttribute("data-timeId")
                                td.setAttribute(`data-timeId`, lessonsData[o]["lesson_time"]["id"])
                                if (lessonsData[o].teacher) {
                                    td.getAttribute("data-teacherId")
                                    td.setAttribute(`data-teacherId`, lessonsData[o].teacher["id"])
                                }
                                if (lessonsData[o].room) {
                                    td.getAttribute("data-roomId")
                                    td.setAttribute(`data-roomId`, lessonsData[o].room["id"])
                                }
                                if (lessonsData[o].subject) {
                                    td.getAttribute("data-subjectId")
                                    td.setAttribute(`data-subjectId`, lessonsData[o].subject["id"])
                                }
                                if (lessonsData[o]["lesson_time"]["count"] === "breakfast") {
                                    td.style.backgroundColor = 'rgba(0,0,0,0.09)'
                                } else if (res[0]["class"]["class_number"] >= 5 && lessonsData[o]["lesson_time"]["start"] === "13:10") {
                                    td.style.backgroundColor = 'rgba(0,0,0,0.09)'
                                } else if (res[0]["class"]["class_number"] <= 4 && lessonsData[o]["lesson_time"]["start"] === "12:15") {
                                    td.style.backgroundColor = 'rgba(0,0,0,0.09)'
                                } else {
                                    td.classList.add("zone-1")
                                }
                                const sub = document.createElement("div")
                                const teacher = document.createElement('div')
                                const room = document.createElement('div')
                                sub.getAttribute("data-isDropped")
                                sub.setAttribute("data-isDropped", true)
                                sub.draggable = true
                                teacher.getAttribute("data-isDropped")
                                teacher.setAttribute("data-isDropped", true)
                                teacher.draggable = true
                                room.getAttribute("data-isDropped")
                                room.setAttribute("data-isDropped", true)
                                room.draggable = true
                                room.classList.add("subjects")
                                room.classList.add("time_subject")
                                sub.classList.add("subjects")
                                sub.classList.add("time_subject")
                                teacher.classList.add("subjects")
                                teacher.classList.add("time_subject")
                                sub.innerHTML += lessonsData[o].subject?.name
                                teacher.innerHTML += `${lessonsData[o].teacher?.name}  ${lessonsData[o].teacher?.surname}`
                                room.innerHTML += lessonsData[o].room?.name
                                if (lessonsData[o].subject) {
                                    sub.getAttribute("data-lessonId")
                                    sub.setAttribute("data-lessonId", lessonsData[o]["lesson_id"])
                                    sub.getAttribute("data-subjectId")
                                    sub.setAttribute("data-subjectId", lessonsData[o]["subject"]["id"])
                                    td.append(sub)
                                }
                                if (lessonsData[o].teacher) {
                                    teacher.getAttribute("data-lessonId")
                                    teacher.setAttribute("data-lessonId", lessonsData[o]["lesson_id"])
                                    teacher.getAttribute("data-teacherId")
                                    teacher.setAttribute("data-teacherId", lessonsData[o]["teacher"]["id"])
                                    td.append(teacher)
                                }
                                if (lessonsData[o].room) {
                                    room.getAttribute("data-lessonId")
                                    room.setAttribute("data-lessonId", lessonsData[o]["lesson_id"])
                                    room.getAttribute("data-roomId")
                                    room.setAttribute("data-roomId", lessonsData[o]["room"]["id"])
                                    td.append(room)
                                }

                                lessons.push(td)

                            }
                            const tr = document.createElement("tr")

                            for (let l = 0; l < lessons.length; l++) {


                                tr.append(lessons[l])


                            }

                            trs.push(tr)
                        }
                        const tbody = document.createElement("tbody")

                        for (let e = 0; e < trs.length; e++) {


                            tbody.append(trs[e])


                        }
                        console.log(trs)
                        table.append(tbody)
                        time_table.append(table)
                        time_two.append(time_table)
                        container_direction.append(time_two)
                        console.log(container_direction)
                        main_container.append(container_direction)
                        main()

                    })
            }


        }
        // container_direction[index].classList.toggle("active_table")

    })

})

function main() {
    let subjects = document.querySelectorAll(".subjects"),
        subject_container = document.querySelector(".subject_container"),
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
                lesson_id: removedElement, item: removedBox, text: removedText, time_table_day_id: removedDay
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
                class_id, day_id, room_id, subject_id, teacher_id, lesson_time,
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
}

main()