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
function goToRegister() {
  router.push('/register')
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
      <h2>Welcome to BI SaaS (DEMO)</h2>
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
        <p>if you don't have an account, <button class="btn link" @click="goToRegister">Register</button></p>
      </div>
      </form>
     
    </div>
  </div>
</template>

<style scoped>
.page.center {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
  margin: 0;
}
.card {
  background: white;
  padding: 2em;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 300px;
}
.field {
  margin-bottom: 1em;
}
label {
  display: block;
  margin-bottom: 0.5em;
  font-weight: bold;
}
input {
  width: 100%;
  padding: 0.5em;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.actions {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.btn {
  padding: 10px 16px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 500;
}   
.btn.primary {
  background: #2563eb;
  color: white;
}
.btn.link {
  background: none;
  color: #2563eb;
  text-decoration: underline;
  padding: 0;
}
</style>


