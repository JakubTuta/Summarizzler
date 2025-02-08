import { jwtDecode } from 'jwt-decode'
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
    loading.value = true

    const decodedToken = jwtDecode(localStorage.getItem(ACCESS_TOKEN)!)
    // @ts-expect-error user_id is one of the fields in the token
    const userId = decodedToken.user_id

    const url = `/auth/user/${userId}/`
    const response = await apiStore.sendRequest({
      url,
      method: 'GET',
    })

    if (!apiStore.isResponseOk(response)) {
      loading.value = false

      return
    }

    const responseData = response!.data
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
