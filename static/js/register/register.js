let box = document.querySelectorAll('.block_info_item'),
    block = document.querySelector('.block'),
    input = document.querySelectorAll('.input'),
    block_info = document.querySelectorAll('.block_info'),
    dates_info = document.querySelectorAll('.dates_info'),
    dates_item = document.querySelectorAll('.dates_item')


block_info.forEach((item, index) => {
    item.addEventListener('click', () => {
        input[index].click()
        box[index].classList.add('input_active')
    })
})

function add(block_info, box, input) {
    block.addEventListener('click', (event) => {
        console.log(true)
        if (event.target !== block_info && event.target !== box && event.target !== input) {
            if (!input.value) {
                box.classList.remove('input_active')
            }
        }
    })
}


dates_info.forEach((item, index) => {
    item.addEventListener('click', () => {
        dates_item[index].classList.add('active')
    })
})


add(block_info[0], box[0], input[0])
add(block_info[1], box[1], input[1])
add(block_info[2], box[2], input[2])