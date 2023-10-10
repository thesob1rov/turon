let murojat_delete = document.querySelectorAll('.murojat_delete'),
    delete_icon = document.querySelectorAll('.delete');

murojat_delete.forEach((item, index) => {
    item.addEventListener('click', () => {
        let status = confirm("Izohni o'chirishni xohlaysizmi");
        if (status) {
            delete_icon[index].click()
        }
    })
})