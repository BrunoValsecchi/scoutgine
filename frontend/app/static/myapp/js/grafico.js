
document.addEventListener('DOMContentLoaded', function() {
    // Verificar que jugadoresData tiene al menos dos jugadores
    
    if (jugadoresData.length >= 2) {
      // Asignar los jugadores al formulario
      document.getElementById('jugador1').value = jugadoresData[0].player;
      document.getElementById('jugador2').value = jugadoresData[1].player;
  
      // Crear el gráfico de radar
      crearRadar();
  
      // Inicializar ag-Grid
      const gridOptions = {
        columnDefs: columnasData,
        rowData: jugadoresData,
        defaultColDef: {
          sortable: true,
          filter: true,
          resizable: true,
          flex: 1
        },
        pagination: true,
        paginationPageSize: 10,
        rowClass: function(params) {
          return params.node.rowIndex % 2 === 0 ? 'ag-row-even' : 'ag-row-odd';
        },
        getRowStyle: function(params) {
          if (params.data && params.data.rating > 8) {
            return { 'background-color': 'rgba(0, 255, 0, 0.1)' };
          }
          return null;
        }
      };
  
      // Verificar si el contenedor de ag-Grid existe
      const gridDiv = document.querySelector('#myGrid');
      if (gridDiv) {
        new agGrid.Grid(gridDiv, gridOptions);
      } else {
        console.error("Elemento #myGrid no encontrado en el DOM");
      }
  
      // Aplicar estilo de neón a los contenedores de gráficos
      aplicarEstiloNeonECharts();
    }
  
    // Regenerar el gráfico al enviar el formulario
    document.getElementById('form-comparar').addEventListener('submit', function(e) {
      e.preventDefault();
      crearRadar();
    });
  });
  
  // Función para crear el gráfico de radar
  function crearRadar() {
    const jugador1Nombre = document.getElementById('jugador1').value;
    const jugador2Nombre = document.getElementById('jugador2').value;
  
    const jugador1 = jugadoresData.find(j => j.player === jugador1Nombre);
    const jugador2 = jugadoresData.find(j => j.player === jugador2Nombre);
  
    if (!jugador1 || !jugador2) {
      console.error('No se encontraron los jugadores seleccionados.');
      return;
    }
  
    const statsToShow = Object.keys(jugador1).filter(key => key !== 'player');
    const schema = statsToShow.map(stat => ({ 
      name: stat, 
      max: 100,
      axisLabel: {
        show: true,
        color: '#ffffff',
        fontSize: 10
      }
    }));
  
    const calcularPercentiles = (jugador) => {
      return statsToShow.map(stat => {
        const valores = jugadoresData.map(j => j[stat] || 0);
        const valorJugador = jugador[stat] || 0;
        const percentil = (valores.filter(v => v <= valorJugador).length / valores.length) * 100;
        return Math.round(percentil);
      });
    };
  
    const jugador1Percentiles = calcularPercentiles(jugador1);
    const jugador2Percentiles = calcularPercentiles(jugador2);
  
    const radarChart = echarts.init(document.getElementById('grafico_radar'));
    const option = {
      backgroundColor: 'rgba(10, 10, 10, 0.8)',
      title: {
        text: 'Comparación de Percentiles',
        textStyle: {
          color: '#00ffff',
          fontFamily: "'Orbitron', sans-serif",
          fontWeight: 'bold',
          fontSize: 20,
          textShadow: '0 0 10px rgba(0, 255, 255, 0.7)'
        },
        left: 'center',
        top: 10
      },
      tooltip: {
        trigger: 'item',
        backgroundColor: 'rgba(10, 10, 10, 0.8)',
        borderColor: '#00ffff',
        textStyle: {
          color: '#ffffff'
        }
      },
      legend: {
        data: [jugador1Nombre, jugador2Nombre],
        textStyle: {
          color: '#ffffff',
          fontFamily: "'Rajdhani', sans-serif"
        },
        bottom: 10
      },
      radar: {
        indicator: schema,
        shape: 'circle',
        splitNumber: 4,
        center: ['50%', '50%'],
        radius: '65%',
        name: {
          textStyle: {
            color: '#ffffff',
            fontFamily: "'Rajdhani', sans-serif",
            backgroundColor: 'rgba(0, 0, 0, 0.4)',
            borderRadius: 3,
            padding: [3, 5]
          }
        },
        axisLine: {
          lineStyle: {
            color: 'rgba(0, 255, 255, 0.2)'
          }
        },
        splitLine: {
          lineStyle: {
            color: 'rgba(0, 255, 255, 0.3)'
          }
        },
        splitArea: {
          areaStyle: {
            color: ['rgba(0, 255, 255, 0.05)', 'rgba(0, 255, 255, 0.02)']
          }
        }
      },
      series: [{
        name: 'Comparación',
        type: 'radar',
        data: [
          {
            value: jugador1Percentiles,
            name: jugador1Nombre,
            lineStyle: {
              color: '#00ffff',
              width: 2,
              shadowColor: '#00ffff',
              shadowBlur: 10
            },
            areaStyle: { 
              opacity: 0.2,
              color: new echarts.graphic.RadialGradient(0.5, 0.5, 1, [
                { color: 'rgba(0, 255, 255, 0.5)', offset: 0 },
                { color: 'rgba(0, 255, 255, 0)', offset: 1 }
              ])
            },
            symbol: 'circle',
            symbolSize: 8,
            itemStyle: {
              color: '#00ffff',
              borderColor: '#00ffff',
              borderWidth: 2,
              shadowBlur: 10,
              shadowColor: '#00ffff'
            }
          },
          {
            value: jugador2Percentiles,
            name: jugador2Nombre,
            lineStyle: {
              color: '#ede4e2',
              width: 2,
              shadowColor: '#ff00ff',
              shadowBlur: 10
            },
            areaStyle: { 
              opacity: 0.2,
              color: new echarts.graphic.RadialGradient(0.5, 0.5, 1, [
                { color: 'rgba(255, 0, 255, 0.5)', offset: 0 },
                { color: 'rgba(255, 0, 255, 0)', offset: 1 }
              ])
            },
            symbol: 'circle',
            symbolSize: 8,
            itemStyle: {
              color: '#ff00ff',
              borderColor: '#ff00ff',
              borderWidth: 2,
              shadowBlur: 10,
              shadowColor: '#ff00ff'
            }
          }
        ]
      }]
    };
  
    radarChart.setOption(option);
  }
  
  // Función para aplicar el estilo de neón
  function aplicarEstiloNeonECharts() {
    const chartContainers = document.querySelectorAll('.chart-container');
    chartContainers.forEach(container => {
      container.style.backgroundColor = 'rgba(10, 10, 10, 0.8)';
      container.style.borderRadius = '8px';
      container.style.border = '1px solid #00ffff';
      container.style.boxShadow = '0 0 10px rgba(0, 255, 255, 0.7), 0 0 20px rgba(0, 255, 255, 0.5)';
      container.style.padding = '10px';
      container.style.marginBottom = '20px';
    });
  }
  