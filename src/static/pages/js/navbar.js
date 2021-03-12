const navbar = document.getElementById("navbar");
navbar.classList.remove("scroll");
console.log(navbar);
window.onscroll = () => {
  if (
    document.body.scrollTop >= 100 ||
    document.documentElement.scrollTop >= 100
  ) {
    navbar.classList.add("scroll");
  } else {
    navbar.classList.remove("scroll");
  }
};
