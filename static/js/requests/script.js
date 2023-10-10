let delete_request = document.querySelectorAll('.delete_request'),
    delete_link = document.querySelectorAll('.delete_link');

delete_request.forEach((item, index) => {
    item.addEventListener('click', () => {
        let status = confirm("Arizani o'chirishni xohlaysizmi?");
        if (status) {
            delete_link[index].click()
        }
    })
})