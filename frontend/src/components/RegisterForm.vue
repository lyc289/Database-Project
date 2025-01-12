<template>
  <div class="box">
    <h2>注册</h2>
    <form @submit.prevent="handleSubmit">
      <div class="inputBox">
        <input 
          type="email" 
          v-model="formData.email" 
          required
        >
        <label>邮箱</label>
      </div>
      <div class="inputBox">
        <input 
          v-model="formData.username" 
          required
        >
        <label>用户名</label>
      </div>
      <div class="inputBox">
        <input 
          type="password" 
          v-model="formData.password" 
          required
        >
        <label>密码</label>
      </div>
      <button type="submit">注册</button>
    </form>
    <router-link class="register" to="/">
      已有账号？点击这里登录
    </router-link>
  </div>
</template>

<script>
export default {
name: 'RegisterForm',
data() {
  return {
    formData: {
      email: '',
      username: '',
      password: ''
    }
  }
},
methods: {
  async handleSubmit() {
    try {
      // 创建表单数据
      const formData = new FormData();
      formData.append('email', this.formData.email);
      formData.append('username', this.formData.username);
      formData.append('password', this.formData.password);

      // 发送POST请求到后端
      const response = await fetch('http://127.0.0.1:8000/api/register/', {
        method: 'POST',
        body: formData,
        credentials: 'include',
        headers: {
          'Accept': 'application/json',
        }
      });

      // 处理响应
      const result = await response.text();
      console.log('注册响应：', result);

      if (response.ok) {
        // 注册成功
        alert('注册成功！');
        // 跳转到登录页
        this.$router.push('/');
      } else {
        // 注册失败
        alert(result || '注册失败，请重试');
      }
    } catch (error) {
      console.error('注册请求失败：', error);
      alert('注册失败，请检查网络连接');
    }
  }
}
}
</script>

<style scoped>
@import '../assets/styles/background.css';
</style>