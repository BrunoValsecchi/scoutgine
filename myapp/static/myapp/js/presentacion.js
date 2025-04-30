// Esperar a que el DOM se cargue completamente
document.addEventListener('DOMContentLoaded', function() {
    // Animaciones de texto e imágenes al cargar la página
    animateEntrance();
    
    // Efecto de color deslizante
    animateColorSlider();
    
    // Efecto parallax al mover el ratón
    setupParallaxEffect();
    
    // Efecto al hacer scroll
    setupScrollEffect();
    
    // Animación de elementos del header
    animateHeaderElements();
});

// Animación de entrada para todos los elementos
function animateEntrance() {
    // Animación del título
    anime({
        targets: '.animated-title',
        opacity: [0, 1],
        translateY: [20, 0],
        easing: 'easeOutExpo',
        duration: 1200,
        delay: 300
    });
    
    // Animación de los párrafos de texto
    anime({
        targets: '.animated-text',
        opacity: [0, 1],
        translateY: [15, 0],
        easing: 'easeOutExpo',
        duration: 1200,
        delay: anime.stagger(200, {start: 500})
    });
    
    // Animación del botón CTA
    anime({
        targets: '.cta-button',
        opacity: [0, 1],
        translateY: [15, 0],
        easing: 'easeOutExpo',
        duration: 1000,
        delay: 1000
    });
    
    // Animación de las imágenes
    anime({
        targets: '.chart-image',
        opacity: [0, 1],
        translateX: [20, 0],
        easing: 'easeOutExpo',
        duration: 1500,
        delay: function(el, i) {
            return 800 + (i * 300);
        }
    });
}

// Efecto de color deslizante de izquierda a derecha - versión más sutil
function animateColorSlider() {
    anime({
        targets: '.color-slider',
        translateX: ['0%', '50%'],
        easing: 'linear',
        duration: 18000,
        loop: true,
        direction: 'alternate'
    });
}

// Configurar efecto parallax en las imágenes según movimiento del ratón
function setupParallaxEffect() {
    document.addEventListener('mousemove', function(e) {
        const windowWidth = window.innerWidth;
        const windowHeight = window.innerHeight;
        
        const mouseX = e.clientX;
        const mouseY = e.clientY;
        
        // Calcular posición relativa del ratón (de -1 a 1)
        const xPos = (mouseX / windowWidth - 0.5) * 2;
        const yPos = (mouseY / windowHeight - 0.5) * 2;
        
        // Mover las imágenes en dirección inversa al movimiento del ratón - más sutil
        const images = document.querySelectorAll('.chart-image');
        images.forEach((img, index) => {
            const factor = (index + 1) * 5; // Factor de movimiento más sutil para cada imagen
            
            anime({
                targets: img,
                translateX: xPos * factor,
                translateY: yPos * factor,
                duration: 1200, // Más lento para un efecto más profesional
                easing: 'easeOutQuad'
            });
        });
    });
}

// Efecto al hacer scroll
function setupScrollEffect() {
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Efecto en las imágenes al hacer scroll
        anime({
            targets: '.image-column',
            translateY: scrollTop * 0.05,
            duration: 400,
            easing: 'easeOutQuad'
        });
        
        // Efecto en el título al hacer scroll
        anime({
            targets: '.animated-title',
            translateY: scrollTop * 0.02,
            duration: 400,
            easing: 'easeOutQuad'
        });
    });
}

// Animaciones de los elementos del header
function animateHeaderElements() {
    // Animación del logo
    anime({
        targets: '.logo',
        scale: [0.9, 1],
        opacity: [0, 1],
        easing: 'easeOutExpo',
        duration: 1200
    });
    
    // Animación de los links del menú
    anime({
        targets: '.div-headerlan-ul li',
        translateY: [-10, 0],
        opacity: [0, 1],
        easing: 'easeOutExpo',
        duration: 1000,
        delay: anime.stagger(100, {start: 300})
    });
    
    // Efecto hover para los links del menú
    const menuLinks = document.querySelectorAll('.li-a-header');
    menuLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            anime({
                targets: this,
                scale: 1.1,
                color: '#3498db',
                duration: 300,
                easing: 'easeOutQuad'
            });
        });
        
        link.addEventListener('mouseleave', function() {
            anime({
                targets: this,
                scale: 1,
                color: '#ffffff',
                duration: 300,
                easing: 'easeOutQuad'
            });
        });
    });
    
    // Efecto hover para el botón CTA
    const ctaButton = document.querySelector('.cta-button');
    if (ctaButton) {
        ctaButton.addEventListener('mouseenter', function() {
            anime({
                targets: this,
                scale: 1.05,
                boxShadow: '0 0 15px rgba(52, 152, 219, 0.5)',
                duration: 300,
                easing: 'easeOutQuad'
            });
        });
        
        ctaButton.addEventListener('mouseleave', function() {
            anime({
                targets: this,
                scale: 1,
                boxShadow: '0 0 0 rgba(52, 152, 219, 0)',
                duration: 300,
                easing: 'easeOutQuad'
            });
        });
    }
}