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

                console.log('Respuesta fetch:', response);

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                console.log('JSON recibido:', data);
                
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

            chartContainer.style.width = '800px';
            chartContainer.style.height = '700px';
            if (!chartContainer || !window.echarts) {
                this.mostrarError('Error de configuración');
                return;
            }

            if (this.dispersionChart) {
                this.dispersionChart.dispose();
            }
            chartContainer.innerHTML = '';

            this.dispersionChart = echarts.init(chartContainer, 'dark', {
                devicePixelRatio: 2
            });

            const scatterData = data.equipos.map(equipo => [
                equipo.stat_principal,
                equipo.stat_comparacion,
                equipo.nombre
            ]);
            const equipoActual = data.equipos.find(eq => eq.es_actual);

            const option = {
                backgroundColor: '#181b23',
                title: {
                    text: `${this.statName} vs ${statComparacion}`,
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
                        const isCurrent = equipoActual && params.data[2] === equipoActual.nombre;
                        return `
                            <div style="font-size:17px;font-weight:bold;color:${isCurrent ? '#FFD700' : '#67aaff'};margin-bottom:6px;">
                                ${isCurrent ? '⭐ ' : ''}${params.data[2]}
                            </div>
                            <div>${this.statName}: <b>${params.data[0]}</b></div>
                            <div>${statComparacion}: <b>${params.data[1]}</b></div>
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
                    name: this.statName,
                    nameLocation: 'middle',
                    nameGap: 40,
                    nameTextStyle: { color: '#fff', fontSize: 18, fontWeight: 600 },
                    axisLabel: { color: '#b0b8c9', fontSize: 15 },
                    axisLine: { lineStyle: { color: '#67aaff', width: 2 } },
                    splitLine: { lineStyle: { color: '#23243a', type: 'dashed' } }
                },
                yAxis: {
                    type: 'value',
                    name: statComparacion,
                    nameLocation: 'middle',
                    nameGap: 60,
                    nameTextStyle: { color: '#fff', fontSize: 18, fontWeight: 600 },
                    axisLabel: { color: '#b0b8c9', fontSize: 15 },
                    axisLine: { lineStyle: { color: '#67aaff', width: 2 } },
                    splitLine: { lineStyle: { color: '#23243a', type: 'dashed' } }
                },
                series: [
                    {
                        type: 'scatter',
                        data: scatterData,
                        symbolSize: function(data) {
                            const equipo = data[2];
                            return equipoActual && equipo === equipoActual.nombre ? 28 : 18;
                        },
                        itemStyle: {
                            color: function(params) {
                                const equipo = params.data[2];
                                if (equipoActual && equipo === equipoActual.nombre) {
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
                    }
                ]
            };

            this.dispersionChart.setOption(option);

                    // --- FIX: Usa una referencia única para el handler ---
            if (this._resizeHandler) {
                window.removeEventListener('resize', this._resizeHandler);
            }
            this._resizeHandler = () => {
                if (this.dispersionChart && !this.dispersionChart.isDisposed()) {
                    this.dispersionChart.resize();
                }
            };
            window.addEventListener('resize', this._resizeHandler);
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

    function cargarRadar(grupo = 'ofensivos') {
        const radarContainer = document.getElementById('radar-chart-container');
        if (!radarContainer || !window.equipoId) return;
        radarContainer.style.width = '100%';
        radarContainer.style.maxWidth = '600px';
        radarContainer.style.height = '620px';
        radarContainer.style.margin = '0 auto';

        fetch(`/ajax/radar-equipo/?equipo_id=${window.equipoId}&grupo=${grupo}`)
            .then(resp => resp.json())
            .then(data => {
                const radarChart = echarts.init(radarContainer, null, {devicePixelRatio: 2});
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
                            formatter: function(value) {
                                // Salto de línea solo al finalizar palabra, cada ~14 caracteres
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
            });
    }

    document.addEventListener('DOMContentLoaded', function() {
        if (window.equipoId) {
            cargarRadar('ofensivos');
            const radarSelector = document.getElementById('radar-group-selector');
            if (radarSelector) {
                radarSelector.addEventListener('change', function() {
                    cargarRadar(this.value);
                });
            }
        }
    });
}