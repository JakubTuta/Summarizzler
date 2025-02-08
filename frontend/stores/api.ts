import axios, { type AxiosResponse } from 'axios'
import { ACCESS_TOKEN } from '~/constants/localStorage'

export const useApiStore = defineStore('api', () => {
  const runtimeConfig = useRuntimeConfig()
  const baseURL = runtimeConfig.public.serverUrl

  const api = axios.create({
    baseURL,
    headers: {
      'Content-Type': 'application/json',
    },
    responseType: 'json',
  })

  api.interceptors.request.use((config) => {
    const accessToken = localStorage.getItem(ACCESS_TOKEN)

    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`
    }

    return config
  }, (error) => {
    return Promise.reject(error)
  })

  const sendRequest = async (
    { url, method, data }:
    { url: string, method: 'GET' | 'POST' | 'PUT' | 'DELETE', data?: any },
  ): Promise<AxiosResponse | null> => {
    let response: AxiosResponse | null = null

    try {
      switch (method) {
        case 'GET':
          response = await api.get(url)
          break
        case 'POST':
          response = await api.post(url, data)
          break
        case 'PUT':
          response = await api.put(url, data)
          break
        default:
          break
      }
    }
    catch (error) {
      console.error(error)

      return null
    }

    return response
  }

  const isResponseOk = (response: AxiosResponse | null): boolean => {
    return response !== null && response.status >= 200 && response.status < 300
  }

  return {
    sendRequest,
    isResponseOk,
  }
})
