// JavaScript específico para páginas de equipos
console.log("=== EQUIPO.JS CARGADO ===");

document.addEventListener('DOMContentLoaded', function() {
    console.log("=== EQUIPO DOM LOADED ===");
    
    // Actualizar el título del header con el nombre del equipo
    const equipoNombre = document.querySelector('.equipo-nombre-principal');
    if (equipoNombre && window.HeaderManager) {
        const nombreEquipo = equipoNombre.textContent;
        window.HeaderManager.updatePageHeader(
            'bx-football',
            nombreEquipo,
            '/ Detalle del Equipo'
        );
        console.log("Header actualizado para equipo:", nombreEquipo);
    }
    
    // Efectos adicionales para la página de equipo
    setupEquipoEffects();
});

function setupEquipoEffects() {
    // Efecto hover en el logo del equipo
    const equipoLogo = document.querySelector('.equipo-logo-grande, .equipo-logo-placeholder-grande');
    if (equipoLogo) {
        equipoLogo.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05) rotate(2deg)';
            this.style.transition = 'transform 0.3s ease';
        });
        
        equipoLogo.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1) rotate(0deg)';
        });
    }
    
    // Efecto en las cards de información
    const infoCards = document.querySelectorAll('.info-card');
    infoCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.transition = 'transform 0.3s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    console.log("✅ Efectos de equipo configurados");
}

console.log("=== EQUIPO.JS INICIALIZADO ===");