// frontend/app/myapp/config/api.js
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://scoutgine-backend.vercel.app'  // Tu backend en Vercel
  : 'http://localhost:8000';               // Para desarrollo local

export default API_BASE_URL;