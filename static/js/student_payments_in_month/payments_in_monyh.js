let delButtonPay = document.querySelectorAll('.delButtonPay'), delButtonCost = document.querySelectorAll('.delButtonCost');

delButtonPay.forEach(trash => {
    trash.addEventListener("click", () => {
        const confirm_question = confirm("Siz bu tolovni ochirmoqchimisiz?")
        if (confirm_question === true) {
            fetch('/delete_payment', {
                method: "POST", body: JSON.stringify({
                    "id": trash.dataset.id
                }), headers: {
                    'Content-type': 'application/json'
                }
            })
        }
    })
})
delButtonCost.forEach(trash => {
    trash.addEventListener("click", () => {
        const confirm_question = confirm("Siz bu harajatni ochirmoqchimisiz?")
        if (confirm_question === true) {
            fetch('/delete_cost', {
                method: "POST", body: JSON.stringify({
                    "id": trash.dataset.id
                }), headers: {
                    'Content-type': 'application/json'
                }
            })
        }
    })
})