let plan = document.querySelector('.plan'), lesson_plan = document.querySelector('.lesson_plan'),
    span = document.querySelectorAll('.span');
span.forEach(item => {
    item.addEventListener('click', () => {

        plan.classList.add('active_add')
    })
})
plan.addEventListener('click', (event) => {
    if (event.target === plan) {
        plan.classList.remove('active_add')
    }
})