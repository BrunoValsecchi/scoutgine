document.addEventListener('DOMContentLoaded', function() {
    const perfilSelect = document.getElementById('perfil-select');
    const equipoExcluir = document.getElementById('equipo-excluir');
    const limiteJugadores = document.getElementById('limite-jugadores');
    const buscarBtn = document.getElementById('buscar-btn');
    
    const perfilInfo = document.getElementById('perfil-info');
    const perfilNombre = document.getElementById('perfil-nombre');
    const perfilDesc = document.getElementById('perfil-desc');
    
    const loading = document.getElementById('loading');
    const resultadosContainer = document.getElementById('resultados-container');
    const jugadoresLista = document.getElementById('jugadores-lista');
    const noResultados = document.getElementById('no-resultados');
    const resultadosTitulo = document.getElementById('resultados-titulo');
    const resultadosContador = document.getElementById('resultados-contador');

    // ✅ MOSTRAR INFO DEL PERFIL AL SELECCIONAR
    perfilSelect.addEventListener('change', function() {
        const selectedOption = this.options[this.selectedIndex];
        
        if (selectedOption.value) {
            const descripcion = selectedOption.getAttribute('data-descripcion');
            perfilNombre.textContent = selectedOption.text;
            perfilDesc.textContent = descripcion;
            perfilInfo.style.display = 'block';
            buscarBtn.disabled = false;
        } else {
            perfilInfo.style.display = 'none';
            buscarBtn.disabled = true;
        }
    });

    // ✅ BUSCAR JUGADORES
    buscarBtn.addEventListener('click', function() {
        const perfil = perfilSelect.value;
        
        if (!perfil) {
            alert('Por favor selecciona un perfil');
            return;
        }

        buscarJugadores();
    });

    function buscarJugadores() {
        const perfil = perfilSelect.value;
        const equipo = equipoExcluir.value;
        const limite = limiteJugadores.value;

        // Mostrar loading
        loading.style.display = 'block';
        resultadosContainer.style.display = 'none';
        noResultados.style.display = 'none';

        // Construir URL
        const params = new URLSearchParams({
            perfil: perfil,
            limite: limite
        });
        
        if (equipo) {
            params.append('equipo_excluir', equipo);
        }

        // Realizar petición AJAX
        fetch(`/ajax/recomendar-jugadores/?${params.toString()}`)
            .then(response => response.json())
            .then(data => {
                loading.style.display = 'none';
                
                if (data.error) {
                    console.error('Error:', data.error);
                    noResultados.style.display = 'block';
                    return;
                }

                if (data.jugadores && data.jugadores.length > 0) {
                    mostrarResultados(data);
                } else {
                    noResultados.style.display = 'block';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                loading.style.display = 'none';
                noResultados.style.display = 'block';
            });
    }

    function mostrarResultados(data) {
        const jugadores = data.jugadores;
        const perfilInfo = data.perfil_info;

        // Actualizar título y contador
        resultadosTitulo.textContent = `Mejores ${perfilInfo.descripcion}`;
        resultadosContador.textContent = `${data.total} jugadores encontrados`;

        // Limpiar lista anterior
        jugadoresLista.innerHTML = '';

        // Crear cards de jugadores
        jugadores.forEach((jugador, index) => {
            const jugadorCard = crearJugadorCard(jugador, index + 1);
            jugadoresLista.appendChild(jugadorCard);
        });

        // Mostrar resultados
        resultadosContainer.style.display = 'block';
    }

    function crearJugadorCard(jugador, posicion) {
        const card = document.createElement('div');
        card.className = 'jugador-card';
        card.onclick = () => window.location.href = `/jugador/${jugador.id}/`;

        const logoEquipo = jugador.equipo_logo 
            ? `<img src="${jugador.equipo_logo}" alt="${jugador.equipo}">`
            : `<div class="equipo-logo-placeholder"><i class='bx bx-shield'></i></div>`;

        const statsHtml = Object.entries(jugador.stats_destacadas)
            .map(([key, stat]) => `
                <div class="stat-item">
                    <span class="stat-nombre">${stat.nombre_friendly}</span>
                    <span class="stat-valor">${stat.valor}</span>
                </div>
            `).join('');

        card.innerHTML = `
            <div class="jugador-header">
                <div class="jugador-info">
                    <h3>#${posicion} ${jugador.nombre}</h3>
                    <div class="posicion">${jugador.posicion}</div>
                </div>
                <div class="puntuacion-badge">
                    ${jugador.puntuacion}
                </div>
            </div>
            
            <div class="jugador-equipo">
                ${logoEquipo}
                <div class="equipo-info">
                    <div class="equipo-nombre">${jugador.equipo}</div>
                    <div class="jugador-edad">
                        ${jugador.edad ? `${jugador.edad} años` : 'Edad no disponible'} 
                        ${jugador.pais ? `• ${jugador.pais}` : ''}
                    </div>
                </div>
            </div>
            
            <div class="stats-destacadas">
                <h4><i class='bx bx-bar-chart-alt-2'></i> Estadísticas Destacadas</h4>
                <div class="stats-lista">
                    ${statsHtml}
                </div>
            </div>
        `;

        return card;
    }

    // ✅ INICIALIZAR
    buscarBtn.disabled = true;
});