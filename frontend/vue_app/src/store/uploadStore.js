import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axiosBI from '../config/axiosinstance.js'

export const useUploadStore = defineStore('dataset', () => {

  // State
  const uploaded = ref(null)
  const loading = ref(false)

  // Getters
  const hasDataset = computed(() => !!uploaded.value)

  // Actions

  function setUploadedDataset(data) {
    uploaded.value = data
    sessionStorage.setItem('uploadedData', JSON.stringify(data))
  }

  function clearData() {
    uploaded.value = null
    sessionStorage.removeItem('uploadedData')
  }

  function loadFromSession() {
    const raw = sessionStorage.getItem('uploadedData')
    uploaded.value = raw ? JSON.parse(raw) : null
  }

  // 👉 Новата upload логика
  async function uploadFile(file) {
    loading.value = true

    const form = new FormData()
    form.append('file', file)

    try {
      const res = await axiosBI.post('api/datasets/upload/', form)
      setUploadedDataset(res.data)
      return res.data
    } catch (err) {
      console.error('Upload error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    uploaded,
    loading,
    hasDataset,
    setUploadedDataset,
    loadFromSession,
    clearData,
    uploadFile
  }
})
