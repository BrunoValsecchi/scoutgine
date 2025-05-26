console.log("=== TOPNAV.JS CARGADO ===");

// JavaScript para cambiar el header dinámicamente
document.addEventListener('DOMContentLoaded', function() {
    console.log("=== HEADER DOM LOADED ===");
    
    const currentPath = window.location.pathname;
    console.log("Ruta actual:", currentPath);
    
    // Configuración de páginas
    const pageConfig = {
        '/ligas/': {
            icon: 'bx-trophy',
            title: 'Tabla de Posiciones',
            subtitle: '/ Ligas Principales'
        },
        '/equipos/': {
            icon: 'bx-football',
            title: 'Equipos',
            subtitle: '/ Gestión de Clubes'
        },
        '/estadisticas/': {
            icon: 'bx-line-chart',
            title: 'Estadísticas',
            subtitle: '/ Análisis de Datos'
        },
        '/comparacion/': {
            icon: 'bx-scatter-chart',
            title: 'Comparación',
            subtitle: '/ Análisis de Jugadores'
        },
        '/recomendacion/': {
            icon: 'bx-user-pin',
            title: 'Recomendaciones',
            subtitle: '/ Sistema de Sugerencias'
        },
        '/club/': {
            icon: 'bx-badge-check',
            title: 'Club Favorito',
            subtitle: '/ Configuración Personal'
        },
        '/dashboard/': {
            icon: 'bx-home',
            title: 'Dashboard',
            subtitle: '/ Panel Principal'
        },
        '/jugadores/': {
            icon: 'bx-user',
            title: 'Jugadores',
            subtitle: '/ Base de Datos'
        },
        '/': {
            icon: 'bx-home',
            title: 'ScoutGine',
            subtitle: '/ Inicio'
        }
    };
    
    console.log("Configuraciones disponibles:", Object.keys(pageConfig));
    
    // Actualizar header si existe configuración
    if (pageConfig[currentPath]) {
        const config = pageConfig[currentPath];
        console.log("Aplicando configuración:", config);
        
        // Buscar elementos del DOM
        const pageIcon = document.querySelector('.page-icon');
        const pageTitle = document.querySelector('.page-title');
        const pageSubtitle = document.querySelector('.page-subtitle');
        
        if (pageIcon) {
            pageIcon.className = `bx ${config.icon} page-icon`;
            console.log("Icono actualizado:", config.icon);
        } else {
            console.warn("Elemento .page-icon no encontrado");
        }
        
        if (pageTitle) {
            pageTitle.textContent = config.title;
            console.log("Título actualizado:", config.title);
        } else {
            console.warn("Elemento .page-title no encontrado");
        }
        
        if (pageSubtitle) {
            pageSubtitle.textContent = config.subtitle;
            console.log("Subtítulo actualizado:", config.subtitle);
        } else {
            console.warn("Elemento .page-subtitle no encontrado");
        }
        
    } else {
        console.warn("No hay configuración para la ruta:", currentPath);
        
        // Configuración por defecto si no se encuentra la ruta
        const pageIcon = document.querySelector('.page-icon');
        const pageTitle = document.querySelector('.page-title');
        const pageSubtitle = document.querySelector('.page-subtitle');
        
        if (pageIcon) pageIcon.className = 'bx bx-home page-icon';
        if (pageTitle) pageTitle.textContent = 'ScoutGine';
        if (pageSubtitle) pageSubtitle.textContent = '/ Panel Principal';
    }
    
    // Marcar la opción activa en el sidebar
    markActiveMenuItem(currentPath);
    
    // Agregar efectos de hover mejorados
    addHeaderEffects();
});

// Función para marcar el elemento activo en el sidebar
function markActiveMenuItem(currentPath) {
    console.log("Marcando elemento activo para:", currentPath);
    
    // Quitar clase active de todos los enlaces
    const menuLinks = document.querySelectorAll('.menu a');
    menuLinks.forEach(link => {
        link.classList.remove('active');
    });
    
    // Mapeo de rutas a selectores
    const routeMapping = {
        '/ligas/': 'a[href*="ligas"]',
        '/equipos/': 'a[href*="equipos"]',
        '/estadisticas/': 'a[href*="estadisticas"]',
        '/comparacion/': 'a[href*="comparacion"]',
        '/recomendacion/': 'a[href*="recomendacion"]',
        '/club/': 'a[href*="club"]',
        '/dashboard/': 'a[href*="dashboard"]',
        '/jugadores/': 'a[href*="jugadores"]',
        '/': 'a[href="/"]'
    };
    
    // Agregar clase active al enlace correspondiente
    if (routeMapping[currentPath]) {
        const activeLink = document.querySelector(routeMapping[currentPath]);
        if (activeLink) {
            activeLink.classList.add('active');
            console.log("Elemento activo marcado:", activeLink.textContent.trim());
        }
    }
}

// Función para agregar efectos dinámicos al header
function addHeaderEffects() {
    console.log("Agregando efectos al header");
    
    // Efecto de refresh button
    const refreshBtn = document.querySelector('.refresh-btn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            this.style.transform = 'rotate(360deg) scale(1.1)';
            this.style.transition = 'transform 0.6s ease';
            
            setTimeout(() => {
                this.style.transform = 'scale(1)';
                this.style.transition = 'transform 0.3s ease';
            }, 600);
            
            // Simular actualización
            console.log("Refrescando datos...");
        });
    }
    
    // Efecto de season selector
    const seasonSelector = document.querySelector('.season-selector');
    if (seasonSelector) {
        seasonSelector.addEventListener('change', function() {
            console.log("Temporada cambiada a:", this.value);
            
            // Efecto visual de cambio
            this.style.transform = 'scale(1.05)';
            this.style.transition = 'transform 0.2s ease';
            
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 200);
        });
    }
    
    // Efecto de typing en el título
    const pageTitle = document.querySelector('.page-title');
    if (pageTitle) {
        pageTitle.addEventListener('mouseenter', function() {
            this.style.textShadow = '0 4px 8px rgba(52, 152, 219, 0.4)';
            this.style.transition = 'text-shadow 0.3s ease';
        });
        
        pageTitle.addEventListener('mouseleave', function() {
            this.style.textShadow = '0 2px 4px rgba(0, 0, 0, 0.5)';
        });
    }
}

// Función para actualizar el breadcrumb desde otras páginas
function updatePageHeader(icon, title, subtitle) {
    console.log("Actualizando header manualmente:", { icon, title, subtitle });
    
    const pageIcon = document.querySelector('.page-icon');
    const pageTitle = document.querySelector('.page-title');
    const pageSubtitle = document.querySelector('.page-subtitle');
    
    if (pageIcon && icon) {
        pageIcon.className = `bx ${icon} page-icon`;
    }
    
    if (pageTitle && title) {
        pageTitle.textContent = title;
    }
    
    if (pageSubtitle && subtitle) {
        pageSubtitle.textContent = subtitle;
    }
}

// Función para animar la transición entre páginas
function animatePageTransition() {
    const topNav = document.querySelector('.top-nav');
    if (topNav) {
        topNav.style.opacity = '0.7';
        topNav.style.transform = 'translateY(-10px)';
        topNav.style.transition = 'all 0.3s ease';
        
        setTimeout(() => {
            topNav.style.opacity = '1';
            topNav.style.transform = 'translateY(0)';
        }, 300);
    }
}

// Exportar funciones para uso global
window.HeaderManager = {
    updatePageHeader,
    animatePageTransition,
    markActiveMenuItem
};

console.log("=== TOPNAV.JS INICIALIZADO ===");

