<script setup>
    import { ref } from 'vue'
    import { useAuthStore } from '../store/authStore'
    import { useRouter } from 'vue-router'

    const authStore = useAuthStore()    



    const router = useRouter()
    const registerForm = ref({
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
    }
        
    )  

    function goToLogin() {
        router.push('/')
    }



    const onRegister = async () => {
        try {
            await authStore.registerUser({
                username: registerForm.value.username,
                email: registerForm.value.email,
                password: registerForm.value.password
            })
            router.push('/dashboard')
        } catch (error) {
            console.error('Registration failed:', error)
            alert('Registration failed. Please try again.')
        }
    }


</script>




<template>
    <div class="page center">
        <div class="card">
        <h2>Register an Account</h2>
        <p>Please fill in the details to create an account.</p>
        <form @submit.prevent="onRegister">
            <div class="form-group">
            <label for="username">Username:</label>
            <input type="text" id="username" v-model="registerForm.username" required />
            </div>
            <div class="form-group">
            <label for="email">Email:</label>
            <input type="email" id="email" v-model="registerForm.email" required />
            </div>
            <div class="form-group">
            <label for="password">Password:</label>
            <input type="password" id="password" v-model="registerForm.password" required />
            </div>
            <div class="form-group">
            <label for="confirmPassword">Confirm Password:</label>
            <input type="password" id="confirmPassword" v-model="registerForm.confirmPassword" required />
            
            </div>
            <div class="btn-group">
            <button type="submit" class="btn primary">Register</button>
            <p>If you already have an account, <button class="btn link" @click="goToLogin">Login</button></p>
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
  }
  
  .card {
    background: #fff;
    padding: 2em;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    width: 300px;
  }
  
  .form-group {
    margin-bottom: 1em;
  }
  
  label {
    display: block;
    margin-bottom: 0.5em;
  }
  
  input {
    width: 100%;
    padding: 0.5em;
    box-sizing: border-box;
  }
  
  .btn {
    width: 100%;
    padding: 0.75em;
    background-color: #42b983;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .btn:hover {
    background-color: #369870;
  }
  .btn.link {
    background: none;
    color: #2563eb;
    padding: 0;
    border: none;
    cursor: pointer;
    text-decoration: underline;
    font-size: 1em;
  }


</style>