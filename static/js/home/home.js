let xmark = document.querySelector('.x'),
    plus=document.querySelector('.plus');




function addClass(boxes) {
    boxes[0].classList.add("w2")
    boxes[4].classList.add("h2")
    boxes[5].classList.add("w2")
}

function updateGallery(response) {
    let big = document.querySelector('.big');
    big.innerHTML = ''
    for (let img of response['gallery_list']) {
        big.innerHTML += `<div class="box" data-id="${img['id']}">
                    <img class="box_img" src="${img['img_url']}" alt="">
                </div>`
    }
    let boxes = document.querySelectorAll(".box");

    boxes.forEach(item => {
        item.addEventListener("click", async () => {


        })
    })
    console.log(boxes)
    if (!boxes){
         addClass(boxes)
    }

}

fetch('/get_gallery', {
    method: "GET",
})
    .then(function (response) {
        return response.json()
    })
    .then(function (response) {
        updateGallery(response)
    })


function updatePartners(response) {
    let big = document.querySelector('.logo');
    big.innerHTML = ''
    for (let img of response['gallery_list']) {
        big.innerHTML += `
                    <img class="box_img" src="${img['img_url']}" alt="">`
    }
    let boxes = document.querySelectorAll(".box");

    boxes.forEach(item => {
        item.addEventListener("click", async () => {


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
        updatePartners(response)
    })