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
        '/equipo/': {
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
    
    // Detectar si es página de equipo específico
    if (currentPath.match(/^\/equipo\/\d+\/$/)) {
        const equipoNombre = document.querySelector('.equipo-nombre-principal')?.textContent || 'Equipo';
        pageConfig[currentPath] = {
            icon: 'bx-football',
            title: equipoNombre,
            subtitle: '/ Detalle del Equipo'
        };
    }
    
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
    }
    
    // Marcar la opción activa en el sidebar
    markActiveMenuItem(currentPath);
    
    // Agregar efectos de hover mejorados
    addHeaderEffects();
    
    // CONFIGURAR BOTONES DE NAVEGACIÓN
    setupNavButtons();
});

// Función para configurar los botones de navegación
function setupNavButtons() {
    console.log("=== CONFIGURANDO BOTONES DE NAVEGACIÓN ===");
    
    const btnTablas = document.getElementById('btn-tablas');
    const btnStatsEquipo = document.getElementById('btn-stats-equipo');
    const btnStatsJugadores = document.getElementById('btn-stats-jugadores');
    
    // Detectar qué contenedores están disponibles
    const tablasContainer = document.getElementById('tablas-container');
    const infoContainer = document.getElementById('info-container');
    const statsEquipoContainer = document.getElementById('stats-equipos-container');
    const statsJugadoresContainer = document.getElementById('stats-jugadores-container');

    console.log("Elementos encontrados:", {
        btnTablas: !!btnTablas,
        btnStatsEquipo: !!btnStatsEquipo,
        btnStatsJugadores: !!btnStatsJugadores,
        tablasContainer: !!tablasContainer,
        infoContainer: !!infoContainer,
        statsEquipoContainer: !!statsEquipoContainer,
        statsJugadoresContainer: !!statsJugadoresContainer
    });

    // Función para quitar todas las clases active
    function removeAllActive() {
        btnTablas?.classList.remove('active');
        btnStatsEquipo?.classList.remove('active');
        btnStatsJugadores?.classList.remove('active');
    }

    // Función para ocultar todos los contenedores
    function hideAllContainers() {
        if (tablasContainer) tablasContainer.style.display = 'none';
        if (infoContainer) infoContainer.style.display = 'none';
        if (statsEquipoContainer) statsEquipoContainer.style.display = 'none';
        if (statsJugadoresContainer) statsJugadoresContainer.style.display = 'none';
    }

    // Botón principal (Tablas o Info General)
    if (btnTablas) {
        btnTablas.addEventListener('click', function(e) {
            e.preventDefault();
            console.log("=== BOTÓN PRINCIPAL CLICKEADO ===");
            removeAllActive();
            hideAllContainers();
            btnTablas.classList.add('active');
            
            // Mostrar el contenedor apropiado
            if (tablasContainer) {
                tablasContainer.style.display = '';
                console.log("Mostrando tablas-container");
            } else if (infoContainer) {
                infoContainer.style.display = '';
                console.log("Mostrando info-container");
            }
        });
    }

    // Botón Stats Equipos / Plantilla
    if (btnStatsEquipo) {
        btnStatsEquipo.addEventListener('click', function(e) {
            e.preventDefault();
            console.log("=== BOTÓN STATS EQUIPO CLICKEADO ===");
            removeAllActive();
            hideAllContainers();
            btnStatsEquipo.classList.add('active');
            if (statsEquipoContainer) statsEquipoContainer.style.display = '';

            // Cargar contenido dinámicamente si es necesario
            const currentPath = window.location.pathname;
            if (currentPath.includes('/ligas/') && !statsEquipoContainer.innerHTML.trim()) {
                console.log("Cargando stats equipos...");
                fetch('/stats_equipos/')
                    .then(res => res.text())
                    .then(html => {
                        statsEquipoContainer.innerHTML = html;
                        console.log("Stats equipos cargado");
                    })
                    .catch(err => {
                        console.error("Error cargando stats equipos:", err);
                    });
            }
        });
    }

    // Botón Stats Jugadores / Estadísticas
    if (btnStatsJugadores) {
        btnStatsJugadores.addEventListener('click', function(e) {
            e.preventDefault();
            console.log("=== BOTÓN STATS JUGADORES CLICKEADO ===");
            removeAllActive();
            hideAllContainers();
            btnStatsJugadores.classList.add('active');
            if (statsJugadoresContainer) statsJugadoresContainer.style.display = '';
            
            // Cargar contenido dinámicamente si es necesario
            const currentPath = window.location.pathname;
            if (currentPath.includes('/ligas/')) {
                console.log("🔄 Iniciando fetch a /stats_jugadores/");
                fetch('/stats_jugadores/')
                    .then(res => {
                        console.log("✅ Response recibida:", res.status, res.statusText);
                        return res.text();
                    })
                    .then(html => {
                        console.log("✅ HTML recibido (primeros 200 chars):", html.substring(0, 200));
                        statsJugadoresContainer.innerHTML = html;
                        console.log("✅ HTML insertado en container");
                    })
                    .catch(err => {
                        console.error("❌ Error en fetch:", err);
                        if (statsJugadoresContainer) {
                            statsJugadoresContainer.innerHTML = '<p style="color: red;">Error: ' + err.message + '</p>';
                        }
                    });
            }
        });
    }
}

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
        '/equipo/': 'a[href*="equipo"]',
        '/estadisticas/': 'a[href*="estadisticas"]',
        '/comparacion/': 'a[href*="comparacion"]',
        '/recomendacion/': 'a[href*="recomendacion"]',
        '/club/': 'a[href*="club"]',
        '/dashboard/': 'a[href*="dashboard"]',
        '/jugadores/': 'a[href*="jugadores"]',
        '/': 'a[href="/"]'
    };
    
    // Para páginas de equipo específico, marcar el enlace de equipos
    if (currentPath.match(/^\/equipo\/\d+\/$/)) {
        const activeLink = document.querySelector('a[href*="equipo"]');
        if (activeLink) {
            activeLink.classList.add('active');
            console.log("Elemento activo marcado para equipo:", activeLink.textContent.trim());
        }
        return;
    }
    
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
            
            console.log("Refrescando datos...");
        });
    }
    
    // Efecto de season selector
    const seasonSelector = document.querySelector('.season-selector');
    if (seasonSelector) {
        seasonSelector.addEventListener('change', function() {
            console.log("Temporada cambiada a:", this.value);
            
            this.style.transform = 'scale(1.05)';
            this.style.transition = 'transform 0.2s ease';
            
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 200);
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

// Exportar funciones para uso global
window.HeaderManager = {
    updatePageHeader,
    markActiveMenuItem
};

console.log("=== TOPNAV.JS INICIALIZADO ===");

