let td = document.querySelectorAll('.index_box_days .td'), calendar_active = document.querySelector('.calendar_active'),
    button = document.querySelector('.button'), select = document.querySelector('#select');

td.forEach(item => {
    item.addEventListener('click', () => {
        calendar_active.classList.remove('active_sunday')
        button.addEventListener('click', () => {
            fetch('change_type', {
                method: 'POST', body: JSON.stringify({
                    'day_id': item.dataset.id, 'type_id': select.value
                }), headers: {
                    'Content-type': 'application/json'
                }
            })
                .then(response => response.json())
                .then(response => {
                    calendar_active.classList.add('active_sunday')
                    item.style.background = `${response['color']}`
                })
        })

    })
})
