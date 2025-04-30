  document.addEventListener("DOMContentLoaded", function () {
    // Agregar clase para activar transición con CSS si la usás
    document.querySelector(".section-presentacion")?.classList.add("show");

    // Animar el logo
    anime({
      targets: '.a-logo',
      translateY: [-100, 0],
      duration: 1500,
      easing: 'easeInOutQuad'
    });

  });
