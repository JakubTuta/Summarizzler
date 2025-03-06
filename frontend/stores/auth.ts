import type { AxiosResponse } from 'axios'
import { jwtDecode } from 'jwt-decode'
import { type IUser, mapUser } from '~/models/user'

export const useAuthStore = defineStore('auth', () => {
  const loading = ref(false)
  const initLoading = ref(true)
  const user = ref<IUser | null>(null)

  const apiStore = useApiStore()
  const userStore = useUserStore()
  const router = useRouter()
  const summaryStore = useSummaryStore()

  const clearAuth = () => {
    localStorage.removeItem(ACCESS_TOKEN)
    localStorage.removeItem(REFRESH_TOKEN)
    user.value = null
    userStore.resetState()
  }

  const login = async (username: string, password: string) => {
    const url = '/auth/login/'
    const requestData = { username, password }

    loading.value = true

    const response = await apiStore.sendRequest({
      url,
      method: 'POST',
      data: requestData,
    })

    if (!apiStore.isResponseOk(response)) {
      loading.value = false

      return
    }

    const responseObject = response as AxiosResponse<{ tokens: { access: string, refresh: string }, user: IUser }>
    const responseData = responseObject.data

    const tokens = responseData.tokens
    localStorage.setItem(ACCESS_TOKEN, tokens.access)
    localStorage.setItem(REFRESH_TOKEN, tokens.refresh)

    user.value = mapUser(responseData.user)

    loading.value = false

    router.push('/panel')
  }

  const logout = () => {
    clearAuth()
    summaryStore.resetState()
    router.push('/')
  }

  const register = async (email: string, username: string, password: string) => {
    const url = '/auth/register/'
    const requestData = { email, username, password }

    loading.value = true

    const response = await apiStore.sendRequest({
      url,
      method: 'POST',
      data: requestData,
    })

    if (!apiStore.isResponseOk(response)) {
      loading.value = false

      return
    }

    const responseObject = response as AxiosResponse<{ tokens: { access: string, refresh: string }, user: IUser }>
    const responseData = responseObject.data

    const tokens = responseData.tokens
    localStorage.setItem(ACCESS_TOKEN, tokens.access)
    localStorage.setItem(REFRESH_TOKEN, tokens.refresh)

    user.value = mapUser(responseData.user)

    loading.value = false

    router.push('/panel')
  }

  const refreshToken = async () => {
    const refreshToken = localStorage.getItem(REFRESH_TOKEN)

    if (!refreshToken) {
      return false
    }

    const url = '/auth/token/refresh/'
    const requestData = { refresh: refreshToken }

    const response = await apiStore.sendRequest({
      url,
      method: 'POST',
      data: requestData,
    })

    if (!apiStore.isResponseOk(response)) {
      clearAuth()
      router.push('/')

      return false
    }

    const responseObject = response as AxiosResponse<{ access: string }>
    const accessToken = responseObject.data.access
    localStorage.setItem(ACCESS_TOKEN, accessToken)

    return true
  }

  const isTokenValid = async () => {
    const token = localStorage.getItem(ACCESS_TOKEN)

    if (!token) {
      return false
    }

    const decodedToken = jwtDecode(token)
    const tokenExp = decodedToken.exp || 0
    const now = Math.floor(Date.now() / 1000)

    if (tokenExp < now) {
      return await refreshToken()
    }
    else {
      return true
    }
  }

  const init = async () => {
    const tokenValid = await isTokenValid()

    if (!tokenValid) {
      clearAuth()
      initLoading.value = false

      return
    }

    const url = `/auth/user/me/`
    const response = await apiStore.sendRequest({
      url,
      method: 'GET',
    })

    if (!apiStore.isResponseOk(response)) {
      clearAuth()
      initLoading.value = false

      if (!['/auth/login', '/auth/register'].includes(router.currentRoute.value.path)) {
        router.push('/auth/login')
      }

      return
    }

    const responseObject = response as AxiosResponse<{ user: IUser }>
    const responseData = responseObject.data
    user.value = mapUser(responseData.user)

    if (['/', '/auth/login', '/auth/register'].includes(router.currentRoute.value.path)) {
      initLoading.value = false
      router.push('/panel')
    }

    initLoading.value = false
  }

  return {
    loading,
    initLoading,
    user,
    login,
    logout,
    register,
    refreshToken,
    isTokenValid,
    init,
  }
})
