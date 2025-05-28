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
    
    // NUEVA LÓGICA PARA LOS 3 BOTONES
    setupNavButtons();
});

// Función para configurar los botones de navegación
function setupNavButtons() {
    console.log("=== CONFIGURANDO BOTONES DE NAVEGACIÓN ===");
    
    const btnTablas = document.getElementById('btn-tablas');
    const btnStatsEquipo = document.getElementById('btn-stats-equipo');
    const btnStatsJugadores = document.getElementById('btn-stats-jugadores');
    const tablasContainer = document.getElementById('tablas-container');
    const statsEquipoContainer = document.getElementById('stats-equipos-container');
    const statsJugadoresContainer = document.getElementById('stats-jugadores-container');

    console.log("Elementos encontrados:", {
        btnTablas: !!btnTablas,
        btnStatsEquipo: !!btnStatsEquipo,
        btnStatsJugadores: !!btnStatsJugadores,
        tablasContainer: !!tablasContainer,
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
        if (statsEquipoContainer) statsEquipoContainer.style.display = 'none';
        if (statsJugadoresContainer) statsJugadoresContainer.style.display = 'none';
    }

    // Botón Tablas
    if (btnTablas) {
        btnTablas.addEventListener('click', function(e) {
            e.preventDefault();
            console.log("=== BOTÓN TABLAS CLICKEADO ===");
            removeAllActive();
            hideAllContainers();
            btnTablas.classList.add('active');
            if (tablasContainer) tablasContainer.style.display = '';
        });
    }

    // Botón Stats Equipos
    if (btnStatsEquipo) {
        btnStatsEquipo.addEventListener('click', function(e) {
            e.preventDefault();
            console.log("=== BOTÓN STATS EQUIPO CLICKEADO ===");
            removeAllActive();
            hideAllContainers();
            btnStatsEquipo.classList.add('active');
            if (statsEquipoContainer) statsEquipoContainer.style.display = '';

            // Cargar contenido si no existe
            if (!statsEquipoContainer.innerHTML.trim()) {
                console.log("Cargando stats equipos...");
                fetch('/stats_equipos/')
                    .then(res => res.text())
                    .then(html => {
                        statsEquipoContainer.innerHTML = html;
                        console.log("Stats equipos cargado");
                        
                        // Cargar el script de stats equipos dinámicamente
                        const script = document.createElement('script');
                        script.src = "{% static 'myapp/js/statsequipo.js' %}";
                        script.onload = function() {
                            console.log("✅ Script statsequipo.js cargado dinámicamente");
                        };
                        document.head.appendChild(script);
                    })
                    .catch(err => {
                        console.error("Error cargando stats equipos:", err);
                    });
            }
        });
    }

    // Botón Stats Jugadores
    if (btnStatsJugadores) {
        btnStatsJugadores.addEventListener('click', function(e) {
            e.preventDefault();
            console.log("=== BOTÓN STATS JUGADORES CLICKEADO ===");
            console.log("btnStatsJugadores existe:", !!btnStatsJugadores);
            console.log("statsJugadoresContainer existe:", !!statsJugadoresContainer);
            
            removeAllActive();
            hideAllContainers();
            btnStatsJugadores.classList.add('active');
            if (statsJugadoresContainer) statsJugadoresContainer.style.display = '';
            
            // Debug del fetch
            console.log("🔄 Iniciando fetch a /stats_jugadores/");
            fetch('/stats_jugadores/')
                .then(res => {
                    console.log("✅ Response recibida:", res.status, res.statusText);
                    console.log("Response OK?", res.ok);
                    return res.text();
                })
                .then(html => {
                    console.log("✅ HTML recibido (primeros 200 chars):", html.substring(0, 200));
                    console.log("Longitud del HTML:", html.length);
                    statsJugadoresContainer.innerHTML = html;
                    console.log("✅ HTML insertado en container");
                })
                .catch(err => {
                    console.error("❌ Error en fetch:", err);
                    if (statsJugadoresContainer) {
                        statsJugadoresContainer.innerHTML = '<p style="color: red;">Error: ' + err.message + '</p>';
                    }
                });
        });
    } else {
        console.error("❌ btnStatsJugadores NO ENCONTRADO");
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

// Nuevos scripts para acciones en el navbar
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.nav-action-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (this.textContent.includes('Stats Equipo')) {
                e.preventDefault();
                fetch('/stats_equipos/')
                  .then(res => res.text())
                  .then(html => {
                      document.getElementById('stats-equipos-container').innerHTML = html;
                  });
            }
        });
    });
    
    const btnTablas = document.getElementById('btn-tablas');
    const btnStats = document.getElementById('btn-stats-equipo');
    const tablasContainer = document.getElementById('tablas-container');
    const statsContainer = document.getElementById('stats-equipos-container');

    btnTablas.addEventListener('click', function(e) {
        e.preventDefault();
        btnTablas.classList.add('active');
        btnStats.classList.remove('active');
        tablasContainer.style.display = '';
        statsContainer.style.display = 'none';
    });

    btnStats.addEventListener('click', function(e) {
        e.preventDefault();
        btnStats.classList.add('active');
        btnTablas.classList.remove('active');
        tablasContainer.style.display = 'none';
        statsContainer.style.display = '';
        // Solo carga una vez, si quieres recargar cada vez, quita el if
        if (!statsContainer.innerHTML.trim()) {
            fetch('/stats-equipos/')
                .then(res => res.text())
                .then(html => {
                    statsContainer.innerHTML = html;
                });
        }
    });
});

console.log("=== TOPNAV.JS INICIALIZADO ===");

