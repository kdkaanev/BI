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
            
            <button type="submit" class="btn">Register</button>
        </form>
        </div>
    </div>
</template>