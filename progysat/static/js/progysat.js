var navbar = document.getElementById("navbar");
var bodyContent = document.getElementById("body-content");

function updateNavbarSuccinctStatus() {
    if (window.scrollY > 150) {
        navbar.classList.add("is-succinct");
        bodyContent.classList.add("is-succinct-pt");
    } else {
        navbar.classList.remove("is-succinct");
        bodyContent.classList.remove("is-succinct-pt");
    }
}

window.addEventListener('scroll', updateNavbarSuccinctStatus);

function toggleLanguageDropdown() {
    console.log("toggleLanguageDropdown 0");
    var el = document.getElementById("language-dropdown");
    console.log("toggleLanguageDropdown", el);
    if (el.classList.contains('is-active')){
        el.classList.remove('is-active');
    } else {
        el.classList.add('is-active');
    }
}
