
function scrollToTop(){
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    })
}

document.getElementById('scrollToTopButton').addEventListener('click', scrollToTop)

window.onscroll = function () {
    var button = document.getElementById('scrollToTopButton');

    if(document.body.scrollTop > 40 || document.documentElement.scrollTop > 40){
        button.style.display = "block"
    }else{
        button.style.display = "none"
    }
};



const firstname = document.querySelector('#firstName');
const lastname = document.querySelector('#lastName');
const errorFirstname = document.querySelector('#error-firstname');
const formRegister = document.querySelector('#formRegister');


if(firstname && lastname && errorFirstname && formRegister){
    formRegister.addEventListener('submit', validarFormulario)
}else{
    console.log("error no se puede manejar eventos no encontrados")
}

function validarFormulario(event){
    event.preventDefault();

    let validation = true;

    if(firstname.value ===''){
        firstname.classList.add("error");
        errorFirstname.textContent = "El nombre no puede estar vacio"
        validation = false
    }else{
        firstname.classList.remove("error");
        errorFirstname.textContent = ""
    }


    if(lastname.value ===''){
        lastname.classList.add("error");
        alert("El apellido no puede estar vacio");
        validation = false
    }else{
        firstname.classList.remove("error");
        
    }

    if(validation){
        console.log("Nombre y apellido validos")
    }else{
        console.log("El formulario tiene errores, no se puede enviar")
    }

    firstname.addEventListener('input', () =>{
        if(firstname.value !== ''){
            firstname.classList.remove('error')
            errorFirstname.textContent = "";
        }
    });

    lastname.addEventListener('input', () =>{
        
            lastname.classList.remove('error')
        
    });

}

/* AGREGADP desplazamiento suave*/
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

/* AGREGADP desplazamiento suave*/


// para el Movimiento
const scroller = document.getElementById('top-rated-list');
let scrollAmount = 0;
const scrollSpeed = 1; // Ajusta la velocidad del desplazamiento


function scrollItems() {
    scrollAmount += scrollSpeed; // Ajusta la velocidad del desplazamiento
    scroller.style.transform = `translateX(-${scrollAmount}px)`;

    // Reinicia el desplazamiento cuando se haya desplazado una cierta cantidad
    if (scrollAmount >= scroller.scrollWidth / 2) {
        scrollAmount = 0; // Reinicia el desplazamiento
    }

    requestAnimationFrame(scrollItems); // Llama a la función de nuevo
}

// Inicia el desplazamiento
scrollItems();
// para el Movimiento

const menuToggle = document.getElementById('menu-toggle');
const menuLabel = document.querySelector('.menu-toggle-icon');

menuToggle.addEventListener('change', () => {
    const isChecked = menuToggle.checked;
    menuLabel.setAttribute('aria-expanded', isChecked);
});

document.querySelector('.hamburger-button').addEventListener('click', function() {
    // Código para mostrar/ocultar el menú
});
