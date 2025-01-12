<template>
    <div class="box">
      <h2>登录</h2>
      <form @submit.prevent="handleLogin">
        <div class="inputBox">
          <input 
            v-model="username"
            @input="e => username = e.target.value"
            required
          >
          <label>用户名</label>
        </div>
        <div class="inputBox">
          <input 
            type="password" 
            v-model="password"
            @input="e => password = e.target.value"
            required
          >
          <label>密码</label>
        </div>
        <!-- <div class="inputBox">
          <input 
            v-model="verificationCode"
            @input="e => verificationCode = e.target.value"
            required
          >
          <label>验证码</label>
        </div> -->
        <button type="submit" >登录</button>
        <div>
          <a href="/register" class="register">还没有账号？立即注册</a>
        </div>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    name: 'LoginView',
    data() {
      return {
        username: '',
        password: '',
        verificationCode: ''
      }
    },
    methods: {
    async handleLogin() {
      try {
        // 创建表单数据
        const formData = new FormData();
        formData.append('username', this.username);
        formData.append('password', this.password);
        formData.append('code', this.verificationCode);

        // 发送POST请求到后端
        const response = await fetch('http://127.0.0.1:8000/api/login/', {
          method: 'POST',
          body: formData,
          // 如果需要携带cookie，添加以下配置
          credentials: 'include',
          // 如果遇到跨域问题，可能需要以下请求头
          headers: {
            'Accept': 'application/json',
          }
        });

        // 处理响应
        const result = await response.text();
        console.log('登录响应：', result);

        if (response.ok) {
          // 登录成功
          alert('登录成功！');
          localStorage.setItem('token', result);
          localStorage.setItem('username', this.username);
          localStorage.setItem('password', this.password);
          this.$router.push('/Home');
        } else {
          // 登录失败
          alert(result);
        }
      } catch (error) {
        console.error('登录请求失败：', error);
        alert('登录失败，请检查网络连接');
      }
    }
  }
}
</script>
  
  <style scoped>
  @import '../assets/styles/background.css';
  </style>