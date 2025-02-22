import type { AxiosResponse } from 'axios'
import { AxiosError } from 'axios'
import type { ISummary } from '~/models/summary'
import { mapSummary } from '~/models/summary'
import type { ISummaryPreview } from '~/models/summaryPreview'
import { mapSummaryPreview } from '~/models/summaryPreview'

export const useSummaryStore = defineStore('summary', () => {
  const loading = ref(false)
  const recentlyCreatedId = ref<string | null>(null)
  const recentlyError = ref<string | null>(null)
  const summaries = ref<ISummaryPreview[]>([])
  const lastLoadedObject = ref<ISummary | null>(null)
  const isEmpty = ref(false)
  const searchSummaries = ref<ISummaryPreview[]>([])

  const apiStore = useApiStore()
  const router = useRouter()

  const clearSummaries = () => {
    summaries.value = []
    lastLoadedObject.value = null
    isEmpty.value = false
  }

  const createWebsiteSummary = async (userUrl: string, userPrompt: string, isPrivate: boolean) => {
    recentlyCreatedId.value = null
    recentlyError.value = null
    const url = '/summary/website/'
    const data = { url: userUrl, prompt: userPrompt, private: isPrivate }

    loading.value = true

    const response = await apiStore.sendRequest({
      url,
      method: 'POST',
      data,
    })

    if (apiStore.isResponseOk(response)) {
      const responseObject = response as AxiosResponse
      const createdId = responseObject.data.id
      recentlyCreatedId.value = createdId
      loading.value = false

      return createdId
    }
    else if (response instanceof AxiosError) {
      const responseObject = response as AxiosError
      // @ts-expect-error message
      recentlyError.value = responseObject.response?.data?.message || 'An error occurred'
    }

    loading.value = false

    return null
  }

  const createTextSummary = async (userText: string, userPrompt: string, isPrivate: boolean) => {
    recentlyCreatedId.value = null
    recentlyError.value = null
    const url = '/summary/text/'
    const data = { text: userText, prompt: userPrompt, private: isPrivate }

    loading.value = true

    const response = await apiStore.sendRequest({
      url,
      method: 'POST',
      data,
    })

    if (apiStore.isResponseOk(response)) {
      const responseObject = response as AxiosResponse
      const createdId = responseObject.data.id
      recentlyCreatedId.value = createdId
      loading.value = false

      return createdId
    }
    else if (response instanceof AxiosError) {
      const responseObject = response as AxiosError
      // @ts-expect-error message
      recentlyError.value = responseObject.response?.data?.message || 'An error occurred'
    }

    loading.value = false

    return null
  }

  const createFileSummary = async (formData: FormData | null) => {
    if (!formData) {
      return
    }

    recentlyCreatedId.value = null
    recentlyError.value = null

    const url = '/summary/file/'

    loading.value = true

    const response = await apiStore.sendRequest({
      url,
      method: 'POST',
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    if (apiStore.isResponseOk(response)) {
      const responseObject = response as AxiosResponse
      const createdId = responseObject.data.id
      recentlyCreatedId.value = createdId
      loading.value = false

      return createdId
    }
    else if (response instanceof AxiosError) {
      const responseObject = response as AxiosError
      // @ts-expect-error message
      recentlyError.value = responseObject.response?.data?.message || 'An error occurred'
    }

    loading.value = false
  }

  const getSummaries = async (
    {
      limit = 10,
      privateParam = null,
      meOnly = false,
      sort = 'date',
      contentType = null,
      category = null,
    }: {
      limit: number
      privateParam: boolean | null
      meOnly: boolean
      sort: 'favorites' | 'likes' | 'date'
      contentType: 'text' | 'website' | 'file' | 'video' | null
      category: string | null
    }) => {
    let url = `/summary/?limit=${limit}&me=${meOnly}&sort=${sort}`

    if (lastLoadedObject.value) {
      url += `&startAfter=${lastLoadedObject.value.id}`
    }

    if (privateParam !== null) {
      url += `&private=${privateParam}`
    }

    if (contentType) {
      url += `&contentType=${contentType}`
    }

    if (category) {
      url += `&category=${category}`
    }

    loading.value = true
    const response = await apiStore.sendRequest({ url, method: 'GET' })

    if (apiStore.isResponseOk(response)) {
      loading.value = false

      const mappedSummaries = (response as AxiosResponse).data.map(mapSummaryPreview)
      summaries.value.push(...mappedSummaries)
      lastLoadedObject.value = mappedSummaries[mappedSummaries.length - 1]

      if (mappedSummaries.length < limit) {
        isEmpty.value = true
      }

      return mappedSummaries
    }

    loading.value = false
  }

  const getSummaryById = async (id: string) => {
    loading.value = true
    const url = `/summary/id/${id}/`

    const response = await apiStore.sendRequest({ url, method: 'GET' })

    if (response?.status === 401) {
      loading.value = false

      throw new Error('Unauthorized')
    }

    if (apiStore.isResponseOk(response)) {
      loading.value = false

      return mapSummary((response as AxiosResponse).data)
    }

    loading.value = false

    return null
  }

  const deleteSummary = async (id: string) => {
    const url = `/summary/id/${id}/`

    const response = await apiStore.sendRequest({ url, method: 'DELETE' })

    if (apiStore.isResponseOk(response)) {
      router.push('/panel')

      return true
    }

    return false
  }

  const searchSummary = async (query: string) => {
    const url = `/summary/search/?query=${query}&limit=5`

    const response = await apiStore.sendRequest({ url, method: 'GET' })

    if (apiStore.isResponseOk(response)) {
      const summaries = (response as AxiosResponse).data.map(mapSummaryPreview)

      searchSummaries.value = summaries
    }
  }

  return {
    loading,
    recentlyCreatedId,
    recentlyError,
    summaries,
    isEmpty,
    searchSummaries,
    clearSummaries,
    createWebsiteSummary,
    createTextSummary,
    createFileSummary,
    getSummaries,
    getSummaryById,
    searchSummary,
    deleteSummary,
  }
})
