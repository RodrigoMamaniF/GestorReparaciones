// JavaScript para agregar la clase visible cuando la página se carga.

document.addEventListener("DOMContentLoaded", function() {
    const containers = document.querySelectorAll('.container');
    containers.forEach(container => {
        container.classList.add('visible');
    });

    const menuToggle = document.getElementById("menu-toggle");
    const mobileNav = document.querySelector(".mobile-nav");

    menuToggle.addEventListener("change", function() {
        mobileNav.style.display = menuToggle.checked ? "flex" : "none"; // Muestra u oculta el menú
    });
});

document.querySelector('.hamburger-button').addEventListener('click', function() {
    // Código para mostrar/ocultar el menú
});