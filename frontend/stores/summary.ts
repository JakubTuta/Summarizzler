export const useSummaryStore = defineStore('summary', () => {
  const apiStore = useApiStore()

  const getWebsiteSummary = async (userUrl: string, userPrompt: string) => {
    const url = '/summary/website/'
    const data = { url: userUrl, prompt: userPrompt }

    const response = await apiStore.sendRequest({
      url,
      method: 'POST',
      data,
    })

    console.log(response)
  }

  return {
    getWebsiteSummary,
  }
})
