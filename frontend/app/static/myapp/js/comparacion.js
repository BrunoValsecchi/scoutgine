document.addEventListener('DOMContentLoaded', function() {
    // ✅ VERIFICAR QUE NO SE EJECUTE MÚLTIPLES VECES
    if (window.comparacionInitialized) {
        return;
    }
    window.comparacionInitialized = true;
    
    // Verificar ECharts
    if (typeof echarts === 'undefined') {
        console.error('❌ ECharts no disponible');
        return;
    }
    
    // Verificar elementos de datos
    const equiposDataElement = document.getElementById('equipos-data');
    const gruposEquiposElement = document.getElementById('grupos-stats-equipos-data');
    
    if (!equiposDataElement || !gruposEquiposElement) {
        console.error('❌ Elementos de datos no encontrados');
        return;
    }
    
    // ✅ PARSEAR DATOS
    let equiposData, gruposEquipos;
    
    try {
        equiposData = JSON.parse(equiposDataElement.textContent.trim());
        gruposEquipos = JSON.parse(gruposEquiposElement.textContent.trim());
    } catch (error) {
        console.error('❌ Error parseando datos:', error);
        return;
    }
    
    // ✅ INICIALIZAR ECHARTS CON DIMENSIONES MÁS COMPACTAS
    const chartContainer = document.getElementById('radar-comparacion-equipos');
    if (!chartContainer) {
        console.error('❌ Contenedor del gráfico no encontrado');
        return;
    }

    chartContainer.style.width = '100%';
    chartContainer.style.maxWidth = '550px';
    chartContainer.style.height = '480px';
    chartContainer.style.margin = '0 auto';

    const myChart = echarts.init(chartContainer, null, {devicePixelRatio: 2});
    
    // ✅ VARIABLES GLOBALES PARA EL TOOLTIP Y MODO
    let equiposActuales = {};
    let grupoActual = 'Ofensivos';
    let modoActual = 'graficos'; // 'graficos' o 'estadisticas'
    
    // ✅ ELEMENTOS DOM
    const btnGraficos = document.getElementById('btn-graficos-equipos');
    const btnEstadisticas = document.getElementById('btn-estadisticas-equipos');
    const containerGrafico = document.getElementById('radar-comparacion-equipos');
    const containerEstadisticas = document.getElementById('estadisticas-comparacion-equipos');
    const grupoSelector = document.getElementById('grupo-select-equipos'); // ✅ AÑADIR REFERENCIA
    
    // ✅ FUNCIÓN PARA CAMBIAR MODO
    function cambiarModo(modo) {
        modoActual = modo;
        
        if (modo === 'graficos') {
            btnGraficos.classList.add('modo-activo');
            btnEstadisticas.classList.remove('modo-activo');
            containerGrafico.style.display = 'block';
            containerEstadisticas.style.display = 'none';
            
            // ✅ MOSTRAR SELECTOR DE GRUPOS EN MODO GRÁFICO
            if (grupoSelector && grupoSelector.parentElement) {
                grupoSelector.parentElement.style.display = 'block';
            }
            
        } else {
            btnEstadisticas.classList.add('modo-activo');
            btnGraficos.classList.remove('modo-activo');
            containerGrafico.style.display = 'none';
            containerEstadisticas.style.display = 'block';
            
            // ✅ OCULTAR SELECTOR DE GRUPOS EN MODO ESTADÍSTICAS
            if (grupoSelector && grupoSelector.parentElement) {
                grupoSelector.parentElement.style.display = 'none';
            }
        }
        
        // ✅ ACTUALIZAR VISTA SEGÚN EQUIPOS SELECCIONADOS
        actualizarVista();
    }
    
    // ✅ FUNCIÓN PARA ACTUALIZAR VISTA
    function actualizarVista() {
        const selectEquipo1 = document.getElementById('equipo1-select');
        const selectEquipo2 = document.getElementById('equipo2-select');
        
        if (!selectEquipo1 || !selectEquipo2) {
            return;
        }
        
        const equipoId1 = parseInt(selectEquipo1.value);
        const equipoId2 = parseInt(selectEquipo2.value);
        
        if (!equipoId1 || !equipoId2 || equipoId1 === equipoId2) {
            if (modoActual === 'graficos') {
                myChart.clear();
            } else {
                containerEstadisticas.innerHTML = '<div class="no-data">Selecciona dos equipos diferentes para comparar</div>';
            }
            return;
        }
        
        const equipo1 = equiposData.find(e => e.id === equipoId1);
        const equipo2 = equiposData.find(e => e.id === equipoId2);
        
        if (!equipo1 || !equipo2) {
            return;
        }
        
        if (modoActual === 'graficos') {
            generarGraficoRadar(equipo1, equipo2, gruposEquipos);
        } else {
            generarTablaEstadisticas(equipo1, equipo2, gruposEquipos);
        }
    }
    
    // ✅ FUNCIÓN PARA GENERAR TABLA DE ESTADÍSTICAS - TODAS JUNTAS
    function generarTablaEstadisticas(equipo1, equipo2, grupos) {
        let html = `
            <div class="estadisticas-header">
                <h3>Comparación Completa: ${equipo1.nombre} vs ${equipo2.nombre}</h3>
            </div>
            <div class="tabla-comparacion">
        `;
        
        // ✅ ITERAR POR CADA GRUPO DE ESTADÍSTICAS
        Object.entries(grupos).forEach(([nombreGrupo, estadisticasGrupo]) => {
            html += `
                <div class="grupo-estadisticas">
                    <h4 class="grupo-titulo">${nombreGrupo}</h4>
                    <table class="stats-table">
                        <thead>
                            <tr>
                                <th>Estadística</th>
                                <th class="equipo-col equipo1-col">${equipo1.nombre}</th>
                                <th class="equipo-col equipo2-col">${equipo2.nombre}</th>
                                <th>Diferencia</th>
                            </tr>
                        </thead>
                        <tbody>
            `;
            
            // ✅ ITERAR POR CADA ESTADÍSTICA DEL GRUPO
            estadisticasGrupo.forEach(([nombre, campo]) => {
                const valor1 = equipo1[campo] || 0;
                const valor2 = equipo2[campo] || 0;
                const percentil1 = equipo1[`${campo}_percentil`] || 50;
                const percentil2 = equipo2[`${campo}_percentil`] || 50;
                
                const diferencia = (valor1 - valor2).toFixed(2);
                const diferenciaClass = diferencia > 0 ? 'positiva' : diferencia < 0 ? 'negativa' : 'neutra';
                const diferenciaSymbol = diferencia > 0 ? '+' : '';
                
                // ✅ DETERMINAR CUÁL EQUIPO ES MEJOR EN ESTA ESTADÍSTICA
                const equipo1Mejor = valor1 > valor2;
                const equipo2Mejor = valor2 > valor1;
                
                html += `
                    <tr>
                        <td class="stat-name">${nombre}</td>
                        <td class="stat-value equipo1-col ${equipo1Mejor ? 'mejor-valor' : ''}">
                            <div class="valor-principal">${valor1}</div>
                            <div class="percentil">P${percentil1}</div>
                        </td>
                        <td class="stat-value equipo2-col ${equipo2Mejor ? 'mejor-valor' : ''}">
                            <div class="valor-principal">${valor2}</div>
                            <div class="percentil">P${percentil2}</div>
                        </td>
                        <td class="diferencia ${diferenciaClass}">
                            ${diferenciaSymbol}${diferencia}
                        </td>
                    </tr>
                `;
            });
            
            html += `
                        </tbody>
                    </table>
                </div>
            `;
        });
        
        html += `</div>`;
        
        containerEstadisticas.innerHTML = html;
    }
    
    // ✅ FUNCIÓN PARA GENERAR GRÁFICO RADAR (sin cambios)
    function generarGraficoRadar(equipo1, equipo2, grupos) {
        const grupoSelect = document.getElementById('grupo-select-equipos');
        const grupoSeleccionado = grupoSelect ? grupoSelect.value : 'Ofensivos';
        
        // ✅ ACTUALIZAR VARIABLES GLOBALES
        grupoActual = grupoSeleccionado;
        equiposActuales = {
            [equipo1.nombre]: equipo1,
            [equipo2.nombre]: equipo2
        };
        
        if (!grupos[grupoSeleccionado]) {
            return;
        }
        
        const indicators = [];
        const data1 = [];
        const data2 = [];
        
        // ✅ USAR PERCENTILES PRE-CALCULADOS DEL BACKEND
        grupos[grupoSeleccionado].forEach(([nombre, campo]) => {
            const valorOriginal1 = equipo1[campo] || 0;
            const valorOriginal2 = equipo2[campo] || 0;
            
            // ✅ OBTENER PERCENTILES YA CALCULADOS EN PYTHON
            const percentil1 = equipo1[`${campo}_percentil`] || 50;
            const percentil2 = equipo2[`${campo}_percentil`] || 50;
            
            indicators.push({ 
                name: nombre, 
                max: 100,
                min: 0
            });
            
            data1.push(percentil1);
            data2.push(percentil2);
        });
        
        // ✅ CONFIGURACIÓN RADAR CON DIMENSIONES MÁS COMPACTAS
        const option = {
            backgroundColor: 'transparent',
            tooltip: { 
                trigger: 'item',
                backgroundColor: '#23243a',
                borderColor: '#00d4ff',
                borderWidth: 2,
                textStyle: { color: '#fff', fontSize: 13 },
                formatter: function(params) {
                    const equipoNombre = params.name;
                    const indicatorIndex = params.dataIndex;
                    
                    const equipoData = equiposActuales[equipoNombre];
                    if (!equipoData) {
                        return `<div style="color:red;">Error: Equipo ${equipoNombre} no encontrado</div>`;
                    }
                    
                    return generarTooltipContent(equipoData, equipoNombre, indicatorIndex, grupos, grupoActual);
                }
            },
            legend: {
                data: [equipo1.nombre, equipo2.nombre],
                top: 5,
                textStyle: { color: '#fff', fontSize: 11 }
            },
            radar: {
                indicator: indicators,
                center: ['50%', '52%'],
                radius: '62%',
                splitLine: { 
                    lineStyle: { color: '#23243a' } 
                },
                splitArea: { 
                    areaStyle: { color: ['#23243a', '#181b23'] } 
                },
                axisName: {
                    color: '#00d4ff',
                    fontSize: 12,
                    formatter: function(value) {
                        const palabras = value.split(' ');
                        let linea = '';
                        let resultado = '';
                        for (let palabra of palabras) {
                            if ((linea + ' ' + palabra).trim().length > 12) {
                                resultado += linea.trim() + '\n';
                                linea = palabra + ' ';
                            } else {
                                linea += palabra + ' ';
                            }
                        }
                        resultado += linea.trim();
                        return resultado;
                    }
                },
                axisLabel: {
                    show: true,
                    fontSize: 9,
                    color: '#666',
                    formatter: function(value) {
                        return `P${value}`;
                    }
                }
            },
            series: [{
                name: 'Comparación',
                type: 'radar',
                data: [
                    {
                        value: data1,
                        name: equipo1.nombre,
                        areaStyle: { color: 'rgba(0,212,255,0.3)' },
                        itemStyle: { color: '#00d4ff' },
                        lineStyle: { color: '#00d4ff', width: 2 }
                    },
                    {
                        value: data2,
                        name: equipo2.nombre,
                        areaStyle: { color: 'rgba(255,215,0,0.15)' },
                        itemStyle: { color: '#ffd700' },
                        lineStyle: { color: '#ffd700', width: 2 }
                    }
                ],
                symbolSize: 5
            }]
        };
        
        myChart.setOption(option);
    }
    
    // ✅ FUNCIÓN AUXILIAR PARA GENERAR CONTENIDO DEL TOOLTIP
    function generarTooltipContent(equipoData, equipoNombre, indicatorIndex, grupos, grupoActual) {
        let tooltip = `<div style="font-weight:bold;color:#00d4ff;margin-bottom:8px;font-size:16px;">${equipoNombre}</div>`;
        
        grupos[grupoActual].forEach(([nombre, campo], index) => {
            const valorOriginal = equipoData[campo] || 0;
            const percentil = equipoData[`${campo}_percentil`] || 50;
            
            const esActual = index === indicatorIndex;
            const estilo = esActual ? 
                'style="background-color:rgba(0,212,255,0.2);padding:2px 4px;border-radius:3px;margin:1px 0;"' : 
                'style="margin:1px 0;"';
            
            tooltip += `<div ${estilo}>${nombre}: <b style="color:#fff;">${valorOriginal}</b> <span style="color:#ffd700;">(P${percentil})</span></div>`;
        });
        
        return tooltip;
    }
    
    // ✅ EVENT LISTENERS PARA BOTONES DE MODO
    if (btnGraficos) {
        btnGraficos.addEventListener('click', () => cambiarModo('graficos'));
    }
    
    if (btnEstadisticas) {
        btnEstadisticas.addEventListener('click', () => cambiarModo('estadisticas'));
    }
    
    // ✅ EVENT LISTENERS PARA SELECTS
    const selectEquipo1 = document.getElementById('equipo1-select');
    const selectEquipo2 = document.getElementById('equipo2-select');
    const grupoSelect = document.getElementById('grupo-select-equipos');
    
    if (selectEquipo1) {
        selectEquipo1.addEventListener('change', actualizarVista);
    }
    
    if (selectEquipo2) {
        selectEquipo2.addEventListener('change', actualizarVista);
    }
    
    if (grupoSelect) {
        grupoSelect.addEventListener('change', actualizarVista);
    }
    
    // ✅ RESPONSIVE
    window.addEventListener('resize', function() {
        if (myChart && modoActual === 'graficos') {
            myChart.resize();
        }
    });
    
});

// ✅ FUNCIONES PARA JUGADORES
let jugadoresData = [];

// ✅ CARGAR DATOS DE JUGADORES AL INICIALIZAR
document.addEventListener('DOMContentLoaded', function() {
    // Cargar datos de jugadores si existen
    const jugadoresDataElement = document.getElementById('jugadores-data');
    if (jugadoresDataElement) {
        try {
            jugadoresData = JSON.parse(jugadoresDataElement.textContent.trim());
            console.log('✅ Datos de jugadores cargados:', jugadoresData.length);
            
            // ✅ DEBUG COMPLETO: Verificar estructura de datos
            if (jugadoresData.length > 0) {
                console.log('🔍 ESTRUCTURA DEL PRIMER JUGADOR:');
                console.log(jugadoresData[0]);
                
                // ✅ VERIFICAR EQUIPOS DISPONIBLES
                const equiposUnicos = [...new Set(jugadoresData
                    .filter(j => j.equipo_id !== null)
                    .map(j => `${j.equipo} (ID: ${j.equipo_id})`))];
                
                console.log('🏟️ EQUIPOS DISPONIBLES EN JUGADORES:');
                equiposUnicos.slice(0, 5).forEach(equipo => console.log(`   - ${equipo}`));
                
                // ✅ VERIFICAR POSICIONES DISPONIBLES
                const posicionesUnicas = [...new Set(jugadoresData
                    .filter(j => j.posicion && j.posicion !== 'N/A')
                    .map(j => j.posicion))];
                
                console.log('⚽ POSICIONES DISPONIBLES:');
                posicionesUnicas.forEach(pos => console.log(`   - ${pos}`));
                
                // ✅ ESTADÍSTICAS GENERALES
                const conEquipo = jugadoresData.filter(j => j.equipo_id !== null).length;
                const sinEquipo = jugadoresData.filter(j => j.equipo_id === null).length;
                
                console.log('📊 ESTADÍSTICAS JUGADORES:');
                console.log(`   Total: ${jugadoresData.length}`);
                console.log(`   Con equipo: ${conEquipo}`);
                console.log(`   Sin equipo: ${sinEquipo}`);
            }
            
        } catch (error) {
            console.error('❌ Error parseando datos de jugadores:', error);
        }
    } else {
        console.error('❌ Elemento jugadores-data no encontrado');
    }
});

// ✅ FUNCIÓN MEJORADA PARA FILTRAR JUGADORES - FILTRO MÁS FLEXIBLE
function filtrarJugadores(equipoId, posicion = '') {
    console.log(`🔍 FILTRADO DETALLADO:`);
    console.log(`   Equipo ID solicitado: ${equipoId} (tipo: ${typeof equipoId})`);
    console.log(`   Posición solicitada: '${posicion}'`);
    console.log(`   Total jugadores disponibles: ${jugadoresData.length}`);
    
    let jugadoresFiltrados = jugadoresData;
    
    // ✅ FILTRAR POR EQUIPO - CONVERSIÓN CORRECTA DE TIPOS
    if (equipoId) {
        const equipoIdNum = parseInt(equipoId);
        console.log(`   Buscando jugadores con equipo_id = ${equipoIdNum} (convertido de "${equipoId}")`);
        
        jugadoresFiltrados = jugadoresFiltrados.filter(j => {
            const jugadorEquipoId = parseInt(j.equipo_id);
            return jugadorEquipoId === equipoIdNum;
        });
        
        console.log(`   ✅ Después de filtrar por equipo: ${jugadoresFiltrados.length} jugadores`);
        
        // ✅ MOSTRAR TODOS LOS JUGADORES DEL EQUIPO (para debug)
        if (jugadoresFiltrados.length > 0) {
            console.log(`   🎯 Todos los jugadores del equipo ${equipoIdNum}:`);
            jugadoresFiltrados.forEach(j => {
                console.log(`     - ${j.nombre} (${j.posicion}) - Equipo: ${j.equipo}`);
            });
        } else {
            console.warn(`   ⚠️ NO se encontraron jugadores para equipo_id = ${equipoIdNum}`);
            return jugadoresFiltrados;
        }
    }
    
    // ✅ FILTRAR POR POSICIÓN - MÁS FLEXIBLE
    if (posicion && jugadoresFiltrados.length > 0) {
        console.log(`   🔍 Filtrando por posición: '${posicion}'`);
        
        const jugadoresPrevios = jugadoresFiltrados.length;
        const jugadoresAntesDelFiltro = [...jugadoresFiltrados]; // Copia para debug
        
        jugadoresFiltrados = jugadoresFiltrados.filter(j => {
            if (!j.posicion || j.posicion === 'N/A') return false;
            
            const posicionJugador = j.posicion.toUpperCase();
            const posicionFiltro = posicion.toUpperCase();
            
            // ✅ VARIOS TIPOS DE COINCIDENCIA
            const coincide = posicionJugador === posicionFiltro || 
                           posicionJugador.includes(posicionFiltro) ||
                           posicionJugador.split(',').some(p => p.trim() === posicionFiltro) ||
                           posicionJugador.split(' ').some(p => p.trim() === posicionFiltro);
            
            return coincide;
        });
        
        console.log(`   ✅ Después de filtrar por posición: ${jugadoresFiltrados.length}/${jugadoresPrevios} jugadores`);
        
        // ✅ DEBUG: Mostrar por qué no hay coincidencias
        if (jugadoresFiltrados.length === 0 && jugadoresPrevios > 0) {
            console.log(`   📍 Análisis de posiciones disponibles en equipo ${equipoId}:`);
            
            const posicionesDisponibles = jugadoresAntesDelFiltro.map(j => ({
                nombre: j.nombre,
                posicion: j.posicion,
                coincide_exacta: j.posicion === posicion,
                coincide_incluye: j.posicion && j.posicion.includes(posicion),
                coincide_split_coma: j.posicion && j.posicion.split(',').some(p => p.trim().toUpperCase() === posicion.toUpperCase()),
                coincide_split_espacio: j.posicion && j.posicion.split(' ').some(p => p.trim().toUpperCase() === posicion.toUpperCase())
            }));
            
            console.log(`   Detalle de posiciones:`);
            posicionesDisponibles.forEach(p => {
                console.log(`     - ${p.nombre}: "${p.posicion}" | Exacta: ${p.coincide_exacta} | Incluye: ${p.coincide_incluye} | Coma: ${p.coincide_split_coma} | Espacio: ${p.coincide_split_espacio}`);
            });
            
            const posicionesUnicas = [...new Set(jugadoresAntesDelFiltro.map(j => j.posicion).filter(p => p && p !== 'N/A'))];
            console.log(`   📍 Posiciones únicas disponibles: [${posicionesUnicas.join(', ')}]`);
        }
    }
    
    console.log(`🎯 RESULTADO FINAL: ${jugadoresFiltrados.length} jugadores filtrados`);
    
    return jugadoresFiltrados;
}

// ✅ FUNCIÓN MEJORADA PARA ACTUALIZAR LISTA
function actualizarListaJugadores(selectId, equipoId, posicion = '') {
    console.log(`\n🔄 ACTUALIZANDO LISTA ${selectId}:`);
    console.log(`   Equipo seleccionado: ${equipoId}`);
    console.log(`   Posición seleccionada: '${posicion}'`);
    
    const select = document.getElementById(selectId);
    if (!select) {
        console.error(`❌ Select ${selectId} no encontrado`);
        return;
    }
    
    const jugadoresFiltrados = filtrarJugadores(equipoId, posicion);
    
    // ✅ LIMPIAR OPCIONES
    select.innerHTML = '';
    
    if (!equipoId) {
        select.innerHTML = '<option value="">Primero selecciona equipo</option>';
        select.disabled = true;
        console.log(`   ℹ️ Sin equipo seleccionado, deshabilitando select`);
        return;
    }
    
    if (jugadoresFiltrados.length === 0) {
        select.innerHTML = '<option value="">No hay jugadores disponibles</option>';
        select.disabled = true;
        console.warn(`   ⚠️ NO hay jugadores disponibles para equipo ${equipoId} y posición '${posicion}'`);
        return;
    }
    
    // ✅ AGREGAR OPCIÓN POR DEFECTO
    select.innerHTML = '<option value="">Selecciona jugador</option>';
    
    // ✅ AGREGAR JUGADORES FILTRADOS
    jugadoresFiltrados.forEach(jugador => {
        const option = document.createElement('option');
        option.value = jugador.id;
        option.textContent = `${jugador.nombre} (${jugador.posicion || 'N/A'})`;
        select.appendChild(option);
    });
    
    select.disabled = false;
    console.log(`   ✅ Lista ${selectId} actualizada con ${jugadoresFiltrados.length} jugadores`);
}

// ✅ EVENT LISTENERS MEJORADOS PARA FILTROS DE JUGADORES
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Configurando event listeners para jugadores...');
    
    // Selectores de equipo para jugadores
    const equipoJugador1Select = document.getElementById('equipo-jugador1-select');
    const equipoJugador2Select = document.getElementById('equipo-jugador2-select');
    const posicionSelect = document.getElementById('posicion-select-jugadores');
    
    // ✅ CUANDO CAMBIA EL EQUIPO DEL JUGADOR 1
    if (equipoJugador1Select) {
        equipoJugador1Select.addEventListener('change', function() {
            const equipoId = this.value;
            const posicion = posicionSelect ? posicionSelect.value : '';
            console.log(`🔄 Cambió equipo jugador 1: ${equipoId}`);
            actualizarListaJugadores('jugador1-select', equipoId, posicion);
        });
    }
    
    // ✅ CUANDO CAMBIA EL EQUIPO DEL JUGADOR 2
    if (equipoJugador2Select) {
        equipoJugador2Select.addEventListener('change', function() {
            const equipoId = this.value;
            const posicion = posicionSelect ? posicionSelect.value : '';
            console.log(`🔄 Cambió equipo jugador 2: ${equipoId}`);
            actualizarListaJugadores('jugador2-select', equipoId, posicion);
        });
    }
    
    // ✅ CUANDO CAMBIA LA POSICIÓN
    if (posicionSelect) {
        posicionSelect.addEventListener('change', function() {
            const posicion = this.value;
            console.log(`🔄 Cambió posición: ${posicion}`);
            
            // ✅ ACTUALIZAR LISTAS DE JUGADORES SEGÚN EQUIPO Y POSICIÓN
            const equipoId1 = equipoJugador1Select ? equipoJugador1Select.value : '';
            const equipoId2 = equipoJugador2Select ? equipoJugador2Select.value : '';
            
            actualizarListaJugadores('jugador1-select', equipoId1, posicion);
            actualizarListaJugadores('jugador2-select', equipoId2, posicion);
        });
    }
    
    // ✅ INICIALIZAR SELECTS DE JUGADORES SI YA HAY EQUIPOS SELECCIONADOS
    const equipoId1 = equipoJugador1Select ? equipoJugador1Select.value : '';
    const equipoId2 = equipoJugador2Select ? equipoJugador2Select.value : '';
    
    if (equipoId1) {
        actualizarListaJugadores('jugador1-select', equipoId1);
    }
    
    if (equipoId2) {
        actualizarListaJugadores('jugador2-select', equipoId2);
    }
});

// ✅ VARIABLES GLOBALES PARA JUGADORES
let jugadoresActuales = {};
let grupoActualJugadores = 'Ofensivos';
let modoActualJugadores = 'graficos'; // 'graficos' o 'estadisticas'

// ✅ EVENT LISTENERS PARA COMPARACIÓN DE JUGADORES CON MODOS
document.addEventListener('DOMContentLoaded', function() {
    // ✅ ELEMENTOS DOM PARA JUGADORES
    const btnGraficosJugadores = document.getElementById('btn-graficos-jugadores');
    const btnEstadisticasJugadores = document.getElementById('btn-estadisticas-jugadores');
    const containerGraficoJugadores = document.getElementById('radar-comparacion-jugadores');
    const containerEstadisticasJugadores = document.getElementById('estadisticas-comparacion-jugadores');
    
    // ✅ FUNCIÓN PARA CAMBIAR MODO JUGADORES
    function cambiarModoJugadores(modo) {
        modoActualJugadores = modo;
        
        if (modo === 'graficos') {
            btnGraficosJugadores.classList.add('modo-activo');
            btnEstadisticasJugadores.classList.remove('modo-activo');
            containerGraficoJugadores.style.display = 'block';
            containerEstadisticasJugadores.style.display = 'none';
        } else {
            btnEstadisticasJugadores.classList.add('modo-activo');
            btnGraficosJugadores.classList.remove('modo-activo');
            containerGraficoJugadores.style.display = 'none';
            containerEstadisticasJugadores.style.display = 'block';
        }
        
        // ✅ ACTUALIZAR VISTA SEGÚN JUGADORES SELECCIONADOS
        actualizarVistaJugadores();
    }
    
    // ✅ FUNCIÓN PARA ACTUALIZAR VISTA JUGADORES
    function actualizarVistaJugadores() {
        const selectJugador1 = document.getElementById('jugador1-select');
        const selectJugador2 = document.getElementById('jugador2-select');
        
        if (!selectJugador1 || !selectJugador2) {
            return;
        }
        
        const jugadorId1 = parseInt(selectJugador1.value);
        const jugadorId2 = parseInt(selectJugador2.value);
        
        if (!jugadorId1 || !jugadorId2 || jugadorId1 === jugadorId2) {
            if (modoActualJugadores === 'graficos') {
                const chartContainer = document.getElementById('radar-comparacion-jugadores');
                if (chartContainer) {
                    echarts.getInstanceByDom(chartContainer)?.clear();
                }
            } else {
                containerEstadisticasJugadores.innerHTML = '<div class="no-data">Selecciona dos jugadores diferentes para comparar</div>';
            }
            return;
        }
        
        const jugador1 = jugadoresData.find(j => j.id === jugadorId1);
        const jugador2 = jugadoresData.find(j => j.id === jugadorId2);
        
        if (!jugador1 || !jugador2) {
            console.error('❌ Jugadores no encontrados:', jugadorId1, jugadorId2);
            return;
        }
        
        // ✅ CARGAR GRUPOS DE ESTADÍSTICAS DE JUGADORES
        const gruposJugadoresElement = document.getElementById('grupos-stats-jugadores-data');
        let gruposJugadores = {};
        
        if (gruposJugadoresElement) {
            try {
                gruposJugadores = JSON.parse(gruposJugadoresElement.textContent.trim());
            } catch (error) {
                console.error('❌ Error parseando grupos de jugadores:', error);
                return;
            }
        }
        
        if (modoActualJugadores === 'graficos') {
            console.log('🎯 Comparando jugadores (gráfico):', jugador1.nombre, 'vs', jugador2.nombre);
            generarGraficoRadarJugadores(jugador1, jugador2, gruposJugadores);
        } else {
            console.log('🎯 Comparando jugadores (estadísticas):', jugador1.nombre, 'vs', jugador2.nombre);
            generarTablaEstadisticasJugadores(jugador1, jugador2, gruposJugadores);
        }
    }
    
    // ✅ FUNCIÓN PARA GENERAR TABLA DE ESTADÍSTICAS JUGADORES - TODAS JUNTAS
    function generarTablaEstadisticasJugadores(jugador1, jugador2, grupos) {
        let html = `
            <div class="estadisticas-header">
                <h3>Comparación Completa: ${jugador1.nombre} vs ${jugador2.nombre}</h3>
                <div class="info-jugadores">
                    <div class="jugador-info jugador1-info">
                        <span class="nombre-jugador">${jugador1.nombre}</span>
                        <span class="equipo-jugador">${jugador1.equipo}</span>
                        <span class="posicion-jugador">${jugador1.posicion}</span>
                    </div>
                    <div class="vs-separator">VS</div>
                    <div class="jugador-info jugador2-info">
                        <span class="nombre-jugador">${jugador2.nombre}</span>
                        <span class="equipo-jugador">${jugador2.equipo}</span>
                        <span class="posicion-jugador">${jugador2.posicion}</span>
                    </div>
                </div>
            </div>
            <div class="tabla-comparacion">
        `;
        
        // ✅ ITERAR POR CADA GRUPO DE ESTADÍSTICAS
        Object.entries(grupos).forEach(([nombreGrupo, estadisticasGrupo]) => {
            html += `
                <div class="grupo-estadisticas">
                    <h4 class="grupo-titulo">${nombreGrupo}</h4>
                    <table class="stats-table">
                        <thead>
                            <tr>
                                <th>Estadística</th>
                                <th class="jugador-col jugador1-col">${jugador1.nombre}</th>
                                <th class="jugador-col jugador2-col">${jugador2.nombre}</th>
                                <th>Diferencia</th>
                            </tr>
                        </thead>
                        <tbody>
            `;
            
            // ✅ ITERAR POR CADA ESTADÍSTICA DEL GRUPO
            estadisticasGrupo.forEach(([nombre, campo]) => {
                const valor1 = jugador1[campo] || 0;
                const valor2 = jugador2[campo] || 0;
                const percentil1 = jugador1[`${campo}_percentil`] || 50;
                const percentil2 = jugador2[`${campo}_percentil`] || 50;
                
                // ✅ FORMATEAR VALORES SEGÚN EL TIPO
                const valorFormateado1 = formatearValorJugador(valor1, campo);
                const valorFormateado2 = formatearValorJugador(valor2, campo);
                
                const diferencia = (valor1 - valor2).toFixed(2);
                const diferenciaClass = diferencia > 0 ? 'positiva' : diferencia < 0 ? 'negativa' : 'neutra';
                const diferenciaSymbol = diferencia > 0 ? '+' : '';
                
                // ✅ DETERMINAR CUÁL JUGADOR ES MEJOR EN ESTA ESTADÍSTICA
                const jugador1Mejor = valor1 > valor2;
                const jugador2Mejor = valor2 > valor1;
                
                html += `
                    <tr>
                        <td class="stat-name">${nombre}</td>
                        <td class="stat-value jugador1-col ${jugador1Mejor ? 'mejor-valor' : ''}">
                            <div class="valor-principal">${valorFormateado1}</div>
                            <div class="percentil">P${percentil1}</div>
                        </td>
                        <td class="stat-value jugador2-col ${jugador2Mejor ? 'mejor-valor' : ''}">
                            <div class="valor-principal">${valorFormateado2}</div>
                            <div class="percentil">P${percentil2}</div>
                        </td>
                        <td class="diferencia ${diferenciaClass}">
                            ${diferenciaSymbol}${diferencia}
                        </td>
                    </tr>
                `;
            });
            
            html += `
                        </tbody>
                    </table>
                </div>
            `;
        });
        
        html += `</div>`;
        
        containerEstadisticasJugadores.innerHTML = html;
    }
    
    // ✅ FUNCIÓN AUXILIAR PARA FORMATEAR VALORES DE JUGADORES
    function formatearValorJugador(valor, campo) {
        // Campos de porcentaje
        if (campo.includes('percentage') || campo.includes('accuracy') || campo.includes('success')) {
            return `${valor.toFixed(1)}%`;
        }
        
        // Campos decimales (xG, xA, etc.)
        if (campo.includes('xg') || campo.includes('xa') || campo.includes('expected')) {
            return valor.toFixed(2);
        }
        
        // Campos enteros
        return Math.round(valor);
    }
    
    // ✅ EVENT LISTENERS PARA BOTONES DE MODO JUGADORES
    if (btnGraficosJugadores) {
        btnGraficosJugadores.addEventListener('click', () => cambiarModoJugadores('graficos'));
    }
    
    if (btnEstadisticasJugadores) {
        btnEstadisticasJugadores.addEventListener('click', () => cambiarModoJugadores('estadisticas'));
    }
    
    // ✅ EVENT LISTENERS PARA SELECCIÓN DE JUGADORES
    const jugador1Select = document.getElementById('jugador1-select');
    const jugador2Select = document.getElementById('jugador2-select');
    const grupoJugadoresSelect = document.getElementById('grupo-select-jugadores');
    
    if (jugador1Select) {
        jugador1Select.addEventListener('change', actualizarVistaJugadores);
    }
    
    if (jugador2Select) {
        jugador2Select.addEventListener('change', actualizarVistaJugadores);
    }
    
    if (grupoJugadoresSelect) {
        grupoJugadoresSelect.addEventListener('change', function() {
            grupoActualJugadores = this.value;
            actualizarVistaJugadores();
        });
    }
    
    // ✅ INICIALIZAR MODO GRÁFICO POR DEFECTO
    cambiarModoJugadores('graficos');
});

// ✅ ACTUALIZAR FUNCIÓN GENERARGRAFICOJUGADORES PARA USAR VARIABLES GLOBALES
function generarGraficoRadarJugadores(jugador1, jugador2, grupos) {
    const grupoSelect = document.getElementById('grupo-select-jugadores');
    const grupoSeleccionado = grupoSelect ? grupoSelect.value : 'Ofensivos';
    
    // ✅ ACTUALIZAR VARIABLES GLOBALES
    grupoActualJugadores = grupoSeleccionado;
    jugadoresActuales = {
        [jugador1.nombre]: jugador1,
        [jugador2.nombre]: jugador2
    };
    
    const chartContainer = document.getElementById('radar-comparacion-jugadores');
    if (!chartContainer) {
        console.error('❌ Contenedor del gráfico de jugadores no encontrado');
        return;
    }

    // ✅ INICIALIZAR ECHARTS PARA JUGADORES
    chartContainer.style.width = '100%';
    chartContainer.style.maxWidth = '550px';
    chartContainer.style.height = '480px';
    chartContainer.style.margin = '0 auto';

    const myChartJugadores = echarts.init(chartContainer, null, {devicePixelRatio: 2});
    
    if (!grupos[grupoSeleccionado]) {
        console.error(`❌ Grupo ${grupoSeleccionado} no encontrado`);
        return;
    }
    
    const indicators = [];
    const data1 = [];
    const data2 = [];
    
    // ✅ USAR PERCENTILES PARA JUGADORES
    grupos[grupoSeleccionado].forEach(([nombre, campo]) => {
        const percentil1 = jugador1[`${campo}_percentil`] || 50;
        const percentil2 = jugador2[`${campo}_percentil`] || 50;
        
        indicators.push({ 
            name: nombre, 
            max: 100,
            min: 0
        });
        
        data1.push(percentil1);
        data2.push(percentil2);
    });
    
    // ✅ CONFIGURACIÓN RADAR PARA JUGADORES
    const option = {
        backgroundColor: 'transparent',
        tooltip: { 
            trigger: 'item',
            backgroundColor: '#23243a',
            borderColor: '#00d4ff',
            borderWidth: 2,
            textStyle: { color: '#fff', fontSize: 13 },
            formatter: function(params) {
                const jugadorNombre = params.name;
                const indicatorIndex = params.dataIndex;
                
                const jugadorData = jugadoresActuales[jugadorNombre];
                if (!jugadorData) {
                    return `<div style="color:red;">Error: Jugador ${jugadorNombre} no encontrado</div>`;
                }
                
                return generarTooltipJugadores(jugadorData, jugadorNombre, indicatorIndex, grupos, grupoActualJugadores);
            }
        },
        legend: {
            data: [jugador1.nombre, jugador2.nombre],
            top: 5,
            textStyle: { color: '#fff', fontSize: 11 }
        },
        radar: {
            indicator: indicators,
            center: ['50%', '52%'],
            radius: '62%',
            splitLine: { 
                lineStyle: { color: '#23243a' } 
            },
            splitArea: { 
                areaStyle: { color: ['#23243a', '#181b23'] } 
            },
            axisName: {
                color: '#00d4ff',
                fontSize: 12,
                formatter: function(value) {
                    const palabras = value.split(' ');
                    let linea = '';
                    let resultado = '';
                    for (let palabra of palabras) {
                        if ((linea + ' ' + palabra).trim().length > 12) {
                            resultado += linea.trim() + '\n';
                            linea = palabra + ' ';
                        } else {
                            linea += palabra + ' ';
                        }
                    }
                    resultado += linea.trim();
                    return resultado;
                }
            },
            axisLabel: {
                show: true,
                fontSize: 9,
                color: '#666',
                formatter: function(value) {
                    return `P${value}`;
                }
            }
        },
        series: [{
            name: 'Comparación Jugadores',
            type: 'radar',
            data: [
                {
                    value: data1,
                    name: jugador1.nombre,
                    areaStyle: { color: 'rgba(0,212,255,0.3)' },
                    itemStyle: { color: '#00d4ff' },
                    lineStyle: { color: '#00d4ff', width: 2 }
                },
                {
                    value: data2,
                    name: jugador2.nombre,
                    areaStyle: { color: 'rgba(255,215,0,0.15)' },
                    itemStyle: { color: '#ffd700' },
                    lineStyle: { color: '#ffd700', width: 2 }
                }
            ],
            symbolSize: 5
        }]
    };
    
    myChartJugadores.setOption(option);
}

// ✅ FUNCIÓN AUXILIAR PARA TOOLTIP DE JUGADORES
function generarTooltipJugadores(jugadorData, jugadorNombre, indicatorIndex, grupos, grupoActual) {
    let tooltip = `<div style="font-weight:bold;color:#00d4ff;margin-bottom:8px;font-size:16px;">${jugadorNombre}</div>`;
    tooltip += `<div style="color:#ffd700;margin-bottom:5px;">${jugadorData.equipo} - ${jugadorData.posicion}</div>`;
    
    grupos[grupoActual].forEach(([nombre, campo], index) => {
        const valorOriginal = jugadorData[campo] || 0;
        const percentil = jugadorData[`${campo}_percentil`] || 50;
        
        const esActual = index === indicatorIndex;
        const estilo = esActual ? 
            'style="background-color:rgba(0,212,255,0.2);padding:2px 4px;border-radius:3px;margin:1px 0;"' : 
            'style="margin:1px 0;"';
        
        tooltip += `<div ${estilo}>${nombre}: <b style="color:#fff;">${valorOriginal}</b> <span style="color:#ffd700;">(P${percentil})</span></div>`;
    });
    
    return tooltip;
}

// ✅ EVENT LISTENERS PARA COMPARACIÓN DE JUGADORES
document.addEventListener('DOMContentLoaded', function() {
    // Selectores de jugador
    const jugador1Select = document.getElementById('jugador1-select');
    const jugador2Select = document.getElementById('jugador2-select');
    const grupoJugadoresSelect = document.getElementById('grupo-select-jugadores');
    
    // ✅ CARGAR GRUPOS DE ESTADÍSTICAS DE JUGADORES
    const gruposJugadoresElement = document.getElementById('grupos-stats-jugadores-data');
    let gruposJugadores = {};
    
    if (gruposJugadoresElement) {
        try {
            gruposJugadores = JSON.parse(gruposJugadoresElement.textContent.trim());
            console.log('✅ Grupos de estadísticas de jugadores cargados:', Object.keys(gruposJugadores));
        } catch (error) {
            console.error('❌ Error parseando grupos de jugadores:', error);
        }
    }
    
    // ✅ FUNCIÓN PARA ACTUALIZAR COMPARACIÓN DE JUGADORES
    function actualizarComparacionJugadores() {
        const jugador1Select = document.getElementById('jugador1-select');
        const jugador2Select = document.getElementById('jugador2-select');
        
        if (!jugador1Select || !jugador2Select) {
            return;
        }
        
        const jugadorId1 = parseInt(jugador1Select.value);
        const jugadorId2 = parseInt(jugador2Select.value);
        
        if (!jugadorId1 || !jugadorId2 || jugadorId1 === jugadorId2) {
            const chartContainer = document.getElementById('radar-comparacion-jugadores');
            if (chartContainer) {
                echarts.getInstanceByDom(chartContainer)?.clear();
            }
            return;
        }
        
        const jugador1 = jugadoresData.find(j => j.id === jugadorId1);
        const jugador2 = jugadoresData.find(j => j.id === jugadorId2);
        
        if (!jugador1 || !jugador2) {
            console.error('❌ Jugadores no encontrados:', jugadorId1, jugadorId2);
            return;
        }
        
        console.log('🎯 Comparando jugadores:', jugador1.nombre, 'vs', jugador2.nombre);
        generarGraficoRadarJugadores(jugador1, jugador2, gruposJugadores);
    }
    
    // ✅ EVENT LISTENERS PARA SELECCIÓN DE JUGADORES
    if (jugador1Select) {
        jugador1Select.addEventListener('change', actualizarComparacionJugadores);
    }
    
    if (jugador2Select) {
        jugador2Select.addEventListener('change', actualizarComparacionJugadores);
    }
    
    if (grupoJugadoresSelect) {
        grupoJugadoresSelect.addEventListener('change', actualizarComparacionJugadores);
    }
});