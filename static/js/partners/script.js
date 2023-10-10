// fetch('/gallery_edit', {
//     method: "POST", body: JSON.stringify({
//         "edit": firstGalleryList,
//     }), headers: {
//         'Content-type': 'application/json'
//     },
// })
let input = document.querySelector(".img");


function updateGallery(response) {
    let big = document.querySelector('.logo');
    big.innerHTML = ''
    for (let img of response['gallery_list']) {
        big.innerHTML += `<div class="logo_box" data-id="${img['id']}">
                    <img class="logo_img" src="${img['img_url']}" alt="">
                </div>`
    }
    let boxes = document.querySelectorAll(".logo_box");

    boxes.forEach(item => {
        item.addEventListener("click", async () => {


            input.click()
            input.setAttribute("data-id", item.dataset.id)
        })
    })

}

fetch('/get_partners', {
    method: "GET",
})
    .then(function (response) {
        return response.json()
    })
    .then(function (response) {
        updateGallery(response)
    })

input.addEventListener("change", () => {
    console.log(input.dataset.id)
    const data = new FormData()

    data.append("file", input.files[0])
    console.log(input.files[0])
    fetch('/partner_edit/' + input.dataset.id, {
        method: "POST", body: data
    })
        .then(function (response) {
            return response.json()
        })
        .then(function (response) {
            updateGallery(response)
        })

})


