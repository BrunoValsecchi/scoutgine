class ScoutGineAPI {
    constructor() {
        this.baseURL = 'https://scoutgine-backend.vercel.app';
    }

    async request(endpoint) {
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                headers: { 'Content-Type': 'application/json' },
                mode: 'cors'
            });
            
            if (!response.ok) {
                throw new Error(`Error ${response.status}: ${response.statusText}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Endpoints principales
    async getLigas() { return this.request('/ligas/'); }
    async getEquipos() { return this.request('/equipo/'); }
    async getJugadores() { return this.request('/stats_jugadores/'); }
    async getComparacion() { return this.request('/comparacion/'); }
    async getRecomendacion() { return this.request('/recomendacion/'); }
    async getStatsEquipos() { return this.request('/stats_equipos/'); }
    async getMenu() { return this.request('/menu/'); }

    // Endpoints específicos
    async getEquipoDetalle(id) { return this.request(`/equipo/${id}/`); }
    async getJugadorDetalle(id) { return this.request(`/jugador/${id}/`); }
}

// Instancia global
window.ScoutGineAPI = new ScoutGineAPI();