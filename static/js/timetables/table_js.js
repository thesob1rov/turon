let teacher = document.querySelector('#teacher_list'),
    subject = document.querySelector('#subject_list'),
    teacher_btn = document.querySelector('#teacher'),
    subject_btn = document.querySelector('#subject'),
    room = document.querySelector('#room_list')
room_btn = document.querySelector('#room');

teacher_btn.addEventListener('click', () => {
    teacher.classList.add('active')
    subject.classList.remove('active')
    room.classList.remove('active')
    teacher_btn.style.background = " #111f4c"
    subject_btn.style.background = " #adadad"
    room_btn.style.background = " #adadad"

})
subject_btn.addEventListener('click', () => {
    subject.classList.add('active')
    teacher.classList.remove('active')
    room.classList.remove('active')
    subject_btn.style.background = " #111f4c"
    teacher_btn.style.background = " #adadad"
    room_btn.style.background = " #adadad"
})

room_btn.addEventListener('click', () => {
    room.classList.add('active')
    teacher.classList.remove('active')
    subject.classList.remove('active')
    room_btn.style.background = " #111f4c"
    subject_btn.style.background = " #adadad"
    teacher_btn.style.background = " #adadad"
})
// let h1 = document.createElement('h1');
// h1.innerText = "hello"
// subject.appendChild(h1)
let class_table = document.querySelector('.class_table')
let time = document.querySelector('.container')
time.appendChild(class_table.cloneNode(true))