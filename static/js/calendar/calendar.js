let td = document.querySelectorAll('.index_box_days .td'), calendar_active = document.querySelector('.calendar_active'),
    button = document.querySelector('.button'), select = document.querySelector('#select'), day_id = 0;

td.forEach(item => {
    item.addEventListener('click', () => {
        calendar_active.classList.remove('active_sunday')
        day_id = item.dataset.id
    })
})
button.addEventListener('click', () => {
    fetch('change_type', {
        method: 'POST', body: JSON.stringify({
            'day_id': day_id, 'type_id': select.value
        }), headers: {
            'Content-type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(response => {
            td.forEach(item => {
                if (day_id === item.dataset.id) {
                    item.style.background = `${response['color']}`
                }
            })
            calendar_active.classList.add('active_sunday')
            day_id = 0
        })
})