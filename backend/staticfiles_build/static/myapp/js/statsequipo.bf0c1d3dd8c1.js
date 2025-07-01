(function() {
    'use strict';
    
    // ✅ PREVENIR MÚLTIPLES CARGAS
    if (window.statsEquiposLoaded) {
        console.log("⚠️ StatsequipoJS ya cargado, saliendo");
        return;
    }
    window.statsEquiposLoaded = true;
    
    console.log("🚀 STATSEQUIPO.JS - VERSIÓN COMPLETA");
    
    // ✅ VARIABLES GLOBALES SIMPLES
    let vistaActual = 'resumen';
    
    // ✅ FUNCIÓN PARA CAMBIAR VISTA
    function cambiarVista(vista) {
        const vistaResumen = document.getElementById('vista-resumen');
        const vistaCompleta = document.getElementById('vista-completa');
        
        if (!vistaResumen || !vistaCompleta) {
            console.log("⚠️ Elementos de vista no encontrados");
            return;
        }
        
        if (vista === 'completa') {
            vistaResumen.style.display = 'none';
            vistaCompleta.style.display = 'block';
            console.log("📈 Vista completa activada");
        } else {
            vistaResumen.style.display = 'block';
            vistaCompleta.style.display = 'none';
            console.log("📋 Vista resumen activada");
        }
        
        vistaActual = vista;
        
        // Actualizar botones
        document.querySelectorAll('[id*="btn-vista-"]').forEach(btn => {
            btn.classList.remove('active');
        });
        
        if (vista === 'resumen') {
            document.querySelectorAll('[id*="btn-vista-resumen"]').forEach(btn => {
                btn.classList.add('active');
            });
        } else {
            document.querySelectorAll('[id*="btn-vista-completa"]').forEach(btn => {
                btn.classList.add('active');
            });
        }
    }
    
    // ✅ FUNCIÓN PARA HACER VISIBLE EL CONTENEDOR
    function mostrarStatsEquipos() {
        const container = document.getElementById('stats-equipos-container');
        if (container) {
            container.style.display = 'block';
            console.log("✅ Contenedor stats-equipos-container visible");
        } else {
            console.log("⚠️ Contenedor stats-equipos-container no encontrado");
        }
    }
    
    // ✅ FUNCIÓN MEJORADA PARA CARGAR DATOS
    window.cargarEstadistica = function(estadistica) {
        console.log("🔄 Iniciando carga de:", estadistica);
        
        // Hacer visible el contenedor primero
        mostrarStatsEquipos();
        
        // Buscar el elemento ranking-list (CORRECTO)
        const rankingList = document.getElementById('ranking-list');
        
        console.log("🔍 Elemento ranking-list:", rankingList);
        
        if (!rankingList) {
            console.error("❌ No se encontró elemento ranking-list");
            
            // Mostrar en alert temporal para debug
            alert("❌ No se encontró elemento ranking-list. Revisa el HTML.");
            
            // Buscar elementos similares
            console.log("🔍 Elementos con 'ranking':");
            document.querySelectorAll('[class*="ranking"], [id*="ranking"]').forEach(el => {
                console.log("  -", el.tagName, el.id, el.className);
            });
            
            return;
        }
        
        if (!estadistica) {
            console.log("⚠️ Estadística vacía");
            return;
        }
        
        // Mostrar loading
        rankingList.innerHTML = '<div class="loading">🔄 Cargando datos...</div>';
        
        console.log("🌐 Haciendo petición a:", `/stats_equipos/?format=json&estadistica=${estadistica}`);
        
        fetch(`/stats_equipos/?format=json&estadistica=${estadistica}`)
            .then(response => {
                console.log("📡 Response status:", response.status);
                return response.json();
            })
            .then(data => {
                console.log("✅ Datos recibidos:", data);
                
                if (data.error) {
                    rankingList.innerHTML = `<div class="error">❌ Error: ${data.error}</div>`;
                    return;
                }
                
                if (!data.equipos || data.equipos.length === 0) {
                    rankingList.innerHTML = '<div class="error">❌ No hay datos disponibles</div>';
                    return;
                }
                
                // ✅ GENERAR HTML USANDO LAS CLASES DEL CSS
                let html = '';
                data.equipos.forEach((equipo, index) => {
                    const posicion = index + 1;
                    let medalla = '';
                    
                    if (posicion === 1) medalla = '🥇';
                    else if (posicion === 2) medalla = '🥈';
                    else if (posicion === 3) medalla = '🥉';
                    else medalla = posicion;
                    
                    html += `
                        <div class="ranking-item">
                            <span class="position">${medalla}</span>
                            <span class="equipo-nombre">${equipo.nombre}</span>
                            <span class="valor">${equipo.valor_formatted}</span>
                        </div>
                    `;
                });
                
                rankingList.innerHTML = html;
                console.log(`✅ Mostrados ${data.equipos.length} equipos en ranking-list`);
                
                // Actualizar labels
                const currentStatLabel = document.getElementById('current-stat-label');
                const totalEquipos = document.getElementById('total-equipos');
                const valorHeader = document.getElementById('valor-header');
                
                if (currentStatLabel) {
                    currentStatLabel.textContent = data.label;
                    console.log("✅ current-stat-label actualizado");
                }
                if (totalEquipos) {
                    totalEquipos.textContent = `${data.total} equipos`;
                    console.log("✅ total-equipos actualizado");
                }
                if (valorHeader) {
                    valorHeader.textContent = data.label;
                    console.log("✅ valor-header actualizado");
                }
            })
            .catch(error => {
                console.error("❌ Error en fetch:", error);
                rankingList.innerHTML = `<div class="error">❌ Error de conexión: ${error.message}</div>`;
            });
    };
    
    // ✅ FUNCIÓN DE PRUEBA GLOBAL
    window.testBackend = function(estadistica = 'fotmob_rating') {
        console.log("🧪 === PROBANDO BACKEND ===");
        cargarEstadistica(estadistica);
    };
    
    // ✅ FUNCIÓN PARA CAMBIAR A VISTA COMPLETA Y CARGAR DATOS
    window.verStatsCompletos = function(estadistica = 'fotmob_rating') {
        console.log("🎯 Cambiando a vista completa y cargando:", estadistica);
        
        // Hacer visible el contenedor
        mostrarStatsEquipos();
        
        // Cambiar a vista completa
        cambiarVista('completa');
        
        // Cargar datos
        setTimeout(() => {
            cargarEstadistica(estadistica);
        }, 100);
    };
    
    // ✅ INICIALIZACIÓN
    document.addEventListener('DOMContentLoaded', function() {
        console.log("🚀 Inicializando StatsEquipos...");
        
        // Event listeners para botones (incluyendo los duplicados)
        document.addEventListener('click', function(e) {
            if (e.target.id && (e.target.id.includes('btn-vista-resumen') || e.target.id === 'btn-vista-resumen-2')) {
                e.preventDefault();
                cambiarVista('resumen');
            }
            if (e.target.id && (e.target.id.includes('btn-vista-completa') || e.target.id === 'btn-vista-completa-2')) {
                e.preventDefault();
                mostrarStatsEquipos();
                cambiarVista('completa');
            }
        });
        
        // Event listener para el dropdown
        const select = document.getElementById('estadistica-select');
        if (select) {
            select.addEventListener('change', function() {
                if (this.value) {
                    console.log("📊 Dropdown cambió a:", this.value);
                    cargarEstadistica(this.value);
                }
            });
            console.log("✅ Dropdown configurado");
        } else {
            console.log("⚠️ Dropdown estadistica-select no encontrado");
        }
        
        console.log("✅ StatsEquipos inicializado");
    });
    
})();

console.log("✅ StatsEquipos módulo cargado");
console.log("🧪 Usa testBackend('fotmob_rating') para probar");
console.log("🧪 Usa verStatsCompletos('fotmob_rating') para ver en pantalla");