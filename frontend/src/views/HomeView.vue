<template>
  <div class="home-container">
    <SiderView />
    <button class="toggle-sider-button" @click="toggleSider">AI</button>
    <aside class="right-ai-sider" v-show="isSiderVisible">
      <div class="ai-response">
        <div v-for="response in aiResponses" :key="response.id" class="response-container">
          <div class="response-content">
            {{ response.content }}
          </div>
        </div>
      </div>
      <div class="send-bar">
        <textarea v-model="userInput" placeholder="输入你的问题..." @input="adjustTextarea"></textarea>
        <div class="button-container">
          <button @click="sendToAI">发送</button>
          <button @click="clearChat">清空</button>
        </div>
      </div>
    </aside>
    <main class="content">
      <div v-for="post in posts" :key="post.id" class="post-container" @click="viewPostDetail(post.id)">
        <div class="post-header">
          <h2 class="post-title">{{ post.title }}</h2>
          <div class="post-meta">
            <span>{{ post.asker + "   " + " " }}</span>
            <span>{{ post.create_date }}</span>
          </div>
        </div>
        <div class="post-content">
          {{ post.content }}
        </div>
      </div>
    </main>
  </div>
</template>

<script>
// import axios from 'axios'
import SiderView from '@/views/SiderView.vue'
export default {
  components: {
    SiderView
  },
  name: 'HomeView',
  data() {
    return {
      posts: [],
      aiResponses: [],
      userInput: '',
      isSiderVisible: false
    }
  },
  methods: {
    async fetchPosts() {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/questions/')

      if (response.ok) {
        const data = await response.json()
        this.posts = data
      } else {
        throw new Error('获取帖子失败')
      }
      } catch (error) {
        console.error('获取帖子失败:', error)
      }
    },
    viewPostDetail(postId) {
      this.$router.push(`/questions/${postId}`)
    },
    createPost() {
      // 实现发帖功能
      this.$router.push('/post')
    },
    logout() {
      // 实现登出功能
      this.$router.push('/login')
    },
    async sendToAI() {
      if (!this.userInput.trim()) {
        alert('请输入有效的问题！');
        return;
      }
      try {
        // 记录用户输入
        const userQuestion = this.userInput.trim(); 
        this.aiResponses.push({ id: this.aiResponses.length + 1, content: `你: ${userQuestion}` });
        this.userInput = ''; // 清空输入框
    
        // 发送请求到后端
        const response = await fetch('http://127.0.0.1:8000/api/ai-response/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ question: userQuestion })
        });
        localStorage.setItem('userQuestion', userQuestion);
        // 处理响应
        if (response.ok) {
          const data = await response.json();
          console.log(data)
          this.aiResponses.push({ id: this.aiResponses.length + 1, content: `AI: ${data.answer.response}` });
        } else {
          console.error('后端返回错误状态:', response.status);
          this.aiResponses.push({ id: this.aiResponses.length + 1, content: 'AI: 请求失败，请稍后重试。' });
        }
      } catch (error) {
        console.error('发送请求时出错:', error);
        this.aiResponses.push({ id: this.aiResponses.length + 1, content: 'AI: 网络错误，请检查你的网络连接。' });
      }
    },
    toggleSider() {
      this.isSiderVisible = !this.isSiderVisible;
    },
    clearChat() {
      this.aiResponses = [];
    },
  },
  created() {
    this.fetchPosts()
  }
}
</script>

<style scoped>
@import '@/assets/styles/SiderV.css';
@import '@/assets/styles/background.css';
@import '@/assets/styles/RightAISider.css';
.home-container {
    width: 100%;
    min-height: 100vh;
    padding: 20px;
    background: url(../assets/img/post.jpg);
    background-size: 100%;
    background-repeat: no-repeat;
    background-attachment: fixed;
  }
  
  .header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 60px;
    background: rgba(0, 0, 0, .6);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
    z-index: 100;
  }
  
  .header-title {
    color: #fff;
    font-size: 20px;
  }
  
  .header-actions {
    display: flex;
    gap: 20px;
  }
  
  .header-button {
    background: transparent;
    border: 1px solid #03a9f4;
    color: #fff;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s;
  }
  
  .header-button:hover {
    background: #03a9f4;
  }
  
  .content {
    margin-top: 80px;
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
  }
  
  .post-container {
    margin-bottom: 20px;
    padding: 20px;
    background: rgba(0, 0, 0, .4);
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, .1);
  }
  
  .post-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(255, 255, 255, .1);
  }
  
  .post-title {
    color: #fff;
    margin: 0;
  }
  
  .post-meta {
    color: rgba(255, 255, 255, .7);
    font-size: 14px;
  }
  
  .post-content {
    color: #fff;
    line-height: 1.6;
  }
.toggle-sider-button {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 1000;
  width: 40px; /* 设置按钮宽度 */
  height: 40px; /* 设置按钮高度 */
  border-radius: 50%; /* 圆形 */
  background-color: #007bff; /* 蓝色背景 */
  color: #fff; /* 白色文字 */
  border: none; /* 去掉边框 */
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer; /* 鼠标指针 */
  font-size: 16px; /* 字体大小 */
}
</style>