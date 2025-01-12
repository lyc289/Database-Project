<template>
    <div sidebox>
      <SiderView />
    </div>
    <div class="box">
      <h2>编辑个人资料</h2>
      <form @submit.prevent="handleSubmit">
        <div class="inputBox">
          <input 
            v-model="formData.username" 
            placeholder="如不修改请留空"
          >
          <label>昵称</label>
        </div>
        <div class="inputBox">
          <input 
            type="email" 
            v-model="formData.email" 
            placeholder="如不修改请留空"
          >
          <label>邮箱</label>
        </div>
        <div class="inputBox">
          <input 
            type="password" 
            v-model="formData.password"
            placeholder="如不修改请留空"
          >
          <label>新密码</label>
        </div>
        <div class="inputBox">
          <input 
            v-model="formData.intro"
            placeholder="如不修改请留空"
          >
          <label>个性签名</label>
        </div>
        <!-- <div class="inputBox">
          <input 
            type="file"
            id="file-input"
            name="photo"
            style="display: none"
            @change="handleFileChange"
            accept="image/*"
            ref="fileInput"
          >
          <input 
            type="text"
            class="file-trigger"
            readonly
            @click="$refs.fileInput.click()"
            :value="fileName || ''"
            placeholder="点击选择头像"
          >
          <label>头像</label>
        </div> -->
        <div class="button-group">
          <button class="editprofile" @click="handleSubmit">保存修改</button>
          <button @click="gotodashboard" class = "gotodashboard">放弃修改</button>
        </div>
      </form>
      
    </div>
  </template>
  
  <script>
  
  export default {
    name: 'EditProfileView',
    
    data() {
      return {
        formData: {
          username: '',
          email: '',
          password: '',
          avatar: null,
          current_username: '',
          intro:'',
        },
        fileName: ''
      }
    },
    methods: {
      handleFileChange(e) {
        const file = e.target.files[0];
        if (file) {
          this.formData.avatar = file;
          this.fileName = file.name;
        }
      },
      gotodashboard() {
        this.$router.push('/dashboard');
      },
      async handleSubmit() {
        try {
          // 创建表单数据
          const formData = new FormData();
          formData.append('username', this.formData.username);
          formData.append('email', this.formData.email);
          formData.append('current_username', localStorage.getItem('username'));
          // alert(localStorage.getItem('username'));
          formData.append("intro",this.formData.intro);
          if (this.formData.password) {
            formData.append('password', this.formData.password);
          }
          if (this.formData.avatar) {
            formData.append('avatar', this.formData.avatar);
          }
    
          // 发送POST请求到后端
          const response = await fetch('http://127.0.0.1:8000/api/edit-profile/', {
            method: 'POST',
            body: formData,
            credentials: 'include',
            headers: {
              'Accept': 'application/json'
            }
          });
    
          // 处理响应
          if (response.ok) {
            alert('个人资料更新成功！');
            this.$router.push('/dashboard');
          } else {
            const errorData = await response.json();
            alert(errorData.error || '更新失败，请重试');
          }
        } catch (error) {
          console.error('更新失败:', error);
          alert('更新失败，请检查网络连接');
        }
      }
    }
  }
  </script>
  
  <style scoped>
  @import '../assets/styles/edit.css';
  .file-trigger {
    background: transparent !important;
    cursor: pointer;
  }
  .button-group {
  display: flex;
  gap: 20px; /* 调整间距大小 */
  }

  .gotodashboard {
    background: transparent;
    border: none;
    outline: none;
    color: #fff;
    background: #03a9f4;
    padding: 10px 20px;
    cursor: pointer;
    border-radius: 5px;
    transition: transform 0.1s ease;
  }

  .gotodashboard:hover {
  transform: scale(1.05); /* 鼠标悬停时变大 */
  }
  .editprofile {
    background: transparent;
    border: none;
    outline: none;
    color: #fff;
    background: #03a9f4;
    padding: 10px 20px;
    cursor: pointer;
    border-radius: 5px;
    transition: transform 0.1s ease;
  }
  .editprofile:hover {
  transform: scale(1.05); /* 鼠标悬停时变大 */
  }
</style>