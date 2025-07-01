// frontend/app/myapp/services/api.js
import API_BASE_URL from '../config/api.js';

const fetchAPI = async (endpoint) => {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
      },
      mode: 'cors',
      credentials: 'include',
    });
    
    if (!response.ok) {
      throw new Error(`Error: ${response.status} - ${response.statusText}`);
    }
    
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      return await response.json();
    } else {
      return await response.text();
    }
  } catch (error) {
    console.error('ScoutGine API Error:', error);
    throw error;
  }
};

// Servicios específicos para ScoutGine
export const getApiInfo = () => fetchAPI('/');
export const getMenuData = () => fetchAPI('/menu/');
export const getLigasData = () => fetchAPI('/ligas/');
export const getEquiposData = () => fetchAPI('/equipo/');
export const getStatsEquipos = () => fetchAPI('/stats_equipos/');
export const getJugadoresData = () => fetchAPI('/stats_jugadores/');
export const getComparacionData = () => fetchAPI('/comparacion/');
export const getRecomendacionData = () => fetchAPI('/recomendacion/');

// Servicios específicos por ID
export const getEquipoDetalle = (equipoId) => fetchAPI(`/equipo/${equipoId}/`);
export const getJugadorDetalle = (jugadorId) => fetchAPI(`/jugador/${jugadorId}/`);