const hamMenu = document.querySelector('.hamburger-menu');
const myNav = document.getElementById("mobile-nav");
hamMenu.addEventListener('click', () => {
    hamMenu.classList.toggle('active');
    if (myNav.style.height == "100%") {
        myNav.style.height = "0%";
    }
    else {
        myNav.style.height = "100%";
    };
});