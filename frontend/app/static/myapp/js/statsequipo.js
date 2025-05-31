console.log("🚀 STATSEQUIPO.JS - VERSION FUNCIONAL CON DROPDOWN");

// Variables globales
let vistaActual = 'resumen';
let currentIndex = 0;

const estadisticas = [
    { field: 'fotmob_rating', label: 'Rating' },
    { field: 'goals_per_match', label: 'Goles por partido' },
    { field: 'goals_conceded_per_match', label: 'Menos goles recibidos' },
    { field: 'average_possession', label: 'Posesión (%)' },
    { field: 'clean_sheets', label: 'Vallas invictas' },
    { field: 'expected_goals_xg', label: 'xG' },
    { field: 'shots_on_target_per_match', label: 'Tiros al arco/partido' },
    { field: 'big_chances', label: 'Grandes chances' },
    { field: 'big_chances_missed', label: 'Grandes chances falladas' },
    { field: 'accurate_passes_per_match', label: 'Pases precisos/partido' },
    { field: 'accurate_long_balls_per_match', label: 'Pases largos precisos/partido' },
    { field: 'accurate_crosses_per_match', label: 'Centros precisos/partido' },
    { field: 'penalties_awarded', label: 'Penales a favor' },
    { field: 'touches_in_opposition_box', label: 'Toques en área rival' },
    { field: 'corners', label: 'Corners' },
    { field: 'xg_conceded', label: 'xG concedido' },
    { field: 'interceptions_per_match', label: 'Intercepciones/partido' },
    { field: 'successful_tackles_per_match', label: 'Entradas exitosas/partido' },
    { field: 'clearances_per_match', label: 'Despejes/partido' },
    { field: 'possession_won_final_3rd_per_match', label: 'Recuperaciones en 1/3 final/partido' },
    { field: 'saves_per_match', label: 'Atajadas/partido' },
    { field: 'fouls_per_match', label: 'Faltas/partido' },
    { field: 'yellow_cards', label: 'Amarillas' },
    { field: 'red_cards', label: 'Rojas' }
];

// Función principal para cambiar vista
function cambiarVista(vista) {
    console.log("🔄 Cambiando a vista:", vista);
    
    const vistaResumen = document.getElementById('vista-resumen');
    const vistaCompleta = document.getElementById('vista-completa');
    
    if (!vistaResumen || !vistaCompleta) {
        console.error("❌ Elementos no encontrados");
        return;
    }
    
    vistaActual = vista;
    
    if (vista === 'completa') {
        console.log("➡️ Activando vista completa");
        vistaResumen.style.display = 'none';
        vistaCompleta.style.display = 'block';
        cargarDatosCompleta();
    } else {
        console.log("⬅️ Activando vista resumen");
        vistaResumen.style.display = 'block';
        vistaCompleta.style.display = 'none';
    }
    
    actualizarBotones(vista);
}

// Función para actualizar botones
function actualizarBotones(vista) {
    const botonesResumen = document.querySelectorAll('[id*="btn-vista-resumen"]');
    const botonesCompleta = document.querySelectorAll('[id*="btn-vista-completa"]');
    
    botonesResumen.forEach(btn => btn.classList.remove('active'));
    botonesCompleta.forEach(btn => btn.classList.remove('active'));
    
    if (vista === 'resumen') {
        botonesResumen.forEach(btn => btn.classList.add('active'));
    } else {
        botonesCompleta.forEach(btn => btn.classList.add('active'));
    }
}

// Función para cargar datos en vista completa
function cargarDatosCompleta() {
    console.log("🔄 Cargando datos para vista completa");
    
    const rankingList = document.getElementById('ranking-list');
    if (!rankingList) return;
    
    rankingList.innerHTML = `
        <div style="color: white; padding: 20px; text-align: center;">
            <h3>🏆 Vista Completa Activada</h3>
            <p style="color: #a0a8c0; margin-top: 20px;">
                💡 Selecciona una estadística del dropdown para ver datos reales
            </p>
        </div>
    `;
    
    // 🔥 CONFIGURAR DROPDOWN AQUÍ DESPUÉS DE QUE SE MUESTRE LA VISTA COMPLETA
    setTimeout(() => {
        configurarDropdown();
    }, 100);
}

// 🔥 NUEVA FUNCIÓN: Configurar dropdown (MÁS SIMPLE)
function configurarDropdown() {
    console.log("🔧 === CONFIGURANDO DROPDOWN ===");
    
    const dropdown = document.getElementById('estadistica-select');
    
    if (!dropdown) {
        console.error("❌ Dropdown no encontrado!");
        
        // Debug: Buscar todos los selects
        const todosLosSelects = document.querySelectorAll('select');
        console.log("🔍 Selects encontrados:", todosLosSelects.length);
        todosLosSelects.forEach((select, i) => {
            console.log(`Select ${i}: ID="${select.id}", Class="${select.className}"`);
        });
        
        return;
    }
    
    console.log("✅ Dropdown encontrado!");
    console.log("📋 Opciones del dropdown:", dropdown.options.length);
    
    // 🔥 LISTENER DIRECTO Y SIMPLE
    dropdown.onchange = function() {
        const valor = this.value;
        console.log("🔥 DROPDOWN CAMBIÓ A:", valor);
        console.log("🔥 Texto seleccionado:", this.options[this.selectedIndex].text);
        
        if (valor && valor !== '') {
            console.log("✅ Valor válido, cargando datos...");
            cargarEstadisticaDelBackend(valor);
        } else {
            console.log("⚠️ Valor vacío");
        }
    };
    
    // 🔥 TAMBIÉN AGREGAR LISTENER CON addEventListener POR SI ACASO
    dropdown.addEventListener('change', function() {
        console.log("🔥 EVENT LISTENER TAMBIÉN FUNCIONÓ:", this.value);
    });
    
    console.log("✅ Dropdown configurado correctamente");
}

// Función para cargar estadística desde el backend
function cargarEstadisticaDelBackend(field) {
    console.log('=== CARGANDO DESDE BACKEND ===');
    console.log('Campo:', field);
    
    const rankingList = document.getElementById('ranking-list');
    const estadisticaActual = estadisticas.find(stat => stat.field === field);
    const labelEsperado = estadisticaActual ? estadisticaActual.label : field;
    
    // Actualizar labels inmediatamente
    const currentStatLabel = document.getElementById('current-stat-label');
    const valorHeader = document.getElementById('valor-header');
    const totalEquipos = document.getElementById('total-equipos');
    
    if (currentStatLabel) currentStatLabel.textContent = labelEsperado;
    if (valorHeader) valorHeader.textContent = labelEsperado;
    
    // Mostrar loading
    if (rankingList) {
        rankingList.innerHTML = `<div style="color: white; padding: 20px; text-align: center;">🔄 Cargando ${labelEsperado}...</div>`;
    }
    
    // Hacer petición al backend
    const url = `/stats_equipos/?format=json&estadistica=${field}`;
    console.log("🌐 Petición a:", url);
    
    fetch(url)
        .then(response => {
            console.log('📡 Response:', response.status);
            if (!response.ok) {
                throw new Error(`Error ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('📊 Datos recibidos:', data);
            
            if (data && data.equipos && data.equipos.length > 0) {
                mostrarRankingReal(data.equipos, data.label || labelEsperado);
                
                // Actualizar contador de equipos
                if (totalEquipos) {
                    totalEquipos.textContent = `${data.equipos.length} equipos`;
                }
            } else {
                mostrarSinDatos(labelEsperado);
            }
        })
        .catch(error => {
            console.error('❌ Error:', error);
            mostrarError(error.message, labelEsperado);
        });
}

// Función para mostrar ranking real
function mostrarRankingReal(equipos, label) {
    console.log('📊 Mostrando ranking real:', equipos.length, 'equipos');
    
    const rankingList = document.getElementById('ranking-list');
    if (!rankingList) return;
    
    let html = '';
    
    equipos.forEach((equipo, index) => {
        const position = index + 1;
        let icon = position;
        
        if (position <= 3) {
            icon = position === 1 ? '🥇' : position === 2 ? '🥈' : '🥉';
        }
        
        html += `
            <div style="margin: 8px 0; padding: 12px; background: rgba(52,152,219,0.1); border-radius: 5px; display: flex; justify-content: space-between; align-items: center; border-left: 3px solid #3498db;">
                <span style="color: white;">${icon} ${equipo.nombre}</span>
                <span style="font-weight: bold; color: #3498db;">${equipo.valor}</span>
            </div>
        `;
    });
    
    rankingList.innerHTML = html;
    console.log("✅ Ranking mostrado correctamente");
}

// Función para mostrar cuando no hay datos
function mostrarSinDatos(label) {
    const rankingList = document.getElementById('ranking-list');
    if (!rankingList) return;
    
    rankingList.innerHTML = `
        <div style="color: #ff6b6b; padding: 2rem; text-align: center;">
            ❌ No hay datos disponibles para: ${label}
        </div>
    `;
}

// Función para mostrar error
function mostrarError(error, label) {
    const rankingList = document.getElementById('ranking-list');
    if (!rankingList) return;
    
    rankingList.innerHTML = `
        <div style="color: #ff6b6b; padding: 2rem; text-align: center;">
            ❌ Error al cargar: ${label}
            <br><small>${error}</small>
        </div>
    `;
}

// Configurar event listeners para botones
function configurarListeners() {
    console.log("🔧 Configurando listeners de botones...");
    
    // Listeners de botones con delegación de eventos
    document.addEventListener('click', function(e) {
        const clickedElement = e.target;
        
        if (clickedElement.id && clickedElement.id.includes('btn-vista-resumen')) {
            e.preventDefault();
            e.stopPropagation();
            console.log("🖱️ Click resumen");
            cambiarVista('resumen');
        }
        
        if (clickedElement.id && clickedElement.id.includes('btn-vista-completa')) {
            e.preventDefault();
            e.stopPropagation();
            console.log("🖱️ Click completa");
            cambiarVista('completa');
        }
    });
    
    // Teclas de acceso directo
    document.addEventListener('keydown', function(e) {
        if (e.key === '1') {
            e.preventDefault();
            cambiarVista('resumen');
        } else if (e.key === '2') {
            e.preventDefault();
            cambiarVista('completa');
        }
    });
    
    console.log("✅ Listeners de botones configurados");
}

// Función para sobrescribir interferencias
function eliminarInterferencias() {
    window.cambiarVista = cambiarVista;
}

// Inicialización
function inicializar() {
    console.log("🚀 Inicializando...");
    
    eliminarInterferencias();
    configurarListeners();
    
    setTimeout(() => {
        cambiarVista('resumen');
        console.log("✅ Inicialización completada");
        console.log("💡 Usa teclas 1 (resumen) y 2 (completa)");
    }, 100);
}

// Ejecutar inmediatamente
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', inicializar);
} else {
    inicializar();
}

document.addEventListener('DOMContentLoaded', function() {
    setTimeout(() => {
        inicializar();
    }, 500);
});

// 🔥 FUNCIÓN GLOBAL PARA DEBUGGING
window.testDropdown = function() {
    console.log("🔍 === TEST DROPDOWN ===");
    
    const dropdown = document.getElementById('estadistica-select');
    
    if (dropdown) {
        console.log("✅ Dropdown encontrado");
        console.log("Valor actual:", dropdown.value);
        console.log("Opciones:", dropdown.options.length);
        
        // Forzar cambio para testing
        dropdown.value = 'average_possession';
        dropdown.onchange();
        
    } else {
        console.error("❌ Dropdown NO encontrado");
        
        // Buscar todos los elementos con 'select' en el nombre
        const elementos = document.querySelectorAll('*[id*="select"], select');
        console.log("Elementos tipo select encontrados:", elementos.length);
        elementos.forEach(el => {
            console.log(`- ID: ${el.id}, Tag: ${el.tagName}, Class: ${el.className}`);
        });
    }
};

console.log("✅ STATSEQUIPO.JS - FUNCIONAL CON DROPDOWN");
console.log("💡 Usa testDropdown() en consola para debugging");