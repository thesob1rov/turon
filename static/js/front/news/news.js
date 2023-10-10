let add_circle = document.querySelector(".circle"), modal = document.querySelector(".modal"),
    close_modal = document.querySelector(".close_modal"), x_2 = document.querySelector(".x_2"),
    back2 = document.querySelector('.back2'),
    next2 = document.querySelector('.next2'), days2 = document.querySelector('.days'),
    main_date2 = document.querySelector('.main_date2'),
    montYear = document.querySelector(".main_date"), days = document.querySelector(".main_weeks_day"),
    back = document.querySelector(".back"), next = document.querySelector(".next"), currentId = 0,
    big_boxes = document.querySelector(".news_list"),
    file_img = document.querySelector('.file_img'), title = document.querySelector(".add_name"),
    desc = document.querySelector(".add_desc"),
    modal__big__block_h1 = document.querySelector('.modal__big__block h1'),
    send = document.querySelector(".send"), img = document.querySelector(".add_img"),
    date = document.querySelector(".add_date"), delete_btn = document.querySelector(".delete"),
    news_left = document.querySelector('.news_left'),
    news_right = document.querySelector('.news_right'),
    counter = 0;


function getNewData(button, days, month_year, num) {
    button.addEventListener("click", () => {
        days.innerHTML = ""
        month_year.innerHTML = ""
        getDates(num, days, month_year)
    })
}

getNewData(back, days, montYear, -1)
getNewData(next, days, montYear, 1)
let events = []

function getDates(num, days, month_year) {
    let events = []
    fetch('/calendar_change/' + num, {
        method: "GET", headers: {
            'Content-type': 'application/json'
        },
    })
        .then(function (response) {
            return response.json()
        })
        .then(function (jsonResponse) {
            month_year.innerHTML = `${jsonResponse['date']['info_date']}`
            for (let item of jsonResponse['date']['day']) {
                if (item['boolean'] === true) {
                    for (let event of item['events']) {
                        events.push(event)
                    }


                    let className = "active"
                    days.innerHTML += `<li class="${className}">${item['day_range']}</li>`
                } else {
                    days.innerHTML += `<li>${item['day_range']}</li>`
                }
            }

            renderEvent(events)
        })
}

const edit = []
get_news(montYear, days)


function get_news(month_year, days) {
    fetch('/news', {
        method: "GET", headers: {
            'Content-type': 'application/json'
        },
    })
        .then(function (response) {
            return response.json()
        })
        .then(function (jsonResponse) {
            month_year.innerHTML = `${jsonResponse['date']['info_date']}`
            for (let item of jsonResponse['date']['day']) {
                if (item['boolean'] === true) {
                    for (let event of item['events']) {
                        events.push(event)
                    }
                    let className = "active_calendar"
                    days.innerHTML += `<li class="${className}">${item['day_range']}</li>`
                } else {
                    days.innerHTML += `<li>${item['day_range']}</li>`
                }
            }
            console.log(true)
            renderEvent(events)
        })
}


function filter_news(events) {
    let filtered_events = []
    for (let item of events) {
        let exist = false
        for (let event of filtered_events) {
            if (event['id'] === item['id']) {
                exist = true
            }
            if (exist) {
                break
            }
        }
        if (!exist) {
            filtered_events.push(item)
        }
    }
    return filtered_events
}

function renderEvent(events) {
    big_boxes.innerHTML = ""


    let filtered_list = filter_news(events)
    console.log(filtered_list)
    if (filtered_list.length > 0) {
        news_left.style.display = "initial"
        news_right.style.display = "initial"
        filtered_list.map((item, index) => {
            currentId = index
            if (index === 0) {
                big_boxes.innerHTML += `
            <div class="news_item news_item_active" data-info_id="${item.id}">
                    <img class="cont_img" src="${item.img}" alt="">
                    <div class="box1">
                        <h4 class="sana">${item.date}</h4>
                       
                    </div>
                    <div class="news_text">
                        <h1>${item.title}</h1>
                        <p>${item.desc}</p>
                    </div>
            </div>      
        `
            } else {
                big_boxes.innerHTML += `
            <div class="news_item" data-info_id="${item.id}">
                    <img class="cont_img" src="${item.img}" alt="">
                    <div class="box1">
                        <h4 class="sana">${item.date}</h4>
                     
                    </div>
                    <div class="news_text">
                        <h1>${item.title}</h1>
                        <p>${item.desc}</p>
                    </div>
            </div>      
        `
            }

        })
    } else {
        news_left.style.display = "none"
        news_right.style.display = "none"
    }

    let edit_icon = document.querySelectorAll(".edit"),
        counter = 0,
        news_item = document.querySelectorAll('.news_item');
    edit_icon.forEach((elem, index) => {
        elem.addEventListener("click", () => {
            console.log(index)
            currentId = index
            modal.style.display = "flex"
            title.value = filtered_list[index].title
            desc.value = filtered_list[index].desc
            date.value = filtered_list[index].edit_date
            img.src = filtered_list[index].img
            main_date2.innerHTML = ""
            days2.innerHTML = ""
            get_news(main_date2, days2)
            modal.action = `/edit_news/${news_item[index].dataset.info_id}`
            modal__big__block_h1.innerText = "Yangilik O'zgartirish"
            delete_btn.style.display = "flex"
        })
    })
    news_right.addEventListener('click', () => {
        counter++
        if (counter > news_item.length - 1) {
            counter = 0
        }
        news_item.forEach(item => {
            item.classList.remove('news_item_active')
        })
        news_item[counter].classList.add('news_item_active')

    })
    news_left.addEventListener('click', () => {
        counter--
        if (counter < 0) {
            counter = news_item.length - 1
        }
        news_item.forEach(item => {
            item.classList.remove('news_item_active')
        })
        news_item[counter].classList.add('news_item_active')

    })

}




