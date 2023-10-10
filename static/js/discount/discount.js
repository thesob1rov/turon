let discount_type = document.querySelector('.discount_type'),
    percentage = document.querySelector('.percentage');


discount_type.addEventListener('change', () => {
    const info = {
        student_id: discount_type.dataset.id,
        discount_type: discount_type.value
    }
    fetch('/check_discount', {
        method: "POST", body: JSON.stringify({
            "info": info
        }), headers: {
            'Content-type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(resp => {
            percentage.value = resp["percentage"]
        })
})