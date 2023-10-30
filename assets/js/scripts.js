window.addEventListener('DOMContentLoaded', event => {

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar 
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            rootMargin: '0px 0px -40%',
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

});
let carousel = document.querySelector('.carousel');
let items = document.querySelectorAll('.item');
let currentItem = 0;
let isMoving = false;

function rotateCarousel() {
    let angle = currentItem * -72;
    carousel.style.transform = 'rotateY(' + angle + 'deg)';
}

let prevButton = document.getElementById('prev');
prevButton.addEventListener('click', function() {
    if (isMoving) return;
    isMoving = true;
    if (currentItem === 0) {
        currentItem = items.length - 1;
    } else {
        currentItem--;
    }
    rotateCarousel();
});

let nextButton = document.getElementById('next');
nextButton.addEventListener('click', function() {
    if (isMoving) return;
    isMoving = true;
    if (currentItem === items.length - 1) {
        currentItem = 0;
    } else {
        currentItem++;
    }
    rotateCarousel();
});

// Después de que la transición termine, cambia isMoving a false
carousel.addEventListener('transitionend', function() {
    isMoving = false;
});
