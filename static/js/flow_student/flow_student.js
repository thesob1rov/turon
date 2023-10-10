let flow = document.querySelector('#flow_list'),
    flow_btn = document.querySelector('#flow'),
    room = document.querySelector('#room_list')
room_btn = document.querySelector('#room');


flow_btn.addEventListener('click', () => {
    flow.classList.add('active')
    room.classList.remove('active')
    room_btn.style.background = "#adadad"
    flow_btn.style.background = "#111f4c"
})
room_btn.addEventListener('click', () => {
    room.classList.add('active')
    flow.classList.remove('active')
    room_btn.style.background = "#111f4c"
    flow_btn.style.background = "#adadad"
})

let subjects = document.querySelectorAll(".subjects"), subject_container = document.querySelector(".subject_container"),
    teachers = document.querySelectorAll('.teachers'), rooms = document.querySelectorAll('.rooms');

const drop = document.querySelectorAll(".zone-1");


let draggedElem, roomId, flowId, isDropped, currentElem


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
    flowId = this.getAttribute("data-flowId")
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
console.log(isDropped)
    if (!ev.target.classList.contains("drop") && isDropped === "true" && !ev.target.classList.contains("time_subject")) {


        if (roomId) currentElem.parentElement.removeAttribute("data-roomId")
        if (flowId) currentElem.parentElement.removeAttribute("data-flowId")

        let removedElement
        let removedBox
        let removedText
        let removedDay
        removedElement = currentElem.getAttribute("data-lessonId")
        if (currentElem.getAttribute("data-flowId")) {
            removedBox = currentElem.getAttribute("data-flowId")
            removedText = "flow"
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
        fetch('/delete_flow_item_in_lesson', {
            method: "POST", body: JSON.stringify({
                "info": info
            }), headers: {
                'Content-type': 'application/json'
            }
        })
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
        const itemFlowId = item.getAttribute("data-flowId")

        const isRoom = roomId ? itemFlowId !== roomId && !itemRoomId : null
        const isFlow = flowId ? itemFlowId !== flowId && !itemFlowId : null

        removeBoxes()
        if (isRoom || isFlow) {
            const elem = draggedElem
            elem.setAttribute("data-isDropped", true)

            item.append(elem)

            const elements = item.querySelectorAll(".time_subject")
            sortElement(elements, item)

            if (roomId) item.setAttribute(`data-roomId`, roomId)
            if (flowId) item.setAttribute(`data-flowId`, flowId)

        }
        roomId = null
        flowId = null
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
        const itemFlowId = item.getAttribute("data-flowId")

        if (itemRoomId) {
            return {
                item, index: 0
            }
        }
        if (itemFlowId) {
            return {
                item, index: 1
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
    const flow_id = item.getAttribute("data-flowId")
    const day_id = item.getAttribute("data-dayId")
    const lesson_time = item.getAttribute("data-timeId")
    if (room_id && flow_id) {
        console.log("true")

        let info = {
            day_id,
            room_id,
            lesson_time,
            flow_id,
        }
        if (item.getAttribute("data-lessonId")) {
            let lesson_id = item.getAttribute("data-lessonId")
            info.lesson_id = lesson_id
        } else {
            info.lesson_id = ""
        }
        console.log(info)
        fetch('/creat_flow_timetable', {
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

