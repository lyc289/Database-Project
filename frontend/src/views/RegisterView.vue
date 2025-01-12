<template>
    <div class="register-page">
      <RegisterForm />
    </div>
  </template>
  
  <script>
  import RegisterForm from '@/components/RegisterForm.vue'
  
  export default {
    name: 'RegisterView',
    components: {
      RegisterForm
    }
  }
  </script>