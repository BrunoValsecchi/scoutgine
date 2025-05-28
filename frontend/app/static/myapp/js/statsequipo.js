document.addEventListener('DOMContentLoaded', function() {
    console.log("=== STATSEQUIPO JAVASCRIPT CARGADO ===");
    
    // Elementos de control de vista
    const vistaResumen = document.getElementById('vista-resumen');
    const vistaCompleta = document.getElementById('vista-completa');
    const btnVistaResumen = document.getElementById('btn-vista-resumen');
    const btnVistaCompleta = document.getElementById('btn-vista-completa');
    const btnVistaResumen2 = document.getElementById('btn-vista-resumen-2');
    const btnVistaCompleta2 = document.getElementById('btn-vista-completa-2');
    
    console.log("🔍 Elementos encontrados:");
    console.log("- vistaResumen:", !!vistaResumen);
    console.log("- vistaCompleta:", !!vistaCompleta);
    console.log("- btnVistaResumen:", !!btnVistaResumen);
    console.log("- btnVistaCompleta:", !!btnVistaCompleta);
    console.log("- btnVistaResumen2:", !!btnVistaResumen2);
    console.log("- btnVistaCompleta2:", !!btnVistaCompleta2);
    
    // Elementos de vista completa
    const estadisticaSelect = document.getElementById('estadistica-select');
    const rankingList = document.getElementById('ranking-list');
    const currentStatLabel = document.getElementById('current-stat-label');
    const valorHeader = document.getElementById('valor-header');
    const statCounter = document.getElementById('stat-counter');
    const btnPrevStat = document.getElementById('btn-prev-stat');
    const btnNextStat = document.getElementById('btn-next-stat');

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

    // Función para cambiar vista
    function cambiarVista(vista) {
        console.log("🔄 Función cambiarVista:", vista);
        
        if (vista === 'completa') {
            console.log("➡️ Cambiando a vista completa");
            if (vistaResumen) vistaResumen.style.display = 'none';
            if (vistaCompleta) vistaCompleta.style.display = 'block';
            
            // Actualizar botones
            if (btnVistaResumen) btnVistaResumen.classList.remove('active');
            if (btnVistaCompleta) btnVistaCompleta.classList.add('active');
            if (btnVistaResumen2) btnVistaResumen2.classList.remove('active');
            if (btnVistaCompleta2) btnVistaCompleta2.classList.add('active');
            
        } else {
            console.log("⬅️ Cambiando a vista resumen");
            if (vistaResumen) vistaResumen.style.display = 'block';
            if (vistaCompleta) vistaCompleta.style.display = 'none';
            
            // Actualizar botones
            if (btnVistaResumen) btnVistaResumen.classList.add('active');
            if (btnVistaCompleta) btnVistaCompleta.classList.remove('active');
            if (btnVistaResumen2) btnVistaResumen2.classList.add('active');
            if (btnVistaCompleta2) btnVistaCompleta.classList.remove('active');
        }
    }

    // Función para cargar estadística
    function cargarEstadistica(field) {
        console.log('=== CARGANDO ESTADÍSTICA ===');
        console.log('Campo:', field);
        
        // Mostrar loading
        if (rankingList) {
            rankingList.innerHTML = '<div class="loading">🔄 Cargando...</div>';
        }
        
        // Hacer petición AJAX
        fetch(`/stats_equipos/?format=json&estadistica=${field}`)
            .then(response => {
                console.log('Response status:', response.status);
                console.log('Response OK:', response.ok);
                return response.json();
            })
            .then(data => {
                console.log('Datos recibidos:', data);
                if (data.equipos && data.equipos.length > 0) {
                    actualizarRanking(data.equipos, data.label);
                    actualizarContadores();
                } else {
                    console.error('No hay datos de equipos');
                    if (rankingList) rankingList.innerHTML = '<div class="error">❌ No hay datos disponibles</div>';
                }
            })
            .catch(err => {
                console.error('Error en fetch:', err);
                if (rankingList) {
                    rankingList.innerHTML = '<div class="error">❌ Error cargando datos: ' + err.message + '</div>';
                }
            });
    }

    // Función para actualizar ranking
    function actualizarRanking(equipos, label) {
        console.log('📊 Actualizando ranking con', equipos.length, 'equipos');
        
        if (currentStatLabel) currentStatLabel.textContent = label;
        if (valorHeader) valorHeader.textContent = label;
        
        let html = '';
        equipos.forEach((equipo, index) => {
            const position = index + 1;
            let positionIcon = position;
            
            if (position <= 3) {
                positionIcon = position === 1 ? '🥇' : position === 2 ? '🥈' : '🥉';
            }
            
            html += `
                <div class="ranking-item" data-position="${position}">
                    <span class="position">${positionIcon}</span>
                    <span class="equipo-info">
                        <span class="equipo-nombre">${equipo.nombre}</span>
                        <span class="equipo-liga">Primera División</span>
                    </span>
                    <span class="valor">${equipo.valor}</span>
                </div>
            `;
        });
        
        if (rankingList) {
            rankingList.innerHTML = html;
            
            // Animar entrada
            const items = rankingList.querySelectorAll('.ranking-item');
            items.forEach((item, index) => {
                item.style.animationDelay = `${index * 0.05}s`;
                item.classList.add('fade-in');
            });
        }
    }

    // Función para actualizar contadores
    function actualizarContadores() {
        if (statCounter) {
            statCounter.textContent = `${currentIndex + 1} / ${estadisticas.length}`;
        }
        
        if (btnPrevStat) {
            btnPrevStat.disabled = currentIndex === 0;
        }
        
        if (btnNextStat) {
            btnNextStat.disabled = currentIndex === estadisticas.length - 1;
        }
    }

    // Event Listeners para cambio de vista
    if (btnVistaCompleta) {
        btnVistaCompleta.addEventListener('click', function(e) {
            e.preventDefault();
            console.log("🖱️ Click en Vista Completa");
            cambiarVista('completa');
            cargarEstadistica(estadisticas[0].field); // Cargar primera estadística
        });
        console.log("✅ Event listener agregado a btnVistaCompleta");
    } else {
        console.error("❌ btnVistaCompleta no encontrado");
    }

    if (btnVistaResumen) {
        btnVistaResumen.addEventListener('click', function(e) {
            e.preventDefault();
            console.log("🖱️ Click en Vista Resumen");
            cambiarVista('resumen');
        });
        console.log("✅ Event listener agregado a btnVistaResumen");
    }

    // Event listeners para botones secundarios
    if (btnVistaCompleta2) {
        btnVistaCompleta2.addEventListener('click', function(e) {
            e.preventDefault();
            console.log("🖱️ Click en Vista Completa 2");
            cambiarVista('completa');
        });
    }

    if (btnVistaResumen2) {
        btnVistaResumen2.addEventListener('click', function(e) {
            e.preventDefault();
            console.log("🖱️ Click en Vista Resumen 2");
            cambiarVista('resumen');
        });
    }

    // Event listener para dropdown
    if (estadisticaSelect) {
        estadisticaSelect.addEventListener('change', function() {
            const selectedField = this.value;
            console.log("📊 Estadística seleccionada:", selectedField);
            currentIndex = estadisticas.findIndex(stat => stat.field === selectedField);
            cargarEstadistica(selectedField);
        });
    }

    // Event listeners para navegación
    if (btnPrevStat) {
        btnPrevStat.addEventListener('click', function() {
            console.log("⬅️ Botón anterior clickeado");
            if (currentIndex > 0) {
                currentIndex--;
                const field = estadisticas[currentIndex].field;
                estadisticaSelect.value = field;
                cargarEstadistica(field);
            }
        });
    }

    if (btnNextStat) {
        btnNextStat.addEventListener('click', function() {
            console.log("➡️ Botón siguiente clickeado");
            if (currentIndex < estadisticas.length - 1) {
                currentIndex++;
                const field = estadisticas[currentIndex].field;
                estadisticaSelect.value = field;
                cargarEstadistica(field);
            }
        });
    }

    // Inicializar contadores
    actualizarContadores();
    
    console.log("=== JAVASCRIPT INICIALIZADO ===");
});

// Ejecutar inmediatamente cuando se carga el script
(function() {
    console.log("=== STATSEQUIPO JAVASCRIPT INICIADO ===");
    
    // Función para inicializar cuando el DOM esté listo
    function initStatsEquipos() {
        console.log("🔄 Inicializando Stats Equipos...");
        
        // Elementos de control de vista
        const vistaResumen = document.getElementById('vista-resumen');
        const vistaCompleta = document.getElementById('vista-completa');
        const btnVistaResumen = document.getElementById('btn-vista-resumen');
        const btnVistaCompleta = document.getElementById('btn-vista-completa');
        const btnVistaResumen2 = document.getElementById('btn-vista-resumen-2');
        const btnVistaCompleta2 = document.getElementById('btn-vista-completa-2');
        
        console.log("🔍 Elementos encontrados:");
        console.log("- vistaResumen:", !!vistaResumen);
        console.log("- vistaCompleta:", !!vistaCompleta);
        console.log("- btnVistaResumen:", !!btnVistaResumen);
        console.log("- btnVistaCompleta:", !!btnVistaCompleta);
        console.log("- btnVistaResumen2:", !!btnVistaResumen2);
        console.log("- btnVistaCompleta2:", !!btnVistaCompleta2);
        
        // Elementos de vista completa
        const estadisticaSelect = document.getElementById('estadistica-select');
        const rankingList = document.getElementById('ranking-list');
        const currentStatLabel = document.getElementById('current-stat-label');
        const valorHeader = document.getElementById('valor-header');
        const statCounter = document.getElementById('stat-counter');
        const btnPrevStat = document.getElementById('btn-prev-stat');
        const btnNextStat = document.getElementById('btn-next-stat');

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

        // Función para cambiar vista
        function cambiarVista(vista) {
            console.log("🔄 Función cambiarVista:", vista);
            
            if (vista === 'completa') {
                console.log("➡️ Cambiando a vista completa");
                if (vistaResumen) vistaResumen.style.display = 'none';
                if (vistaCompleta) vistaCompleta.style.display = 'block';
                
                // Actualizar botones
                if (btnVistaResumen) btnVistaResumen.classList.remove('active');
                if (btnVistaCompleta) btnVistaCompleta.classList.add('active');
                if (btnVistaResumen2) btnVistaResumen2.classList.remove('active');
                if (btnVistaCompleta2) btnVistaCompleta2.classList.add('active');
                
            } else {
                console.log("⬅️ Cambiando a vista resumen");
                if (vistaResumen) vistaResumen.style.display = 'block';
                if (vistaCompleta) vistaCompleta.style.display = 'none';
                
                // Actualizar botones
                if (btnVistaResumen) btnVistaResumen.classList.add('active');
                if (btnVistaCompleta) btnVistaCompleta.classList.remove('active');
                if (btnVistaResumen2) btnVistaResumen2.classList.add('active');
                if (btnVistaCompleta2) btnVistaCompleta.classList.remove('active');
            }
        }

        // Función para cargar estadística
        function cargarEstadistica(field) {
            console.log('=== CARGANDO ESTADÍSTICA ===');
            console.log('Campo:', field);
            
            // Mostrar loading
            if (rankingList) {
                rankingList.innerHTML = '<div class="loading">🔄 Cargando...</div>';
            }
            
            // Hacer petición AJAX
            fetch(`/stats_equipos/?format=json&estadistica=${field}`)
                .then(response => {
                    console.log('Response status:', response.status);
                    console.log('Response OK:', response.ok);
                    return response.json();
                })
                .then(data => {
                    console.log('Datos recibidos:', data);
                    if (data.equipos && data.equipos.length > 0) {
                        actualizarRanking(data.equipos, data.label);
                        actualizarContadores();
                    } else {
                        console.error('No hay datos de equipos');
                        if (rankingList) rankingList.innerHTML = '<div class="error">❌ No hay datos disponibles</div>';
                    }
                })
                .catch(err => {
                    console.error('Error en fetch:', err);
                    if (rankingList) {
                        rankingList.innerHTML = '<div class="error">❌ Error cargando datos: ' + err.message + '</div>';
                    }
                });
        }

        // Función para actualizar ranking
        function actualizarRanking(equipos, label) {
            console.log('📊 Actualizando ranking con', equipos.length, 'equipos');
            
            if (currentStatLabel) currentStatLabel.textContent = label;
            if (valorHeader) valorHeader.textContent = label;
            
            let html = '';
            equipos.forEach((equipo, index) => {
                const position = index + 1;
                let positionIcon = position;
                
                if (position <= 3) {
                    positionIcon = position === 1 ? '🥇' : position === 2 ? '🥈' : '🥉';
                }
                
                html += `
                    <div class="ranking-item" data-position="${position}">
                        <span class="position">${positionIcon}</span>
                        <span class="equipo-info">
                            <span class="equipo-nombre">${equipo.nombre}</span>
                            <span class="equipo-liga">Primera División</span>
                        </span>
                        <span class="valor">${equipo.valor}</span>
                    </div>
                `;
            });
            
            if (rankingList) {
                rankingList.innerHTML = html;
                
                // Animar entrada
                const items = rankingList.querySelectorAll('.ranking-item');
                items.forEach((item, index) => {
                    item.style.animationDelay = `${index * 0.05}s`;
                    item.classList.add('fade-in');
                });
            }
        }

        // Función para actualizar contadores
        function actualizarContadores() {
            if (statCounter) {
                statCounter.textContent = `${currentIndex + 1} / ${estadisticas.length}`;
            }
            
            if (btnPrevStat) {
                btnPrevStat.disabled = currentIndex === 0;
            }
            
            if (btnNextStat) {
                btnNextStat.disabled = currentIndex === estadisticas.length - 1;
            }
        }

        // Event Listeners para cambio de vista
        if (btnVistaCompleta) {
            btnVistaCompleta.addEventListener('click', function(e) {
                e.preventDefault();
                console.log("🖱️ Click en Vista Completa");
                cambiarVista('completa');
                cargarEstadistica(estadisticas[0].field); // Cargar primera estadística
            });
            console.log("✅ Event listener agregado a btnVistaCompleta");
        } else {
            console.error("❌ btnVistaCompleta no encontrado");
        }

        if (btnVistaResumen) {
            btnVistaResumen.addEventListener('click', function(e) {
                e.preventDefault();
                console.log("🖱️ Click en Vista Resumen");
                cambiarVista('resumen');
            });
            console.log("✅ Event listener agregado a btnVistaResumen");
        }

        // Event listeners para botones secundarios
        if (btnVistaCompleta2) {
            btnVistaCompleta2.addEventListener('click', function(e) {
                e.preventDefault();
                console.log("🖱️ Click en Vista Completa 2");
                cambiarVista('completa');
            });
        }

        if (btnVistaResumen2) {
            btnVistaResumen2.addEventListener('click', function(e) {
                e.preventDefault();
                console.log("🖱️ Click en Vista Resumen 2");
                cambiarVista('resumen');
            });
        }

        // Event listener para dropdown
        if (estadisticaSelect) {
            estadisticaSelect.addEventListener('change', function() {
                const selectedField = this.value;
                console.log("📊 Estadística seleccionada:", selectedField);
                currentIndex = estadisticas.findIndex(stat => stat.field === selectedField);
                cargarEstadistica(selectedField);
            });
        }

        // Event listeners para navegación
        if (btnPrevStat) {
            btnPrevStat.addEventListener('click', function() {
                console.log("⬅️ Botón anterior clickeado");
                if (currentIndex > 0) {
                    currentIndex--;
                    const field = estadisticas[currentIndex].field;
                    estadisticaSelect.value = field;
                    cargarEstadistica(field);
                }
            });
        }

        if (btnNextStat) {
            btnNextStat.addEventListener('click', function() {
                console.log("➡️ Botón siguiente clickeado");
                if (currentIndex < estadisticas.length - 1) {
                    currentIndex++;
                    const field = estadisticas[currentIndex].field;
                    estadisticaSelect.value = field;
                    cargarEstadistica(field);
                }
            });
        }

        // Inicializar contadores
        actualizarContadores();
        
        console.log("✅ Stats Equipos inicializado correctamente");
    }

    // Verificar si el DOM ya está cargado
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initStatsEquipos);
    } else {
        // DOM ya está cargado
        initStatsEquipos();
    }

    // También ejecutar cuando se carga contenido dinámico
    document.addEventListener('statsEquiposLoaded', initStatsEquipos);
    
})();