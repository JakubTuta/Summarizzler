import type { AxiosResponse } from 'axios'
import type { IUser } from '~/models/user'
import { mapUser } from '~/models/user'

export const useUserStore = defineStore('user', () => {
  const user = ref<IUser | null>(null)
  const loading = ref(false)

  const apiStore = useApiStore()

  const resetState = () => {
    user.value = null
    loading.value = false
  }

  const getUser = async () => {
    if (user.value)
      return

    loading.value = true

    const token = localStorage.getItem(ACCESS_TOKEN)

    if (!token) {
      loading.value = false

      return
    }

    const url = `/auth/user/me/`
    const response = await apiStore.sendRequest({
      url,
      method: 'GET',
    })

    if (!apiStore.isResponseOk(response)) {
      loading.value = false

      return
    }

    const responseObject = response as AxiosResponse
    const responseData = responseObject.data
    user.value = mapUser(responseData.user)

    loading.value = false
  }

  return {
    user,
    loading,
    resetState,
    getUser,
  }
})
