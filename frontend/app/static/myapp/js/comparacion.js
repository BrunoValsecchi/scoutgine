document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('form-comparar-equipos');
    const equipo1Select = document.getElementById('equipo1-select');
    const equipo2Select = document.getElementById('equipo2-select');
    const grupoSelect = document.getElementById('grupo-select');
    const radarDiv = document.getElementById('radar-comparacion-equipos');
    const btnGraficos = document.getElementById('btn-graficos');
    const btnEstadisticas = document.getElementById('btn-estadisticas');
    const estadisticasDiv = document.getElementById('estadisticas-comparacion');
    let radarChart = null;
    let modo = "graficos";

    // Estadísticas donde menos es mejor
    const STATS_MENOS_ES_MEJOR = [
        "Goles concedidos por partido", "xG concedido",
        "Faltas por partido", "Tarjetas amarillas", "Tarjetas rojas"
    ];

    function compararYMostrar() {
        const equipo1Id = equipo1Select.value;
        const equipo2Id = equipo2Select.value;

        if (!equipo1Id || !equipo2Id || equipo1Id === equipo2Id) return;

        const equipos = JSON.parse(document.getElementById('equipos-data').textContent);
        const equipo1 = equipos.find(eq => eq.id == equipo1Id);
        const equipo2 = equipos.find(eq => eq.id == equipo2Id);
        const gruposStats = JSON.parse(document.getElementById('grupos-stats-data').textContent);

        if (modo === "graficos") {
            // Mostrar selector de grupo y radar, ocultar estadísticas
            grupoSelect.parentElement.querySelector('label').style.display = "";
            grupoSelect.style.display = "";
            estadisticasDiv.style.display = "none";
            radarDiv.style.display = "";

            const grupo = grupoSelect.value;
            const statsGrupo = gruposStats[grupo];
            const labels = statsGrupo.map(([label, field]) => label);
            const fields = statsGrupo.map(([label, field]) => field);
            
            // Usar valores reales, no percentiles
            const data1 = fields.map(field => Number(equipo1[field]) || 0);
            const data2 = fields.map(field => Number(equipo2[field]) || 0);

            // Calcular el máximo dinámico para el radar
            const allValues = [...data1, ...data2];
            const maxValue = Math.max(...allValues) * 1.1; // 10% más para margen

            if (radarChart) radarChart.dispose();
            radarDiv.innerHTML = "";
            radarChart = echarts.init(radarDiv, 'dark', {devicePixelRatio: 2});
            radarChart.setOption({
                backgroundColor: 'transparent',
                tooltip: {
                    trigger: 'item',
                    formatter: function(params) {
                        return `${params.seriesName}<br/>${params.name}: ${params.value}`;
                    }
                },
                legend: {
                    data: [equipo1.nombre, equipo2.nombre],
                    top: 10,
                    textStyle: {color: '#e2e8f0'}
                },
                radar: {
                    indicator: labels.map(l => ({
                        name: l, 
                        max: maxValue,
                        min: 0
                    })),
                    radius: 120,
                    splitLine: {lineStyle: {color: '#2d3748'}},
                    splitArea: {areaStyle: {color: ['#1a202c','#2d3748']}},
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
                        {value: data1, name: equipo1.nombre, areaStyle: {color: 'rgba(0,212,255,0.2)'}},
                        {value: data2, name: equipo2.nombre, areaStyle: {color: 'rgba(255,99,132,0.2)'}}
                    ],
                    symbolSize: 6,
                    lineStyle: {width: 2}
                }]
            });
        } else {
            // Modo estadísticas - OCULTAR SOLO EL SELECT Y LABEL, NO LOS BOTONES
            grupoSelect.parentElement.querySelector('label').style.display = "none";
            grupoSelect.style.display = "none";
            radarDiv.style.display = "none";
            estadisticasDiv.style.display = "";

            // Unificar todas las estadísticas de todos los grupos
            let allStats = [];
            Object.values(gruposStats).forEach(arr => allStats = allStats.concat(arr));
            
            const labels = allStats.map(([label, field]) => label);
            const fields = allStats.map(([label, field]) => field);
            const data1 = fields.map(field => Number(equipo1[field]) || 0);
            const data2 = fields.map(field => Number(equipo2[field]) || 0);
            
            let html = `<table class="tabla-estadisticas"><thead><tr>
                <th>Estadística</th>
                <th>${equipo1.nombre}</th>
                <th>${equipo2.nombre}</th>
            </tr></thead><tbody>`;
            
            for (let i = 0; i < labels.length; i++) {
                let v1 = data1[i], v2 = data2[i];
                let res1 = '', res2 = '';
                
                // Considerar si menos es mejor
                if (STATS_MENOS_ES_MEJOR.includes(labels[i])) {
                    // Para estas stats, el valor MENOR gana
                    if (v1 < v2) res1 = 'resalta';
                    else if (v2 < v1) res2 = 'resalta';
                } else {
                    // Para estas stats, el valor MAYOR gana
                    if (v1 > v2) res1 = 'resalta';
                    else if (v2 > v1) res2 = 'resalta';
                }
                
                html += `<tr>
                    <td>${labels[i]}</td>
                    <td class="${res1}">${v1}</td>
                    <td class="${res2}">${v2}</td>
                </tr>`;
            }
            html += "</tbody></table>";
            estadisticasDiv.innerHTML = html;
        }
    }

    // Botones de modo
    btnGraficos.addEventListener('click', function() {
        modo = "graficos";
        btnGraficos.classList.add('modo-activo');
        btnEstadisticas.classList.remove('modo-activo');
        compararYMostrar();
    });
    
    btnEstadisticas.addEventListener('click', function() {
        modo = "estadisticas";
        btnEstadisticas.classList.add('modo-activo');
        btnGraficos.classList.remove('modo-activo');
        compararYMostrar();
    });

    // Al cambiar selectores, actualiza
    equipo1Select.addEventListener('change', compararYMostrar);
    equipo2Select.addEventListener('change', compararYMostrar);
    grupoSelect.addEventListener('change', compararYMostrar);

    // Inicial
    compararYMostrar();
});