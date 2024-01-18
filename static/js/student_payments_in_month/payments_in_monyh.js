let delButton = document.querySelectorAll('.delButton');

delButton.forEach(trash => {
    trash.addEventListener("click", () => {
        const confirm_question = confirm("Siz bu tolovni ochirmoqchimisiz?")
        if (confirm_question === true) {
            fetch('/delete_object', {
                method: "POST", body: JSON.stringify({
                    "id": trash.dataset.id, 'type': trash.dataset.type
                }), headers: {
                    'Content-type': 'application/json'
                }
            })
                .then(response => response.json())
                .then(resp => {
                    if (resp['status'] === true) {
                        window.location.href = `/all_payments/${trash.dataset.type}/1`;
                    }
                })
        }
    })
})
