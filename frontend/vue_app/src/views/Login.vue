<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/authStore' 
import { onMounted, ref } from 'vue'
const authStore = useAuthStore()
const router = useRouter()
const loginData = ref({
  username: '',
  password: ''
})


function goUploadWizard() {
  router.push('/upload')
}


const onLogin = async () => {
  try {
    await authStore.loginUser({
      username: loginData.value.username,
      password: loginData.value.password
    })
    goUploadWizard()
  } catch (error) {
    console.error('Login failed:', error)
    alert('Login failed. Please check your credentials and try again.')
  }
}
onMounted(() => {
  if (authStore.getCurrentUser()) {
    goUploadWizard()
  }
})

</script>

<template>
  <div class="page center">
    <div class="card">
      <h2>Welcome to BI SaaS (demo)</h2>
      <form @submit.prevent="onLogin">
 <div class="field">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="loginData.username" />
      </div>
      <div class="field">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="loginData.password" />
      </div>
      <div class="actions">
        <button class="btn primary" type="submit">Login</button>
      </div>
      </form>
     
    </div>
  </div>
</template>


