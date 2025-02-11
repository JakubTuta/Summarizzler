import type { AxiosResponse } from 'axios'
import { AxiosError } from 'axios'
import { type ISummary, mapSummary } from '~/models/summary'

export const useSummaryStore = defineStore('summary', () => {
  const loading = ref(false)
  const recentlyCreatedId = ref<string | null>(null)
  const recentlyError = ref<string | null>(null)
  const summaries = ref<ISummary[]>([])
  const lastLoadedObject = ref<ISummary | null>(null)
  const isEmpty = ref(false)

  const apiStore = useApiStore()

  const clearSummaries = () => {
    summaries.value = []
    lastLoadedObject.value = null
    isEmpty.value = false
  }

  const getWebsiteSummary = async (userUrl: string, userPrompt: string, isPrivate: boolean) => {
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

  const getSummaries = async (
    limit: number = 10,
    privateParam: 'all' | 'true' | 'false' = 'all',
    meOnly: boolean = false,
    sort: 'favorites' | 'likes' | 'date' = 'date',
  ) => {
    loading.value = true
    let url = `/summary/?limit=${limit}&private=${privateParam}&me=${meOnly}&sort=${sort}`

    if (lastLoadedObject.value) {
      url += `&startAfter=${lastLoadedObject.value.id}`
    }

    const response = await apiStore.sendRequest({ url, method: 'GET' })

    if (apiStore.isResponseOk(response)) {
      loading.value = false

      const mappedSummaries = (response as AxiosResponse).data.map(mapSummary)
      summaries.value.push(...mappedSummaries)
      lastLoadedObject.value = mappedSummaries[mappedSummaries.length - 1]

      if (mappedSummaries.length < limit) {
        isEmpty.value = true
      }

      return mappedSummaries
    }

    loading.value = false
  }

  return {
    loading,
    recentlyCreatedId,
    recentlyError,
    summaries,
    isEmpty,
    clearSummaries,
    getWebsiteSummary,
    getSummaries,
  }
})
