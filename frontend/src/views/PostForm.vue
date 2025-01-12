<template>
  <div class="post-page">
    <SiderView />

    <div class="post_body">
      <section class="post-form-container">
        <h1>发布新帖子</h1>
        <form @submit.prevent="submitPost">
          <!-- 帖子标题输入框 -->
          <div class="form-group">
            <label for="title">帖子标题：</label>
            <input 
              type="text" 
              id="title" 
              v-model="postTitle" 
              placeholder="请输入帖子标题"
              required
            />
          </div>
          <!-- 帖子内容输入框 -->
          <div class="form-group">
            <label for="content">帖子内容：</label>
            <textarea 
              v-model="postContent"
              id="content" 
              rows="8" 
              placeholder="在此处分享你的想法..."
              required
            ></textarea>
          </div>
          <!-- 文件上传 -->
          <div class="form-group file-upload-container">
            <label for="photo">选择图片（小于3M）</label>
            <input 
              type="file" 
              id="photo" 
              @change="handleFileChange"
              accept="image/*"
            >
          </div>
          <!-- 提交按钮 -->
          <button type="submit" class="btn-primary">发布帖子</button>
        </form>

        <!-- 消息提示 -->
        <div v-if="message.text" :class="['message', message.type]">
          {{ message.text }}
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import SiderView from '@/views/SiderView.vue'

export default {
  name: 'PostFormView',
  components: {
    SiderView,
  },
  data() {
    return {
      postTitle: '', // 新增标题绑定数据
      postContent: '',
      selectedFile: null,
      message: {
        text: '',
        type: ''
      }
    }
  },
  methods: {
    handleFileChange(event) {
      const file = event.target.files[0]
      if (file && file.size > 3 * 1024 * 1024) {
        this.message = {
          text: '图片大小不能超过3M',
          type: 'error-message'
        }
        event.target.value = ''
        return
      }
      this.selectedFile = file
    },
    async submitPost() {
      try {
        const formData = new FormData()
        formData.append('title', this.postTitle)
        formData.append('content', this.postContent)
        if (this.selectedFile) {
          formData.append('photo', this.selectedFile)
        }
        formData.append("createTime", new Date().toISOString())
        formData.append('asker', localStorage.getItem('username'))
        
        const response = await fetch('http://127.0.0.1:8000/api/questions/', {
          method: 'POST',
          body: formData
        })
        
        if (response.ok) {
          this.message = {
            text: '发布成功！',
            type: 'success-message'
          }
          // 清空表单
          this.postTitle = ''
          this.postContent = ''
          this.selectedFile = null
          
          // 发布成功后跳转到首页
          setTimeout(() => {
            this.$router.push('/home')
          }, 1000)
        } else {
          throw new Error('发布失败')
        }
      } catch (error) {
        console.error('发布失败:', error)
        this.message = {
          text: '发布失败，请重试',
          type: 'error-message'
        }
      }
    },
    handleLogout() {
      localStorage.removeItem('token')
      this.$router.push('/login')
    }
  }
}
</script>

<style>
@import '@/assets/styles/post-form.css';

/* 保证标题和内容框的样式一致 */
textarea, input[type="text"] {
  font-family: "SimSun", "宋体", sans-serif;
  width: 100%;
  padding: 0.5rem;
  border-radius: 3px;
  background: rgba(255, 255, 255, 0.1);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.4);
  border: 1px solid #4a4a4a;
  color: #ffffff;
  font-size: 1rem;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

textarea::placeholder, input[type="text"]::placeholder {
  color: rgba(255, 255, 255, 0.6);
}

textarea:hover, input[type="text"]:hover {
  background: rgba(255, 255, 255, 0.15);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

textarea:focus, input[type="text"]:focus {
  outline: none;
  border-color: rgba(255, 255, 255, 0.8);
  box-shadow: 0 0 6px rgba(4, 189, 189, 0.6);
  background: rgba(255, 255, 255, 0.2);
}
</style>
