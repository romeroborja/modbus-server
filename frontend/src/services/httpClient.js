import axios from 'axios';

const api = axios.create({
  baseURL:
    process.env.NODE_ENV=='development'
    ? process.env.VUE_APP_BASE_URL_API
    : `${window.location.protocol}//${window.location.host}/api`,
})

export {api}
