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
    
    // Nuevas animaciones para puntos de datos
    animateDataPoints();

    // Efecto descripcion
    descriptionEffect();

});

// Animación de entrada mejorada para todos los elementos
function animateEntrance() {
    // Animación del título
    anime({
        targets: '.animated-title',
        opacity: [0, 1],
        translateY: [30, 0],
        easing: 'easeOutExpo',
        duration: 1400,
        delay: 300
    });
    
    // Animación de los párrafos de texto
    anime({
        targets: '.animated-text',
        opacity: [0, 1],
        translateY: [20, 0],
        easing: 'easeOutExpo',
        duration: 1400,
        delay: anime.stagger(250, {start: 600})
    });
    
    // Animación del botón CTA
    anime({
        targets: '.cta-button',
        opacity: [0, 1],
        translateY: [20, 0],
        easing: 'easeOutExpo',
        duration: 1200,
        delay: 1100
    });
    
    // Animación de las imágenes - entrando desde diferentes direcciones
    anime({
        targets: '.image-1',
        opacity: [0, 1],
        translateX: [50, 0],
        easing: 'easeOutQuad',
        duration: 1800,
        delay: 800
    });
    
    anime({
        targets: '.image-2',
        opacity: [0, 1],
        translateY: [30, 0],
        easing: 'easeOutQuad',
        duration: 1800,
        delay: 1100
    });
    
    anime({
        targets: '.image-3',
        opacity: [0, 1],
        translateX: [-30, 0],
        easing: 'easeOutQuad',
        duration: 1800,
        delay: 1400
    });
}

// Efecto de color deslizante mejorado
function animateColorSlider() {
    anime({
        targets: '.color-slider',
        translateX: ['0%', '50%'],
        easing: 'linear',
        duration: 20000,
        loop: true,
        direction: 'alternate'
    });
    
    // Animación adicional para la línea brillante
    anime({
        targets: '.glow-line',
        translateY: [-5, 5],
        opacity: [0.2, 0.4],
        easing: 'easeInOutSine',
        duration: 8000,
        loop: true,
        direction: 'alternate'
    });
}

// Animación de puntos de datos
function animateDataPoints() {
    const dataPoints = document.querySelectorAll('.data-point');
    
    dataPoints.forEach((point, index) => {
        // Aparición con retraso
        anime({
            targets: point,
            opacity: [0, 0.8],
            scale: [0, 1],
            easing: 'easeOutExpo',
            duration: 800,
            delay: 1500 + (index * 200)
        });
        
        // Pulso continuo
        anime({
            targets: point,
            scale: [1, 1.5],
            opacity: [0.8, 0.2],
            easing: 'easeInOutSine',
            duration: 1500 + (index * 500),
            loop: true,
            direction: 'alternate',
            delay: 2000 + (index * 200)
        });
    });
}

// Configurar efecto parallax mejorado en las imágenes según movimiento del ratón
function setupParallaxEffect() {
    document.addEventListener('mousemove', function(e) {
        const windowWidth = window.innerWidth;
        const windowHeight = window.innerHeight;
        
        const mouseX = e.clientX;
        const mouseY = e.clientY;
        
        // Calcular posición relativa del ratón (de -1 a 1)
        const xPos = (mouseX / windowWidth - 0.5) * 2;
        const yPos = (mouseY / windowHeight - 0.5) * 2;
        
        // Mover las imágenes con diferentes factores para dar sensación de profundidad
        const image1 = document.querySelector('.image-1');
        const image2 = document.querySelector('.image-2');
        const image3 = document.querySelector('.image-3');
        
        if (window.innerWidth > 992) { // Solo en pantallas grandes
            anime({
                targets: image1,
                translateX: xPos * 8,
                translateY: yPos * 8,
                duration: 1500,
                easing: 'easeOutQuad'
            });
            
            anime({
                targets: image2,
                translateX: xPos * 15,
                translateY: yPos * 15,
                duration: 1500,
                easing: 'easeOutQuad'
            });
            
            anime({
                targets: image3,
                translateX: xPos * -12,
                translateY: yPos * -12,
                duration: 1500,
                easing: 'easeOutQuad'
            });
        }
    });
}

// Configurar efecto de scroll para ocultar elementos de la primera sección
function setupScrollEffect() {
    // Elementos de la sección de presentación que se ocultarán
    const fadeElements = [
        '.animated-title', 
        '.animated-text', 
        '.cta-button', 
        '.image-1', 
        '.image-2', 
        '.image-3',
        '.data-point',
        '.color-slider',
        '.glow-line'
    ];
    
    // Altura de la ventana para calcular el porcentaje de scroll
    const windowHeight = window.innerHeight;
    
    // Función para manejar el evento de scroll
    window.addEventListener('scroll', function() {
        // Obtener la posición actual del scroll
        const scrollPosition = window.scrollY;
        
        // Calcular el porcentaje de scroll en relación a la primera sección
        // Asumimos que la primera sección tiene altura de 85vh como está en el CSS
        const sectionHeight = windowHeight * 0.85;
        
        // Calcular opacidad basada en el porcentaje de scroll
        // Cuanto más scroll hacia abajo, menor opacidad
        let opacity = 1 - (scrollPosition / sectionHeight);
        
        // Limitar la opacidad entre 0 y 1
        opacity = Math.max(0, Math.min(1, opacity));
        
        // Aplicar la opacidad a todos los elementos de la lista
        fadeElements.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(element => {
                element.style.opacity = opacity;
                
                // Añadir efecto de desplazamiento para algunos elementos
                if (['.animated-title', '.animated-text', '.cta-button'].includes(selector)) {
                    // Mover hacia arriba a medida que se hace scroll
                    const translateY = 50 * (1 - opacity);
                    element.style.transform = `translateY(${translateY}px)`;
                }
                
                if (['.image-1', '.image-2', '.image-3'].includes(selector)) {
                    // Escalar y desvanecer las imágenes
                    const scale = 1 - ((1 - opacity) * 0.1);
                    const currentTransform = element.style.transform || '';
                    
                    // Preservar cualquier transformación existente y añadir escala
                    if (!currentTransform.includes('scale')) {
                        element.style.transform = `${currentTransform} scale(${scale})`;
                    } else {
                        // Actualizar solo el valor de escala si ya existe
                        element.style.transform = currentTransform.replace(/scale\([^)]+\)/, `scale(${scale})`);
                    }
                }
            });
        });
        
        // Efecto para la sección completa si es necesario
        const presentacionSection = document.querySelector('.section-presentacion');
        if (scrollPosition > sectionHeight * 0.8) {
            // Cuando el scroll supera el 80% de la sección, añade blur
            const blurAmount = Math.min(5, (scrollPosition - sectionHeight * 0.8) / 20);
            presentacionSection.style.filter = `blur(${blurAmount}px)`;
        } else {
            presentacionSection.style.filter = 'none';
        }
    });
}

function descriptionEffect() {
    // Animación del título
    anime({
        targets: '.section-descrip-title h2',
        opacity: [0, 1],
        translateY: [-30, 0],
        easing: 'easeOutExpo',
        duration: 1200
    });
    
    anime({
        targets: '.title-underline',
        width: [0, '70px'],
        opacity: [0, 1],
        easing: 'easeInOutQuad',
        duration: 800,
        delay: 300
    });

    // Animación de las tarjetas - entrada con escalonamiento
    anime({
        targets: '.section-descrip-div',
        opacity: [0, 1],
        translateY: [60, 0],
        easing: 'easeOutExpo',
        duration: 1500,
        delay: anime.stagger(200)
    });

    // Animación inicial para los íconos con efecto rebote
    anime({
        targets: '.icon-container box-icon',
        scale: [0, 1],
        opacity: [0, 1],
        rotate: [-10, 0],
        easing: 'easeOutBack',
        duration: 1800,
        delay: anime.stagger(250, {start: 400})
    });
    
    // Animación sutil de pulsación para los íconos
    anime({
        targets: '.icon-container',
        scale: [1, 1.05, 1],
        opacity: [1, 0.95, 1],
        easing: 'easeInOutSine',
        duration: 3000,
        delay: function(el, i) { return i * 250 + 1500; },
        loop: true
    });
    
    // Configurar animaciones para eventos hover en tarjetas
    const cards = document.querySelectorAll('.section-descrip-div');
    
    cards.forEach(card => {
        // Animación al entrar el mouse
        card.addEventListener('mouseenter', () => {
            anime({
                targets: card.querySelector('.icon-container'),
                scale: [1, 1.15],
                duration: 400,
                easing: 'easeOutQuad'
            });
            
            anime({
                targets: card.querySelector('box-icon'),
                rotate: [0, 15, -5, 0],
                duration: 800,
                easing: 'easeInOutBack'
            });
            
            anime({
                targets: card.querySelector('h3'),
                translateY: [0, -5],
                color: ['#333', '#3498db'],
                duration: 400,
                easing: 'easeOutQuad'
            });
        });
        
        // Animación al salir el mouse
        card.addEventListener('mouseleave', () => {
            anime({
                targets: card.querySelector('.icon-container'),
                scale: 1,
                duration: 400,
                easing: 'easeOutQuad'
            });
            
            anime({
                targets: card.querySelector('h3'),
                translateY: 0,
                color: '#333',
                duration: 400,
                easing: 'easeOutQuad'
            });
        });
    });
    
    // Añadir efecto de aparición al hacer scroll
    setupDescriptionScrollEffect();
}

// Efecto de aparición gradual para la sección de descripción
function setupDescriptionScrollEffect() {
    const descItems = document.querySelectorAll('.section-descrip-div');
    const descTitle = document.querySelector('.section-descrip-title');
    
    // Usar Intersection Observer para detectar cuando los elementos están en el viewport
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            // Si el elemento es visible en el viewport
            if (entry.isIntersecting) {
                // Añadir clase para activar animación
                entry.target.classList.add('visible');
                // Dejar de observar el elemento una vez que se ha mostrado
                observer.unobserve(entry.target);
            }
        });
    }, {
        root: null, // Viewport
        threshold: 0.2, // Cuando al menos el 20% del elemento es visible
        rootMargin: '0px 0px -100px 0px' // Añadir margen negativo para activar antes
    });
    
    // Observar título
    if (descTitle) {
        observer.observe(descTitle);
    }
    
    // Observar cada tarjeta
    descItems.forEach(item => {
        observer.observe(item);
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
                boxShadow: '0 0 20px rgba(52, 152, 219, 0.5)',
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