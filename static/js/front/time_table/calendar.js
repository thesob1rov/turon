var splide = new Splide('.splide', {
    type: 'loop', focus: "center", // padding: '5rem',
    // perPage: 3,
    breakpoints: {
        1024: {
            perPage: 5,

        }, 768: {
            perPage: 2,

        }, 640: {
            perPage: 1,

        }, 576: {
            perPage: 1
        }
    },
});

splide.mount();