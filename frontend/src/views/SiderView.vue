<template>
    <nav class="left-nav">
      <div class="link-buttons">
        <router-link to="/dashboard">个人中心</router-link>
        <router-link to="/Home">首页</router-link>
        <router-link to="/post">发帖</router-link>
        <a @click="handleLogout" class="logout-link">登出</a>
      </div>
    </nav>
  </template>
  
  <script>
  export default {
    name: 'SiderView',
    methods: {
      handleLogout() {
        localStorage.removeItem('token')
        this.$router.push('/')
      }
    }
  }
  </script>
  
  <style>
  @import '@/assets/styles/SiderV.css';
  </style>