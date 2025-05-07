// Consolidated Animation System for Website
document.addEventListener('DOMContentLoaded', () => {
  // Check and load anime.js if not already included
  if (typeof anime === 'undefined') {
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/animejs/3.2.1/anime.min.js';
    script.onload = initAllAnimations;
    document.head.appendChild(script);
  } else {
    initAllAnimations();
  }

  function initAllAnimations() {
    // Initial entrance animations
    animateEntrance();
    
    // Header animations
    animateHeaderElements();
    
    // Section specific animations
    animateAppSection();
    animatePlansSection();
    animateDescriptionSection();
    
    // Background and decorative effects
    animateColorSlider();
    addParticleEffect();
    animateDataPoints();
    
    // Interactive effects
    setupParallaxEffect();
    setupScrollEffect();
    initScrollAnimations();
    animateFormElements();
  }
  
  // ----- ENTRANCE ANIMATIONS -----
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
  
  // ----- HEADER ANIMATIONS -----
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
          duration: 300,
          easing: 'easeOutQuad'
        });
      });
      
      ctaButton.addEventListener('mouseleave', function() {
        anime({
          targets: this,
          scale: 1,
          duration: 300,
          easing: 'easeOutQuad'
        });
      });
    }
  }
  
  // ----- APP SECTION ANIMATIONS -----
  function animateAppSection() {
    // Animación para el teléfono mockup
    anime({
      targets: '.phone-mockup, .app-preview',
      translateY: [50, 0],
      opacity: [0, 1],
      duration: 1200,
      easing: 'easeOutQuad',
      delay: 300
    });

    // Animación para los elementos del fondo
    anime({
      targets: '.circle-glow',
      scale: [0.8, 1],
      opacity: [0, 0.6],
      duration: 1500,
      easing: 'easeInOutQuad'
    });

    // Animación para la cuadrícula tecnológica
    anime({
      targets: '.tech-grid',
      opacity: [0, 0.3],
      duration: 2000,
      easing: 'easeInOutQuad'
    });

    // Animaciones para las características
    anime({
      targets: '.feature',
      translateX: [-30, 0],
      opacity: [0, 1],
      duration: 800,
      delay: anime.stagger(150, {start: 500}),
      easing: 'easeOutQuad'
    });

    // Animación para botones de descarga
    anime({
      targets: '.store-button',
      scale: [0.9, 1],
      opacity: [0, 1],
      duration: 600,
      delay: anime.stagger(200, {start: 1000}),
      easing: 'spring(1, 80, 10, 0)'
    });
    
    // Animación para el encabezado de la sección
    anime({
      targets: '.app-header h2',
      opacity: [0, 1],
      translateY: [-30, 0],
      duration: 1200,
      easing: 'easeOutExpo'
    });
    
    // Efecto de resplandor para el botón de enviar
    const submitButtonAnimation = anime({
      targets: '.submit-button::before',
      translateX: ['0%', '100%'],
      easing: 'easeInOutSine',
      duration: 1500,
      loop: true,
      autoplay: false
    });
    
    // Activar animación al pasar el ratón
    document.querySelector('.submit-button')?.addEventListener('mouseenter', () => {
      submitButtonAnimation.play();
    });
    
    document.querySelector('.submit-button')?.addEventListener('mouseleave', () => {
      submitButtonAnimation.pause();
    });
  }
  
  // ----- PLANES SECTION ANIMATIONS -----
  function animatePlansSection() {
    // Animación para el encabezado
    anime({
      targets: '.planes-header h2',
      translateY: [30, 0],
      opacity: [0, 1],
      duration: 1000,
      easing: 'easeOutQuad'
    });

    anime({
      targets: '.header-line, .title-underline',
      width: [0, 100],
      opacity: [0, 1],
      duration: 1000,
      delay: 300,
      easing: 'easeInOutQuad'
    });

    anime({
      targets: '.planes-subtitle',
      translateY: [20, 0],
      opacity: [0, 1],
      duration: 800,
      delay: 500,
      easing: 'easeOutQuad'
    });

    // Animación para las tarjetas de planes
    anime({
      targets: '.plan-card',
      translateY: [60, 0],
      opacity: [0, 1],
      duration: 1000,
      delay: anime.stagger(200, {start: 700}),
      easing: 'easeOutElastic(1, .8)'
    });

    // Animación especial para la tarjeta destacada
    
    // Animación para la insignia
    anime({
      targets: '.plan-badge',
      translateX: [20, 0],
      opacity: [0, 1],
      duration: 800,
      delay: 1200,
      easing: 'easeOutBack'
    });

    // Animación para la info adicional
    anime({
      targets: '.planes-info',
      translateY: [20, 0],
      opacity: [0, 1],
      duration: 800,
      delay: 1500,
      easing: 'easeOutQuad'
    });
    
    // Animación al hacer hover en las tarjetas
    document.querySelectorAll('.plan-card').forEach(card => {
      card.addEventListener('mouseenter', () => {
        anime({
          targets: card.querySelector('.plan-price .amount'),
          scale: [1, 1.1],
          duration: 400,
          easing: 'easeOutQuad'
        });
      });
      
      card.addEventListener('mouseleave', () => {
        anime({
          targets: card.querySelector('.plan-price .amount'),
          scale: [1.1, 1],
          duration: 400,
          easing: 'easeOutQuad'
        });
      });
    });
  }
  
  // ----- DESCRIPTION SECTION ANIMATIONS -----
  function animateDescriptionSection() {
    // Animación del título
    anime({
      targets: '.section-descrip-title h2',
      opacity: [0, 1],
      translateY: [-30, 0],
      easing: 'easeOutExpo',
      duration: 1200
    });
    
    anime({
      targets: '.section-descrip-title .title-underline',
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
  
  // ----- BACKGROUND AND DECORATIVE EFFECTS -----
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
  
  function addParticleEffect() {
    // Crear contenedor para partículas
    const appSection = document.querySelector('#app-download');
    if (!appSection) return;
    
    const particlesContainer = document.createElement('div');
    particlesContainer.className = 'particles-container';
    particlesContainer.style.cssText = `
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 1;
      overflow: hidden;
    `;
    appSection.appendChild(particlesContainer);
    
    // Crear partículas
    const particleCount = 15;
    for (let i = 0; i < particleCount; i++) {
      const particle = document.createElement('div');
      particle.className = 'tech-particle';
      particle.style.cssText = `
        position: absolute;
        width: ${Math.random() * 5 + 2}px;
        height: ${Math.random() * 5 + 2}px;
        background-color: rgba(52, 152, 219, ${Math.random() * 0.3 + 0.1});
        border-radius: 50%;
        pointer-events: none;
      `;
      particlesContainer.appendChild(particle);
      
      // Posición inicial aleatoria
      const xPos = Math.random() * 100;
      const yPos = Math.random() * 100;
      
      // Animación de flotación
      anime({
        targets: particle,
        translateX: [
          { value: `${xPos}%` },
          { value: `${xPos + (Math.random() * 20 - 10)}%` }
        ],
        translateY: [
          { value: `${yPos}%` },
          { value: `${yPos + (Math.random() * 20 - 10)}%` }
        ],
        opacity: [
          { value: 0 },
          { value: 1 },
          { value: 0 }
        ],
        scale: [
          { value: 0 },
          { value: 1 },
          { value: 0 }
        ],
        duration: Math.random() * 10000 + 8000,
        easing: 'easeInOutSine',
        loop: true,
        delay: Math.random() * 3000
      });
    }
  }
  
  function animateDataPoints() {
    const dataPoints = document.querySelectorAll('.data-point');
    
    // Si no hay puntos de datos, regresa
    if (!dataPoints.length) return;
    
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
    
    // Animación alternativa para puntos de datos (del primer archivo)
    anime({
      targets: '.data-point',
      opacity: [0, 0.8, 0],
      scale: [0, 1.2, 0],
      easing: 'easeInOutSine',
      duration: 3000,
      delay: anime.stagger(300),
      loop: true
    });
  }
  
  // ----- INTERACTIVE EFFECTS -----
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
      
      if (window.innerWidth > 992 && image1 && image2 && image3) { // Solo en pantallas grandes
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
      if (presentacionSection && scrollPosition > sectionHeight * 0.8) {
        // Cuando el scroll supera el 80% de la sección, añade blur
        const blurAmount = Math.min(5, (scrollPosition - sectionHeight * 0.8) / 20);
        presentacionSection.style.filter = `blur(${blurAmount}px)`;
      } else if (presentacionSection) {
        presentacionSection.style.filter = 'none';
      }
    });
  }
  
  // ----- SCROLL DETECTION ANIMATIONS -----
  function initScrollAnimations() {
    // Detectar elementos cuando entran en el viewport
    const observerOptions = {
      threshold: 0.2,
      rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          // Activar animaciones cuando la sección es visible
          if (entry.target.id === 'app-download') {
            animateAppSection();
          } else if (entry.target.id === 'planes') {
            animatePlansSection();
          } else if (entry.target.classList.contains('section-descrip')) {
            animateDescriptionSection();
          }
          
          // Dejar de observar después de animar
          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);
    
    // Observar las secciones
    const sections = document.querySelectorAll('#app-download, #planes, .section-descrip');
    sections.forEach(section => {
      observer.observe(section);
    });
  }
  
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
  
  // ----- FORM ELEMENT ANIMATIONS -----
  function animateFormElements() {
    // Efecto de entrada para los campos del formulario
    const inputFields = document.querySelectorAll('.input-group input, .input-group textarea');
    
    if (!inputFields.length) return;
    
    inputFields.forEach(input => {
      // Animación al enfocar
      input.addEventListener('focus', () => {
        anime({
          targets: input,
          borderColor: 'rgba(52, 152, 219, 0.8)',
          boxShadow: '0 0 0 3px rgba(52, 152, 219, 0.2)',
          duration: 300,
          easing: 'easeOutQuad'
        });
      });
      
      // Animación al desenfocar
      input.addEventListener('blur', () => {
        if (!input.value) {
          anime({
            targets: input,
            borderColor: 'rgba(255, 255, 255, 0.1)',
            boxShadow: '0 0 0 0px rgba(52, 152, 219, 0)',
            duration: 300,
            easing: 'easeOutQuad'
          });
        }
      });
    });
    
    // Animación de aparición del formulario
    anime({
      targets: '.contact-form-container',
      translateY: [40, 0],
      opacity: [0, 1],
      duration: 1000,
      delay: 300,
      easing: 'easeOutQuad'
    });
    
    // Animación para los campos de formulario
    anime({
      targets: '.input-group',
      translateY: [20, 0],
      opacity: [0, 1],
      duration: 800,
      delay: anime.stagger(100, {start: 600}),
      easing: 'easeOutQuad'
    });
  }
});