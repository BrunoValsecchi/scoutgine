if (typeof window.EstadisticaJugadorLoaded === 'undefined') {
    window.EstadisticaJugadorLoaded = true;

    // --- Radar Chart (ECharts) ---
    function cargarRadarJugador(grupo = 'ofensivos', posicion = null) {
        const radarContainer = document.getElementById('radar-jugador-chart-container');
        if (!radarContainer || !window.jugadorData?.jugadorId) return;
        radarContainer.style.width = '100%';
        radarContainer.style.maxWidth = '600px';
        radarContainer.style.height = '620px';
        radarContainer.style.margin = '0 auto';

        let url = `/ajax/radar-jugador/?jugador_id=${window.jugadorData.jugadorId}&grupo=${grupo}`;
        if (posicion) url += `&posicion=${encodeURIComponent(posicion)}`;

        fetch(url)
            .then(resp => resp.json())
            .then(data => {
                // Si el jugador tiene varias posiciones, muestra el selector
                if (data.posiciones_jugador && data.posiciones_jugador.length > 1) {
                    const selector = document.getElementById('posicion-jugador-selector');
                    selector.style.display = '';
                    selector.innerHTML = '';
                    data.posiciones_jugador.forEach(pos => {
                        const opt = document.createElement('option');
                        opt.value = pos;
                        opt.textContent = pos;
                        if (pos === data.posicion) opt.selected = true;
                        selector.appendChild(opt);
                    });
                    selector.onchange = function() {
                        cargarRadarJugador(grupo, this.value);
                    };
                } else {
                    document.getElementById('posicion-jugador-selector').style.display = 'none';
                }

                // Dibuja el radar con ECharts
                const radarChart = echarts.init(radarContainer, null, {devicePixelRatio: 2});
                radarChart.setOption({
                    backgroundColor: 'transparent',
                    tooltip: {trigger: 'item'},
                    legend: {
                        data: ['Jugador', 'Promedio'],
                        top: 10,
                        textStyle: {color: '#fff'}
                    },
                    radar: {
                        indicator: data.labels.map(l => ({name: l, max: 100})),
                        splitLine: {lineStyle: {color: '#23243a'}},
                        splitArea: {areaStyle: {color: ['#23243a','#181b23']}},
                        axisName: {
                            color: '#00d4ff',
                            fontSize: 13,
                            formatter: function(value) {
                                const palabras = value.split(' ');
                                let linea = '';
                                let resultado = '';
                                for (let palabra of palabras) {
                                    if ((linea + ' ' + palabra).trim().length > 14) {
                                        resultado += linea.trim() + '\n';
                                        linea = palabra + ' ';
                                    } else {
                                        linea += palabra + ' ';
                                    }
                                }
                                resultado += linea.trim();
                                return resultado;
                            }
                        }
                    },
                    series: [{
                        type: 'radar',
                        data: [
                            {value: data.jugador, name: 'Jugador', areaStyle: {color: 'rgba(0,212,255,0.3)'}},
                            {value: data.promedio, name: 'Promedio', areaStyle: {color: 'rgba(255,215,0,0.15)'}}
                        ],
                        symbolSize: 6,
                        lineStyle: {width: 2}
                    }]
                });
            })
            .catch(() => {
                radarContainer.innerHTML = '<div style="color:#ff6b6b;text-align:center;">Error al cargar radar</div>';
            });
    }

    function cargarGraficoDispersionJugador(statX, statY, posicion) {
        console.log('Cargando gráfico con:', {statX, statY, posicion});
        
        const chartContainer = document.getElementById('chart-dispersion-jugador');
        if (!chartContainer) {
            console.error('No se encontró el contenedor del gráfico');
            return;
        }
        
        chartContainer.style.width = '100%';
        chartContainer.style.height = '600px';
        chartContainer.innerHTML = 'Cargando...';

        let url = `/ajax/grafico-dispersion-jugador/?stat_x=${statX}&posicion=${encodeURIComponent(posicion)}`;
        if (statY) url += `&stat_y=${statY}`;
        if (window.jugadorData?.jugadorId) url += `&jugador_id=${window.jugadorData.jugadorId}`;

        fetch(url)
            .then(resp => {
                if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
                return resp.json();
            })
            .then(data => {
                if (!data.success) {
                    chartContainer.innerHTML = `<div style="color:#ff6b6b;text-align:center;">Error: ${data.error}</div>`;
                    return;
                }

                // Actualizar selector de estadística Y
                const statYSelector = document.getElementById('stat-y-selector');
                if (statYSelector) {
                    statYSelector.innerHTML = '';
                    data.campos_y.forEach(campo => {
                        const option = document.createElement('option');
                        option.value = campo;
                        option.textContent = campo.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                        if (campo === data.stat_y) option.selected = true;
                        statYSelector.appendChild(option);
                    });
                }

                // Crear el gráfico con ECharts
                if (window.dispersionJugadorChart) {
                    window.dispersionJugadorChart.dispose();
                }

                window.dispersionJugadorChart = echarts.init(chartContainer, 'dark', {
                    devicePixelRatio: 2
                });

                const scatterData = data.data.map(j => [j.x, j.y, j.nombre]);
                const jugadorActual = data.jugador_actual;

                const option = {
                    backgroundColor: '#181b23',
                    title: {
                        text: `${data.stat_x.replace(/_/g, ' ')} vs ${data.stat_y.replace(/_/g, ' ')}`,
                        left: 'center',
                        top: 20,
                        textStyle: {
                            color: '#fff',
                            fontSize: 26,
                            fontWeight: 600,
                            fontFamily: 'Inter, Arial, sans-serif'
                        }
                    },
                    tooltip: {
                        trigger: 'item',
                        backgroundColor: '#23243a',
                        borderColor: '#67aaff',
                        borderWidth: 2,
                        textStyle: { color: '#fff', fontSize: 16 },
                        formatter: params => {
                            const isCurrent = jugadorActual && params.data[2] === jugadorActual.nombre;
                            return `
                                <div style="font-size:17px;font-weight:bold;color:${isCurrent ? '#FFD700' : '#67aaff'};margin-bottom:6px;">
                                    ${isCurrent ? '⭐ ' : ''}${params.data[2]}
                                </div>
                                <div>${data.stat_x.replace(/_/g, ' ')}: <b>${params.data[0]}</b></div>
                                <div>${data.stat_y.replace(/_/g, ' ')}: <b>${params.data[1]}</b></div>
                            `;
                        }
                    },
                    grid: {
                        left: 80,
                        right: 40,
                        top: 80,
                        bottom: 60,
                        containLabel: true
                    },
                    xAxis: {
                        type: 'value',
                        name: data.stat_x.replace(/_/g, ' '),
                        nameLocation: 'middle',
                        nameGap: 40,
                        nameTextStyle: { color: '#fff', fontSize: 18, fontWeight: 600 },
                        axisLabel: { color: '#b0b8c9', fontSize: 15 },
                        axisLine: { lineStyle: { color: '#67aaff', width: 2 } },
                        splitLine: { lineStyle: { color: '#23243a', type: 'dashed' } }
                    },
                    yAxis: {
                        type: 'value',
                        name: data.stat_y.replace(/_/g, ' '),
                        nameLocation: 'middle',
                        nameGap: 60,
                        nameTextStyle: { color: '#fff', fontSize: 18, fontWeight: 600 },
                        axisLabel: { color: '#b0b8c9', fontSize: 15 },
                        axisLine: { lineStyle: { color: '#67aaff', width: 2 } },
                        splitLine: { lineStyle: { color: '#23243a', type: 'dashed' } }
                    },
                    series: [{
                        type: 'scatter',
                        data: scatterData,
                        symbolSize: function(data) {
                            const nombre = data[2];
                            return jugadorActual && nombre === jugadorActual.nombre ? 28 : 18;
                        },
                        itemStyle: {
                            color: function(params) {
                                const nombre = params.data[2];
                                if (jugadorActual && nombre === jugadorActual.nombre) {
                                    return '#FFD700';
                                }
                                return '#67aaff';
                            },
                            borderColor: '#fff',
                            borderWidth: 2,
                            opacity: 0.85,
                            shadowBlur: 10,
                            shadowColor: 'rgba(103,170,255,0.3)'
                        },
                        emphasis: {
                            itemStyle: {
                                borderColor: '#FFD700',
                                borderWidth: 3,
                                opacity: 1,
                                shadowBlur: 20,
                                shadowColor: '#FFD700'
                            }
                        }
                    }]
                };

                window.dispersionJugadorChart.setOption(option);
            })
            .catch(err => {
                console.error('Error al cargar gráfico de dispersión:', err);
                chartContainer.innerHTML = '<div style="color:#ff6b6b;text-align:center;">Error al cargar el gráfico</div>';
            });
    }

    function cargarBoxplotJugador(estadistica, posicion) {
        const boxplotContainer = document.getElementById('boxplot-jugador-chart-container');
        if (!boxplotContainer || !window.jugadorData?.jugadorId) return;
        
        boxplotContainer.style.width = '100%';
        boxplotContainer.style.height = '350px';
        boxplotContainer.innerHTML = 'Cargando...';

        let url = `/ajax/boxplot-jugador/?jugador_id=${window.jugadorData.jugadorId}&estadistica=${encodeURIComponent(estadistica)}`;
        if (posicion) url += `&posicion=${encodeURIComponent(posicion)}`;

        fetch(url)
            .then(resp => resp.json())
            .then(data => {
                if (!data.success) {
                    boxplotContainer.innerHTML = `<div style="color:#ff6b6b;text-align:center;">${data.error}</div>`;
                    return;
                }

                // Crear el boxplot con ECharts
                if (window.boxplotJugadorChart) {
                    window.boxplotJugadorChart.dispose();
                }

                window.boxplotJugadorChart = echarts.init(boxplotContainer, 'dark', {
                    devicePixelRatio: 2
                });

                const option = {
                    backgroundColor: 'transparent',
                    title: {
                        text: `Distribución de ${data.stat} (${data.posicion})`,
                        left: 'center',
                        textStyle: { color: '#00d4ff', fontSize: 18, fontWeight: 600 }
                    },
                    tooltip: {
                        trigger: 'item',
                        backgroundColor: '#23243a',
                        borderColor: '#67aaff',
                        borderWidth: 2,
                        textStyle: { color: '#fff', fontSize: 14 },
                        formatter: function (param) {
                            if (param.seriesType === 'boxplot') {
                                return `
                                    <div><b>Estadística:</b> ${data.stat}</div>
                                    <div><b>Mínimo:</b> ${param.data[1]}</div>
                                    <div><b>Q1:</b> ${param.data[2]}</div>
                                    <div><b>Mediana:</b> ${param.data[3]}</div>
                                    <div><b>Q3:</b> ${param.data[4]}</div>
                                    <div><b>Máximo:</b> ${param.data[5]}</div>
                                    <div><b>Total jugadores:</b> ${data.total_jugadores}</div>
                                `;
                            } else if (param.seriesType === 'scatter') {
                                return `<div><b>${data.jugador_nombre}:</b> ${param.data[0]}</div>`;
                            }
                        }
                    },
                    grid: { top: 80, bottom: 60, left: 80, right: 40, containLabel: true },
                    xAxis: {
                        type: 'value',
                        name: data.stat,
                        nameLocation: 'middle',
                        nameGap: 40,
                        nameTextStyle: { color: '#fff', fontSize: 16, fontWeight: 600 },
                        axisLabel: { color: '#b0b8c9', fontSize: 15 },
                        axisLine: { lineStyle: { color: '#67aaff', width: 2 } },
                        splitLine: { lineStyle: { color: '#23243a', type: 'dashed' } }
                    },
                    yAxis: {
                        type: 'category',
                        data: [''],
                        axisLabel: { color: '#fff', fontSize: 16 },
                        axisLine: { lineStyle: { color: '#67aaff', width: 2 } }
                    },
                    series: [
                        {
                            name: 'Distribución',
                            type: 'boxplot',
                            data: [data.box],
                            itemStyle: { color: '#00d4ff', borderColor: '#fff' }
                        },
                        // Solo agregar el punto del jugador si tiene valor
                        ...(data.valor_jugador !== null && !isNaN(data.valor_jugador) ? [{
                            name: data.jugador_nombre,
                            type: 'scatter',
                            data: [[data.valor_jugador, 0]],
                            symbolSize: 18,
                            itemStyle: { 
                                color: '#FFD700', 
                                borderColor: '#fff', 
                                borderWidth: 2 
                            },
                            tooltip: { 
                                formatter: `${data.jugador_nombre}: ${data.valor_jugador}` 
                            }
                        }] : [])
                    ]
                };

                window.boxplotJugadorChart.setOption(option);
            })
            .catch(err => {
                console.error('Error al cargar boxplot:', err);
                boxplotContainer.innerHTML = '<div style="color:#ff6b6b;text-align:center;">Error al cargar el boxplot</div>';
            });
    }

    function obtenerStatDeURL() {
        const estadistica = window.jugadorData?.estadistica;
        if (!estadistica) return 'goals';
        
        const mapeo = {
            'Goles': 'goals',
            'Goles esperados (xG)': 'expected_goals_xg',
            'Tiros al arco': 'shots_on_target',
            'Tiros totales': 'shots',
            'Asistencias': 'assists',
            'Penales a favor': 'penalties_awarded',
            'Ocasiones claras falladas': 'big_chances_missed',
            'Goles concedidos': 'goals_conceded',
            'Vallas invictas': 'clean_sheets',
            'xG concedido': 'expected_goals_conceded_xgc',
            'Entradas exitosas': 'tackles_won',
            'Intercepciones': 'interceptions',
            'Despejes': 'blocked',
            'Recuperaciones último tercio': 'recoveries',
            'Atajadas': 'saves',
            'Pases precisos por partido': 'successful_passes',
            'Precisión de pases': 'pass_accuracy_outfield',
            'Pases largos precisos': 'accurate_long_balls_outfield',
            'Centros precisos': 'successful_crosses',
            'Ocasiones creadas': 'chances_created',
            'Toques en área rival': 'touches_in_opposition_box',
            'Tiros de esquina': 'corners_taken',
            'Rating': 'average_rating',
            'Partidos jugados': 'appearances',
            'Minutos jugados': 'minutes_played',
            'Posesión promedio': 'possession_percentage',
            'Toques totales': 'touches',
            'Duelos ganados': 'duels_won_percentage',
            'Duelos aéreos ganados': 'aerial_duels_won_percentage',
            'Faltas por partido': 'fouls_committed',
            'Tarjetas amarillas': 'yellow_cards',
            'Tarjetas rojas': 'red_cards'
        };
        
        return mapeo[estadistica] || 'goals';
    }

    // UN SOLO DOMContentLoaded
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Inicializando estadística jugador...');

        // 1. Cargar radar
        cargarRadarJugador('ofensivos');
        const radarGroupSel = document.getElementById('radar-jugador-group-selector');
        if (radarGroupSel) {
            radarGroupSel.addEventListener('change', function() {
                const pos = document.getElementById('posicion-jugador-selector').value || null;
                cargarRadarJugador(this.value, pos);
            });
        }

        // 2. Cargar dispersión
        fetch(`/api/jugador/${window.jugadorData.jugadorId}/posiciones/`)
            .then(resp => resp.json())
            .then(data => {
                const posiciones = data.posiciones || [];
                const posicionSelector = document.getElementById('posicion-dispersion-selector');
                const statYSelector = document.getElementById('stat-y-selector');
                
                if (posicionSelector && posiciones.length > 0) {
                    // Llenar selector de posiciones
                    posicionSelector.innerHTML = '';
                    posiciones.forEach(pos => {
                        const option = document.createElement('option');
                        option.value = pos;
                        option.textContent = pos;
                        posicionSelector.appendChild(option);
                    });

                    // Cargar gráfico inicial
                    const statX = obtenerStatDeURL();
                    cargarGraficoDispersionJugador(statX, null, posiciones[0]);

                    // Eventos ÚNICOS para los selectores
                    posicionSelector.addEventListener('change', function() {
                        const statX = obtenerStatDeURL();
                        const statY = statYSelector ? statYSelector.value : null;
                        cargarGraficoDispersionJugador(statX, statY, this.value);
                    });

                    if (statYSelector) {
                        statYSelector.addEventListener('change', function() {
                            const statX = obtenerStatDeURL();
                            const posicion = posicionSelector.value;
                            cargarGraficoDispersionJugador(statX, this.value, posicion);
                        });
                    }
                }
            })
            .catch(err => {
                console.error('Error cargando posiciones:', err);
            });

        // 3. Cargar boxplot
        fetch(`/api/jugador/${window.jugadorData.jugadorId}/posiciones/`)
            .then(resp => resp.json())
            .then(data => {
                const posiciones = data.posiciones || [];
                
                const posicionBoxplotSelector = document.getElementById('posicion-boxplot-selector');
                if (posicionBoxplotSelector && posiciones.length > 0) {
                    // Llenar selector de posiciones para boxplot
                    posicionBoxplotSelector.innerHTML = '';
                    posiciones.forEach(pos => {
                        const option = document.createElement('option');
                        option.value = pos;
                        option.textContent = pos;
                        posicionBoxplotSelector.appendChild(option);
                    });

                    // Cargar boxplot inicial
                    const estadistica = window.jugadorData.estadistica;
                    cargarBoxplotJugador(estadistica, posiciones[0]);

                    // Evento para cambio de posición en boxplot
                    posicionBoxplotSelector.addEventListener('change', function() {
                        cargarBoxplotJugador(estadistica, this.value);
                    });
                }
            });
    });
}