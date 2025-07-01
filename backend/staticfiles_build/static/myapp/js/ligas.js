// AG Grid integración para tablas de posiciones
// Asegúrate de tener AG Grid importado en tu HTML (CDN o npm)
// Ejemplo CDN: <script src="https://cdn.jsdelivr.net/npm/ag-grid-community/dist/ag-grid-community.min.noStyle.js"></script>
// Y el CSS: <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/ag-grid-community/styles/ag-grid.css" />
//           <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/ag-grid-community/styles/ag-theme-alpine.css" />


document.addEventListener('DOMContentLoaded', function() {
    
    // Verificar si AG Grid está disponible
    
    // Busca todas las tablas de posiciones
    const tables = document.querySelectorAll('.standings-table');
    tables.forEach((tableContainer, idx) => {
        
        const table = tableContainer.querySelector('table');
        if (!table) {
            return;
        }
        
        // Extrae los datos de la tabla HTML
        const rows = Array.from(table.querySelectorAll('tbody tr'));
        
        if (rows.length === 0) {
            return;
        }
        
        const rowData = rows.map(row => {
            const cells = row.querySelectorAll('td');
            if (cells.length < 10) {
                return null;
            }
            return {
                Pos: parseInt(cells[0]?.textContent.trim()) || 0,
                Equipo: cells[1]?.textContent.trim() || '',
                PJ: parseInt(cells[2]?.textContent.trim()) || 0,
                PG: parseInt(cells[3]?.textContent.trim()) || 0,
                PE: parseInt(cells[4]?.textContent.trim()) || 0,
                PP: parseInt(cells[5]?.textContent.trim()) || 0,
                GF: parseInt(cells[6]?.textContent.trim()) || 0,
                GC: parseInt(cells[7]?.textContent.trim()) || 0,
                DIF: parseInt(cells[8]?.textContent.trim()) || 0,
                PTS: parseInt(cells[9]?.textContent.trim()) || 0,
            };
        }).filter(row => row !== null);
        

        // Define las columnas para AG Grid
        const columnDefs = [
            { 
                headerName: 'Pos', 
                field: 'Pos', 
                width: 70,
                cellStyle: function(params) {
                    const pos = params.value;
                    if (pos <= 4) {
                        return { 
                            fontWeight: 'bold', 
                            color: '#2ecc71',
                            backgroundColor: 'rgba(46, 204, 113, 0.1)',
                            borderRadius: '4px',
                            textShadow: '0 0 8px rgba(46, 204, 113, 0.3)'
                        };
                    } else if (pos <= 6) {
                        return { 
                            fontWeight: 'bold', 
                            color: '#f39c12',
                            backgroundColor: 'rgba(243, 156, 18, 0.1)',
                            borderRadius: '4px',
                            textShadow: '0 0 8px rgba(243, 156, 18, 0.3)'
                        };
                    } else if (pos >= 18) {
                        return { 
                            fontWeight: 'bold', 
                            color: '#e74c3c',
                            backgroundColor: 'rgba(231, 76, 60, 0.1)',
                            borderRadius: '4px',
                            textShadow: '0 0 8px rgba(231, 76, 60, 0.3)'
                        };
                    }
                    return { 
                        fontWeight: 'bold', 
                        color: '#ff7817',
                        textShadow: '0 1px 2px rgba(0, 0, 0, 0.3)'
                    };
                }
            },
            { 
                headerName: 'Equipo', 
                field: 'Equipo', 
                flex: 1, 
                minWidth: 150,
                cellStyle: { 
                    fontWeight: '600', 
                    color: '#ffffff',
                    textAlign: 'left',
                    paddingLeft: '12px'
                }
            },
            { 
                headerName: 'PJ', 
                field: 'PJ', 
                width: 60,
                cellStyle: { color: '#e1e1e6', fontWeight: '500' }
            },
            { 
                headerName: 'PG', 
                field: 'PG', 
                width: 60,
                cellStyle: { color: '#e1e1e6', fontWeight: '500' }
            },
            { 
                headerName: 'PE', 
                field: 'PE', 
                width: 60,
                cellStyle: { color: '#e1e1e6', fontWeight: '500' }
            },
            { 
                headerName: 'PP', 
                field: 'PP', 
                width: 60,
                cellStyle: { color: '#e1e1e6', fontWeight: '500' }
            },
            { 
                headerName: 'GF', 
                field: 'GF', 
                width: 60,
                cellStyle: { color: '#e1e1e6', fontWeight: '500' }
            },
            { 
                headerName: 'GC', 
                field: 'GC', 
                width: 60,
                cellStyle: { color: '#e1e1e6', fontWeight: '500' }
            },
            { 
                headerName: 'DIF', 
                field: 'DIF', 
                width: 80,
                cellStyle: function(params) {
                    const value = params.value;
                    if (value > 0) {
                        return {
                            fontWeight: 'bold',
                            color: '#2ecc71',
                            textShadow: '0 0 8px rgba(46, 204, 113, 0.3)'
                        };
                    } else if (value < 0) {
                        return {
                            fontWeight: 'bold',
                            color: '#e74c3c',
                            textShadow: '0 0 8px rgba(231, 76, 60, 0.3)'
                        };
                    }
                    return {
                        fontWeight: 'bold',
                        color: '#ffffff'
                    };
                }
            },
            { 
                headerName: 'PTS', 
                field: 'PTS', 
                width: 70,
                cellStyle: { 
                    fontWeight: 'bold', 
                    color: '#3498db',
                    fontSize: '1rem',
                    textShadow: '0 1px 2px rgba(0, 0, 0, 0.3)'
                }
            },
        ];

        // Crea un div para AG Grid
        const gridDiv = document.createElement('div');
        gridDiv.style.width = '100%';
        gridDiv.className = 'ag-theme-dark-custom';

        // Calcular altura basada en número de equipos
        const calculatedHeight = Math.min(800, Math.max(400, (rowData.length * 45) + 100)); // 45px por fila + 100px para header
        gridDiv.style.height = `${calculatedHeight}px`;

        // Si hay muchos equipos, agregar clase para altura fija
        if (rowData.length > 15) {
            gridDiv.classList.add('large-table');
            gridDiv.style.height = '800px';
        }

        // Reemplaza la tabla con el grid
        table.parentNode.replaceChild(gridDiv, table);
        console.log("Tabla reemplazada por gridDiv");

        // Opciones del grid
        const gridOptions = {
            columnDefs: columnDefs,
            rowData: rowData,
            defaultColDef: {
                resizable: true,
                sortable: true,
                filter: false
            },
            rowHeight: 45,
            headerHeight: 50,
            animateRows: true,
            domLayout: rowData.length <= 15 ? 'autoHeight' : 'normal', // autoHeight para pocas filas
            pagination: false,
            onGridReady: function(params) {
                params.api.sizeColumnsToFit();
                
                // Ajustar altura del contenedor
                if (rowData.length <= 15) {
                    const actualHeight = (rowData.length * 45) + 60; // filas + header
                    gridDiv.style.height = `${actualHeight}px`;
                }
            },
            suppressHorizontalScroll: false,
            suppressVerticalScroll: rowData.length <= 15 // No scroll si hay pocas filas
        };
        
        try {
            if (typeof agGrid.createGrid === 'function') {
                const gridApi = agGrid.createGrid(gridDiv, gridOptions);
            } else if (typeof agGrid.Grid === 'function') {
                new agGrid.Grid(gridDiv, gridOptions);
            } else {
                // Si AG Grid no está disponible, restaurar la tabla original
                gridDiv.parentNode.replaceChild(table, gridDiv);
                return;
            }
        } catch (error) {
            console.error("Error al inicializar AG Grid:", error);
            // En caso de error, restaurar la tabla HTML original
            gridDiv.parentNode.replaceChild(table, gridDiv);
        }
    });
});

