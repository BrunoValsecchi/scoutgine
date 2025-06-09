// Evitar redeclaración global
if (typeof window.EstadisticaFutbolLoaded === 'undefined') {
    window.EstadisticaFutbolLoaded = true;

    class EstadisticaFutbol {
        constructor() {
            this.equipoId = null;
            this.statName = null;
            this.dispersionChart = null;
            this.inicializar();
        }

        inicializar() {
            // Obtener datos de la URL
            const url = window.location.pathname;
            const matches = url.match(/\/equipo\/(\d+)\/([^\/]+)\//);
            if (matches) {
                this.equipoId = matches[1];
                this.statName = decodeURIComponent(matches[2]);
                console.log('📊 Datos obtenidos:', this.equipoId, this.statName);
            }

            // Esperar a que el DOM esté listo
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', () => this.configurarEventos());
            } else {
                this.configurarEventos();
            }
        }

        configurarEventos() {
            console.log('🔧 Configurando eventos...');
            
            // Selector de estadística para comparación
            const selector = document.getElementById('stat-comparacion-selector');
            if (selector) {
                console.log('✅ Selector encontrado');
                
                selector.addEventListener('change', (e) => {
                    console.log('📈 Cambiando comparación a:', e.target.value);
                    this.cargarGraficoDispersion(e.target.value);
                });
                
                // Cargar gráfico inicial
                this.cargarGraficoDispersion();
            } else {
                console.log('❌ Selector no encontrado');
            }
        }

        async cargarGraficoDispersion(statComparacion = 'Rating') {
            console.log('🚀 Cargando gráfico dispersión:', statComparacion);
            
            const loadingDiv = document.getElementById('loading-dispersion');
            const chartDiv = document.getElementById('chart-dispersion');
            
            try {
                if (loadingDiv) loadingDiv.style.display = 'flex';
                if (chartDiv) chartDiv.style.display = 'none';

                const csrfToken = this.getCsrfToken();
                const requestData = {
                    equipo_id: this.equipoId,
                    stat_principal: this.statName,
                    stat_comparacion: statComparacion
                };

                const response = await fetch('/ajax/grafico-dispersion/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                    body: JSON.stringify(requestData)
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                
                if (data.success) {
                    this.crearGraficoDispersion(data.chart_data, statComparacion);
                } else {
                    this.mostrarError('Error: ' + data.error);
                }

            } catch (error) {
                console.error('❌ Error:', error);
                this.mostrarError('Error de conexión: ' + error.message);
            } finally {
                if (loadingDiv) loadingDiv.style.display = 'none';
                if (chartDiv) chartDiv.style.display = 'block';
            }
        }

        crearGraficoDispersion(data, statComparacion) {
            const chartContainer = document.getElementById('chart-dispersion');
            if (!chartContainer || !window.echarts) {
                this.mostrarError('Error de configuración');
                return;
            }

                        // 👇 FORZAR ALTO Y ANCHO SIEMPRE ANTES DE INICIALIZAR
            chartContainer.style.width = '1000px';
            chartContainer.style.height = '800px'; // Cambia el alto a lo que quieras (ej: 400px, 500px)
            
            if (this.dispersionChart) {
                this.dispersionChart.dispose();
            }
            chartContainer.innerHTML = '';

            this.dispersionChart = echarts.init(chartContainer, null, {
                devicePixelRatio: window.devicePixelRatio || 1
            });

            const scatterData = data.equipos.map(equipo => [
                equipo.stat_principal,
                equipo.stat_comparacion,
                equipo.nombre
            ]);
            const equipoActual = data.equipos.find(eq => eq.es_actual);

            // Calcular la media de X y Y
            const xVals = scatterData.map(d => d[0]);
            const yVals = scatterData.map(d => d[1]);
            const meanX = xVals.reduce((a, b) => a + b, 0) / xVals.length;
            const meanY = yVals.reduce((a, b) => a + b, 0) / yVals.length;

            const option = {
                backgroundColor: 'transparent',
                title: {
                    text: `${this.statName} vs ${statComparacion}`,
                    left: 'center',
                    top: 10,
                    textStyle: {
                        color: '#00d4ff',
                        fontSize: 20,
                        fontWeight: 700,
                        fontFamily: 'Inter, Arial, sans-serif'
                    }
                },
                tooltip: {
                    trigger: 'item',
                    backgroundColor: '#23243a',
                    borderColor: '#00d4ff',
                    borderWidth: 1,
                    textStyle: { color: '#fff', fontSize: 15 },
                    formatter: params => {
                        const isCurrent = equipoActual && params.data[2] === equipoActual.nombre;
                        return `
                            <div style="font-size:16px;font-weight:bold;color:${isCurrent ? '#FFD700' : '#00d4ff'};margin-bottom:6px;">
                                ${isCurrent ? '⭐ ' : ''}${params.data[2]}
                            </div>
                            <div>${this.statName}: <b>${params.data[0]}</b></div>
                            <div>${statComparacion}: <b>${params.data[1]}</b></div>
                        `;
                    }
                },
                grid: {
                    left: 60,
                    right: 30,
                    top: 60,
                    bottom: 50,
                    containLabel: true
                },
                xAxis: {
                    type: 'value',
                    name: this.statName,
                    nameLocation: 'middle',
                    nameGap: 30,
                    nameTextStyle: { color: '#fff', fontSize: 15, fontWeight: 600 },
                    axisLabel: { color: '#b0b8c9', fontSize: 13 },
                    axisLine: { lineStyle: { color: '#00d4ff', width: 1 } },
                    splitLine: { lineStyle: { color: '#23243a', type: 'dashed' } }
                },
                yAxis: {
                    type: 'value',
                    name: statComparacion,
                    nameLocation: 'middle',
                    nameGap: 40,
                    nameTextStyle: { color: '#fff', fontSize: 15, fontWeight: 600 },
                    axisLabel: { color: '#b0b8c9', fontSize: 13 },
                    axisLine: { lineStyle: { color: '#00d4ff', width: 1 } },
                    splitLine: { lineStyle: { color: '#23243a', type: 'dashed' } }
                },
                series: [
                    {
                        type: 'scatter',
                        data: scatterData,
                        symbolSize: function(data) {
                            const equipo = data[2];
                            return equipoActual && equipo === equipoActual.nombre ? 22 : 14;
                        },
                        itemStyle: {
                            color: function(params) {
                                const equipo = params.data[2];
                                if (equipoActual && equipo === equipoActual.nombre) {
                                    return '#FFD700';
                                }
                                return '#00d4ff';
                            },
                            borderColor: '#fff',
                            borderWidth: 1,
                            opacity: 0.9,
                            shadowBlur: 6,
                            shadowColor: 'rgba(0,212,255,0.15)'
                        },
                        emphasis: {
                            itemStyle: {
                                borderColor: '#FFD700',
                                borderWidth: 2,
                                opacity: 1,
                                shadowBlur: 12,
                                shadowColor: '#FFD700'
                            }
                        },
                        // --- LÍNEAS DE MEDIA ---
                        markLine: {
                            symbol: 'none',
                            lineStyle: {
                                color: '#FFD700',
                                width: 2,
                                type: 'dashed'
                            },
                            data: [
                                { xAxis: meanX }, // Línea vertical en la media de X
                                { yAxis: meanY }  // Línea horizontal en la media de Y
                            ],
                            label: {
                                show: false
                            }
                        }
                    }
                ]
            };

            this.dispersionChart.setOption(option);

            // Resize responsivo
            window.addEventListener('resize', () => {
                if (this.dispersionChart && !this.dispersionChart.isDisposed()) {
                    this.dispersionChart.resize();
                }
            });
        }

        mostrarError(mensaje) {
            const chartContainer = document.getElementById('chart-dispersion');
            if (chartContainer) {
                chartContainer.innerHTML = `
                    <div style="display: flex; align-items: center; justify-content: center; height: 100%; color: #ff6b6b; text-align: center; flex-direction: column;">
                        <div style="font-size: 3rem; margin-bottom: 20px;">⚠️</div>
                        <div style="font-size: 1.2rem; font-weight: bold;">${mensaje}</div>
                    </div>
                `;
            }
        }

        getCsrfToken() {
            let token = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
            
            if (!token) {
                token = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
            }
            
            if (!token) {
                const cookies = document.cookie.split(';');
                for (let cookie of cookies) {
                    const [name, value] = cookie.trim().split('=');
                    if (name === 'csrftoken') {
                        token = value;
                        break;
                    }
                }
            }
            
            return token || '';
        }
    }

    // Inicializar
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            console.log('🚀 Inicializando EstadisticaFutbol...');
            window.estadisticaFutbolInstance = new EstadisticaFutbol();
        });
    } else {
        console.log('🚀 Inicializando EstadisticaFutbol...');
        window.estadisticaFutbolInstance = new EstadisticaFutbol();
    }

    document.addEventListener('DOMContentLoaded', function() {
        const radarSelector = document.getElementById('radar-group-selector');
        const radarContainer = document.getElementById('radar-chart-container');
        let radarChart = null;

        function cargarRadar(grupo) {
            if (!radarContainer || !window.equipoId) {
                console.log('No radarContainer o equipoId');
                return;
            }
            if (radarChart) radarChart.dispose();
            // Aumenta el alto aquí:
            radarContainer.style.height = '650px'; // O el valor que prefieras, por ejemplo 600px
            radarContainer.style.maxHeight = '700px'; // Opcional, para limitar el máximo
            console.log('Cargando radar para grupo:', grupo, 'equipo:', window.equipoId);
            fetch(`/ajax/radar-equipo/?equipo_id=${window.equipoId}&grupo=${grupo}`)
                .then(resp => resp.json())
                .then(data => {
                    console.log('Datos radar:', data);
                    radarChart = echarts.init(radarContainer, null, {devicePixelRatio: 2});
                    radarChart.setOption({
                        backgroundColor: 'transparent',
                        tooltip: {trigger: 'item'},
                        legend: {
                            data: ['Equipo', 'Promedio Liga'],
                            top: 10,
                            textStyle: {color: '#fff'}
                        },
                        radar: {
                            indicator: data.labels.map(l => ({name: l, max: data.max})),
                            splitLine: {lineStyle: {color: '#23243a'}},
                            splitArea: {areaStyle: {color: ['#23243a','#181b23']}},
                            axisName: {
                                color: '#00d4ff',
                                fontSize: 13,
                                // 👇 Salto de línea solo al finalizar palabra, cada ~14 caracteres
                                formatter: function(value) {
                                    // Divide en palabras y arma líneas de hasta 14 caracteres
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
                                {value: data.equipo, name: 'Equipo', areaStyle: {color: 'rgba(0,212,255,0.3)'}},
                                {value: data.promedio, name: 'Promedio Liga', areaStyle: {color: 'rgba(255,215,0,0.15)'}}
                            ],
                            symbolSize: 6,
                            lineStyle: {width: 2}
                        }]
                    });
                })
                .catch(err => {
                    console.error('Error cargando radar:', err);
                });
        }

        if (radarSelector) {
            radarSelector.addEventListener('change', e => cargarRadar(e.target.value));
            // Cargar el radar inicial
            cargarRadar(radarSelector.value);
        }
    });
}