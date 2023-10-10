const radio = document.querySelectorAll('.radio')
const input = document.querySelector('.input');
const button = document.querySelector('.btn');
const student_id = document.querySelector('.student_id');

button.addEventListener('click', () => {


    const info = {
        account_type_id: 0,
        money: input.value,
        student_id: student_id.dataset.id
    }
    radio.forEach(item => {
        if (item.checked) {
            info.account_type_id = item.dataset.id
        }
    })
    fetch('/payment', {
        method: "POST", body: JSON.stringify({
            "info": info
        }), headers: {
            'Content-type': 'application/json'
        }
    })
    input.value = ''
})