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
    var el = document.getElementById("language-dropdown");
    if (el.classList.contains('is-active')){
        el.classList.remove('is-active');
    } else {
        el.classList.add('is-active');
    }
}

// make Bulma navbar work
document.addEventListener('DOMContentLoaded', () => {
  // Get all "navbar-burger" elements
  var $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

  // Add a click event on each of them
  $navbarBurgers.forEach( el => {
      el.addEventListener('click', () => {
      console.log("### click on navbar1");
      // Get the target from the "data-target" attribute
      var target = el.dataset.target;
      var $target = document.getElementById(target);

      // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
      el.classList.toggle('is-active');
      $target.classList.toggle('is-active');

    });
  });
});
