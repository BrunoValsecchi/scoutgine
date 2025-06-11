document.addEventListener('DOMContentLoaded', function() {
    // Obtener datos pasados desde el template
    const jugadorData = window.jugadorData;
    
    // Obtener el canvas
    const ctx = document.getElementById('estadisticaChart').getContext('2d');
    
    // Crear el gráfico
    const chart = new Chart(ctx, {
        type: 'line', // o 'bar', 'doughnut', etc.
        data: {
            labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'], // Ejemplo
            datasets: [{
                label: jugadorData.estadistica,
                data: [12, 19, 3, 5, 2, 3], // Datos de ejemplo
                borderColor: '#67aaff',
                backgroundColor: 'rgba(103, 170, 255, 0.1)',
                borderWidth: 2,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: `${jugadorData.estadistica} - ${jugadorData.jugadorNombre}`,
                    color: '#fff'
                },
                legend: {
                    labels: {
                        color: '#fff'
                    }
                }
            },
            scales: {
                y: {
                    ticks: {
                        color: '#94a3b8'
                    },
                    grid: {
                        color: '#23243a'
                    }
                },
                x: {
                    ticks: {
                        color: '#94a3b8'
                    },
                    grid: {
                        color: '#23243a'
                    }
                }
            }
        }
    });
});