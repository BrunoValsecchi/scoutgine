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
    
    // Detectar si es página de jugador específico
    if (currentPath.match(/^\/jugador\/\d+\/$/)) {
        const jugadorNombre = document.querySelector('.player-name')?.textContent || 
                             document.querySelector('.jugador-nombre')?.textContent || 'Jugador';
        pageConfig[currentPath] = {
            icon: 'bx-user',
            title: jugadorNombre,
            subtitle: '/ Perfil del Jugador'
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
    
    const currentPath = window.location.pathname;
    
    // CONFIGURACIÓN PARA PÁGINAS DE LIGAS Y EQUIPOS
    if (currentPath.includes('/ligas/') || currentPath.match(/^\/equipo\/\d+\/$/)) {
        setupLigasEquiposButtons();
    }
    
    // CONFIGURACIÓN PARA PÁGINAS DE COMPARACIÓN
    if (currentPath.includes('/comparacion/')) {
        setupComparacionButtons();
    }
    
    // CONFIGURACIÓN PARA PÁGINAS DE JUGADORES
    if (currentPath.match(/^\/jugador\/\d+\/$/)) {
        setupJugadorButtons();
    }
    
    // CONFIGURACIÓN PARA PÁGINAS DE ESTADÍSTICAS
    if (currentPath.includes('/estadisticas/')) {
        setupEstadisticasButtons();
    }
}

// Configuración para ligas y equipos (existente)
function setupLigasEquiposButtons() {
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

// NUEVA: Configuración para páginas de comparación
function setupComparacionButtons() {
    console.log("=== CONFIGURANDO BOTONES DE COMPARACIÓN ===");
    
    const btnEquipos = document.getElementById('btn-equipos');
    const btnJugadores = document.getElementById('btn-jugadores');
    
    // Contenedores (ahora ambos están en el HTML)
    const equiposContainer = document.getElementById('equipos-comparacion-container');
    const jugadoresContainer = document.getElementById('jugadores-comparacion-container');

    console.log("Elementos de comparación encontrados:", {
        btnEquipos: !!btnEquipos,
        btnJugadores: !!btnJugadores,
        equiposContainer: !!equiposContainer,
        jugadoresContainer: !!jugadoresContainer
    });

    function removeAllActiveComparacion() {
        btnEquipos?.classList.remove('active');
        btnJugadores?.classList.remove('active');
    }

    function hideAllContainersComparacion() {
        if (equiposContainer) equiposContainer.style.display = 'none';
        if (jugadoresContainer) jugadoresContainer.style.display = 'none';
    }

    // Botón Equipos
    if (btnEquipos) {
        btnEquipos.addEventListener('click', function(e) {
            e.preventDefault();
            console.log("=== BOTÓN EQUIPOS CLICKEADO ===");
            removeAllActiveComparacion();
            hideAllContainersComparacion();
            btnEquipos.classList.add('active');
            
            if (equiposContainer) {
                equiposContainer.style.display = '';
                console.log("✅ Mostrando comparación de equipos");
            }
            
            // Actualizar header
            if (window.HeaderManager) {
                window.HeaderManager.updatePageHeader('bx-scatter-chart', 'Comparación de Equipos', '/ Análisis de Clubes');
            }
        });
    }

    // Botón Jugadores
    if (btnJugadores) {
        btnJugadores.addEventListener('click', function(e) {
            e.preventDefault();
            console.log("=== BOTÓN JUGADORES CLICKEADO ===");
            removeAllActiveComparacion();
            hideAllContainersComparacion();
            btnJugadores.classList.add('active');
            
            if (jugadoresContainer) {
                jugadoresContainer.style.display = '';
                console.log("✅ Mostrando comparación de jugadores");
            }
            
            // Actualizar header
            if (window.HeaderManager) {
                window.HeaderManager.updatePageHeader('bx-user', 'Comparación de Jugadores', '/ Análisis de Jugadores');
            }
        });
    }

    // Mostrar equipos por defecto
    if (btnEquipos && equiposContainer) {
        btnEquipos.classList.add('active');
        equiposContainer.style.display = '';
    }
}

// NUEVA: Configuración para páginas de jugadores (CORREGIDA)
function setupJugadorButtons() {
    console.log("=== CONFIGURANDO BOTONES DE JUGADOR ===");
    
    const btnInfo = document.getElementById('btn-info');
    const btnStats = document.getElementById('btn-stats');
    
    // Contenedores principales
    const infoContainer = document.getElementById('info-container');
    const statsContainer = document.getElementById('stats-container');

    console.log("Elementos encontrados:", {
        btnInfo: !!btnInfo,
        btnStats: !!btnStats,
        infoContainer: !!infoContainer,
        statsContainer: !!statsContainer
    });

    function removeAllActive() {
        btnInfo?.classList.remove('active');
        btnStats?.classList.remove('active');
    }

    function showInfo() {
        console.log("📋 Mostrando información");
        removeAllActive();
        btnInfo?.classList.add('active');
        
        // Mostrar información, ocultar estadísticas
        if (infoContainer) {
            infoContainer.style.display = '';
            console.log("✅ Info container mostrado");
        }
        if (statsContainer) {
            statsContainer.style.display = 'none';
            console.log("✅ Stats container ocultado");
        }
    }

    function showStats() {
        console.log("📊 Mostrando estadísticas");
        removeAllActive();
        btnStats?.classList.add('active');
        
        // Ocultar información, mostrar estadísticas
        if (infoContainer) {
            infoContainer.style.display = 'none';
            console.log("✅ Info container ocultado");
        }
        if (statsContainer) {
            statsContainer.style.display = '';
            console.log("✅ Stats container mostrado");
        }
    }

    // Event listeners
    if (btnInfo) {
        btnInfo.addEventListener('click', function(e) {
            e.preventDefault();
            console.log("🖱️ Click en botón INFO");
            showInfo();
        });
    }

    if (btnStats) {
        btnStats.addEventListener('click', function(e) {
            e.preventDefault();
            console.log("🖱️ Click en botón STATS");
            showStats();
        });
    }

    // Mostrar información por defecto
    showInfo();
}

// NUEVA: Configuración para páginas de estadísticas
function setupEstadisticasButtons() {
    console.log("=== CONFIGURANDO BOTONES DE ESTADÍSTICAS ===");
    
    const btnGeneral = document.getElementById('btn-general');
    const btnOfensivo = document.getElementById('btn-ofensivo');
    const btnDefensivo = document.getElementById('btn-defensivo');
    const btnPortero = document.getElementById('btn-portero');
    
    // Contenedores
    const generalContainer = document.getElementById('general-container');
    const ofensivoContainer = document.getElementById('ofensivo-container');
    const defensivoContainer = document.getElementById('defensivo-container');
    const porteroContainer = document.getElementById('portero-container');

    console.log("Elementos de estadísticas encontrados:", {
        btnGeneral: !!btnGeneral,
        btnOfensivo: !!btnOfensivo,
        btnDefensivo: !!btnDefensivo,
        btnPortero: !!btnPortero,
        generalContainer: !!generalContainer,
        ofensivoContainer: !!ofensivoContainer,
        defensivoContainer: !!defensivoContainer,
        porteroContainer: !!porteroContainer
    });

    function removeAllActiveStats() {
        btnGeneral?.classList.remove('active');
        btnOfensivo?.classList.remove('active');
        btnDefensivo?.classList.remove('active');
        btnPortero?.classList.remove('active');
    }

    function hideAllContainersStats() {
        if (generalContainer) generalContainer.style.display = 'none';
        if (ofensivoContainer) ofensivoContainer.style.display = 'none';
        if (defensivoContainer) defensivoContainer.style.display = 'none';
        if (porteroContainer) porteroContainer.style.display = 'none';
    }

    // Botón General
    if (btnGeneral) {
        btnGeneral.addEventListener('click', function(e) {
            e.preventDefault();
            console.log("=== BOTÓN GENERAL CLICKEADO ===");
            removeAllActiveStats();
            hideAllContainersStats();
            btnGeneral.classList.add('active');
            if (generalContainer) generalContainer.style.display = '';
        });
    }

    // Botón Ofensivo
    if (btnOfensivo) {
        btnOfensivo.addEventListener('click', function(e) {
            e.preventDefault();
            console.log("=== BOTÓN OFENSIVO CLICKEADO ===");
            removeAllActiveStats();
            hideAllContainersStats();
            btnOfensivo.classList.add('active');
            if (ofensivoContainer) ofensivoContainer.style.display = '';
        });
    }

    // Botón Defensivo
    if (btnDefensivo) {
        btnDefensivo.addEventListener('click', function(e) {
            e.preventDefault();
            console.log("=== BOTÓN DEFENSIVO CLICKEADO ===");
            removeAllActiveStats();
            hideAllContainersStats();
            btnDefensivo.classList.add('active');
            if (defensivoContainer) defensivoContainer.style.display = '';
        });
    }

    // Botón Portero
    if (btnPortero) {
        btnPortero.addEventListener('click', function(e) {
            e.preventDefault();
            console.log("=== BOTÓN PORTERO CLICKEADO ===");
            removeAllActiveStats();
            hideAllContainersStats();
            btnPortero.classList.add('active');
            if (porteroContainer) porteroContainer.style.display = '';
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
    
    // Para páginas de jugador específico, marcar el enlace de jugadores
    if (currentPath.match(/^\/jugador\/\d+\/$/)) {
        const activeLink = document.querySelector('a[href*="jugadores"]');
        if (activeLink) {
            activeLink.classList.add('active');
            console.log("Elemento activo marcado para jugador:", activeLink.textContent.trim());
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

