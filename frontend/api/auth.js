import axios from 'axios'

export const register = async (userData) => {
  return await axios.post('/register', userData)
}

export const login = async (credentials) => {
  return await axios.post('/login', credentials)
}