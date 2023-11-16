let plan = document.querySelector('.plan'), button = document.querySelector('.plan button'),
    lesson_plan = document.querySelector('.lesson_plan'), span = document.querySelectorAll('.span'),
    name_input = plan.querySelector('.name'), target_input = plan.querySelector('.target'),
    main_input = plan.querySelector('.main'), assessment_input = plan.querySelector('.assessment'),
    homework_input = plan.querySelector('.homework');

span.forEach(item => {
    item.addEventListener('click', () => {
        console.log(item)
        if (item.dataset.change === 'True') {
            if (item.dataset.status === 'False') {
                plan.classList.add('active_add')
                button.addEventListener('click', () => {

                    if (name_input.value) {
                        console.log(item.dataset.time)
                        fetch('/add_lesson_plan', {
                            method: "POST", body: JSON.stringify({
                                'day_id': item.dataset.id,
                                'lesson_time_id': item.dataset.time,
                                'name': name_input.value,
                                'target': target_input.value,
                                'main': main_input.value,
                                'assessment': assessment_input.value,
                                'homework': homework_input.value
                            }), headers: {
                                'Content-type': 'application/json'
                            }
                        })

                            .then(response => response.json())
                            .then(resp => {
                                item.innerHTML = ''
                                plan.classList.remove('active_add')
                                item.innerHTML = `<td data-change="True"
                                    data-status="True"
                                    data-time="${item.dataset.time}"
                                    data-id="${item.dataset.id}" class="span">
                                    
                                    Sinf

                                    <i style="color: #34d534"
                                       class="fa-solid fa-check">
                                    </i>
                                </td>`
                                name_input.value = ''
                                target_input.value = ''
                                main_input.value = ''
                                assessment_input.value = ''
                                homework_input.value = ''
                            })

                    }
                })
            } else if (item.dataset.status === 'True') {
                fetch('/get_lesson_plan', {
                    method: "POST", body: JSON.stringify({
                        'day_id': item.dataset.id, 'lesson_time_id': item.dataset.time
                    }), headers: {
                        'Content-type': 'application/json'
                    }
                })

                    .then(response => response.json())
                    .then(response => {
                        plan.classList.add('active_add')
                        name_input.value = `${response['lesson_data']['name']}`
                        target_input.value = `${response['lesson_data']['target']}`
                        main_input.value = `${response['lesson_data']['main']}`
                        assessment_input.value = `${response['lesson_data']['assessment']}`
                        homework_input.value = `${response['lesson_data']['homework']}`
                    })
                button.addEventListener('click', () => {
                    fetch('/change_lesson_plan', {
                        method: "POST", body: JSON.stringify({
                            'day_id': item.dataset.id,
                            'lesson_time_id': item.dataset.time,
                            'name': name_input.value,
                            'target': target_input.value,
                            'main': main_input.value,
                            'assessment': assessment_input.value,
                            'homework': homework_input.value
                        }), headers: {
                            'Content-type': 'application/json'
                        }
                    })
                        .then(response => response.json())
                        .then(response => {
                            item.innerHTML = ''
                            plan.classList.remove('active_add')
                            item.innerHTML = `<td data-change="True"
                                    data-status="True"
                                    data-time="${item.dataset.time}"
                                    data-id="${item.dataset.id}" class="span">
                                    
                                    Sinf

                                    <i style="color: #34d534"
                                       class="fa-solid fa-check">
                                    </i>
                                    
                                </td>`
                            name_input.value = ''
                            target_input.value = ''
                            main_input.value = ''
                            assessment_input.value = ''
                            homework_input.value = ''
                        })
                })
            }

        } else {
            fetch('/get_lesson_plan', {
                method: "POST", body: JSON.stringify({
                    'day_id': item.dataset.id, 'lesson_time_id': item.dataset.time
                }), headers: {
                    'Content-type': 'application/json'
                }
            })

                .then(response => response.json())
                .then(response => {
                    if (response['lesson_data']['status']) {
                        plan.classList.add('active_add')
                        name_input.value = `${response['lesson_data']['name']}`
                        target_input.value = `${response['lesson_data']['target']}`
                        main_input.value = `${response['lesson_data']['main']}`
                        assessment_input.value = `${response['lesson_data']['assessment']}`
                        homework_input.value = `${response['lesson_data']['homework']}`
                        button.style.display = 'none'
                    } else {
                        alert("Bu kunda dars reja yo'q")
                    }

                })
        }

    })
})
plan.addEventListener('click', (event) => {
    if (event.target === plan) {
        plan.classList.remove('active_add')
        name_input.value = ''
        target_input.value = ''
        main_input.value = ''
        assessment_input.value = ''
        homework_input.value = ''
        button.style.display = 'flex'
    }
})