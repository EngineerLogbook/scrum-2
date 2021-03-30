const navToggleBtn = document.getElementById("nav-toggle");
const navUl = document.getElementById("nav-ul");

navToggleBtn.addEventListener("click", () => {
  navUl.classList.contains("open")
    ? navUl.classList.remove("open")
    : navUl.classList.add("open");
});

[...navUl.children].forEach((link) => {
  link.addEventListener("click", () => {
    navUl.classList.remove("open");
  });
});
