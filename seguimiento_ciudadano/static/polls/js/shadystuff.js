let autohide = document.querySelector('.autohide');
let navbar = document.getElementById("ChihEmprendeNav");
let sticky = navbar.offsetTop;
let last_scroll_top = 0;

document.addEventListener("DOMContentLoaded", function(){
    navbar.classList.add("sticky")
    window.onscroll = function() {scrollhide()};
    function scrollhide() {
        let scroll_top = window.scrollY;
        if(scroll_top < last_scroll_top) {
            autohide.classList.remove('scrolled-down');
            autohide.classList.add('scrolled-up');
        }
        else {
            autohide.classList.remove('scrolled-up');
            autohide.classList.add('scrolled-down');
        }
        last_scroll_top = scroll_top;
    }
});