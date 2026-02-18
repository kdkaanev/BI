<script setup>
import { onMounted, ref } from "vue";
import axiosBI from "../config/axiosinstance.js";
import { useRouter } from "vue-router";
import { useUploadStore } from "../store/uploadStore.js";
import { useAuthStore } from "../store/authStore.js";
const uploadStore = useUploadStore();
const authStore = useAuthStore();
const router = useRouter();

const loading = ref(false);
const fileInput = ref(null);

const chooseFile = () => fileInput.value.click();

onMounted(() => {
  authStore.initAuth();
});

const onDrop = (e) => {
  const file = e.dataTransfer.files[0];
  if (file) upload(file);
};

const onFileChange = (e) => {
  const file = e.target.files[0];
  if (file) upload(file);
};

const upload = async (file) => {
  try {
    await uploadStore.uploadFile(file)
    router.push('/dashboard')
    
  } catch (err) {
    alert('Upload error: ' + (err.response?.data?.detail || err.message))
  }
}

</script>

<template>
  <div class="upload-page">
    <h1>Upload Dataset</h1>

    <!-- Drag & Drop box -->
    <div
      class="drop-box"
      @dragover.prevent
      @drop.prevent="onDrop"
      @click="chooseFile"
    >
      <p>Drag & drop your file here</p>
      <p class="or">or click to choose</p>
    </div>

    <!-- Hidden file input -->
    <input
      ref="fileInput"
      type="file"
      accept=".csv,.txt,.xls,.xlsx"
      class="hidden-input"
      @change="onFileChange"
    />

    <div class="links">
      <button class="upload-btn" :disabled="loading" @click="chooseFile">
      {{ loading ? "Uploading..." : "Upload File" }}
    </button>
    <router-link to="/dashboard" class="dashboard-link">Go to Dashboard</router-link>
    </div>
  </div>
</template>
<style scoped>
.upload-page {
  max-width: 600px;
  margin: 40px auto;
  text-align: center;
  font-family: sans-serif;
}

.drop-box {
  border: 2px dashed #aaa;
  padding: 40px;
  border-radius: 12px;
  cursor: pointer;
  transition: 0.2s;
}

.drop-box:hover {
  border-color: #333;
  background: #fafafa;
}

.or {
  margin-top: 8px;
  font-size: 14px;
  color: #777;
}

.hidden-input {
  display: none;
}

.upload-btn {
  margin-top: 20px;
  padding: 12px 24px;
  font-size: 16px;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.upload-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.dashboard-link {
  display: inline-block;
  margin-top: 16px;
  color: #4f46e5;
  text-decoration: none;
}
.dashboard-link:hover {
  text-decoration: underline;
}
.links {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
