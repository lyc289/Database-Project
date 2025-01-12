<template>
  <div class="question-view-container">
    <SiderView />
    <div class="content-box">
      <!-- 发帖内容 -->
      <div v-if="post" class="post-container">
        <div class="post-header">
          <span class="poster" @click="viewUserInfoDetail(post.asker)" style="cursor:pointer; color: white; text-decoration: underline;">发帖人：{{ post.nickname }}</span>
          <button @click="toggleFavorite" class="favorite-button">
            {{ isFavorited ? '取消收藏' : '收藏' }}
          </button>
        </div>
        <div class="post-content">
          <h2>{{ post.title }}</h2>
          <p>{{ post.content }}</p>
          <img v-if="post.images" :src="getImageUrl(post.images)" alt="帖子图片" class="post-image">
        </div>
        <div class="post-stats">
          <span>评论数：{{ comments.length }}</span>
          <span v-if="totalReplyCount !== undefined">总回复数：{{ totalReplyCount }}</span> <!-- 显示总回复数 -->
          <span class="post-time">发布时间：{{ formatTime(post.create_date) }}</span>
        </div>
      </div>
      <p v-else>加载中</p>
      
      <!-- 评论表单部分 -->
      <div class="comments-section">
        <h3>发送评论：</h3>
        <form @submit.prevent="submitComment" class="comment-form">
          <textarea 
            v-model="newComment"
            name="content"
            placeholder="输入您的评论..."
          ></textarea>
          <input type="submit" name="submit" value="发布评论" class="submit-button">
        </form>
      </div>

      <!-- 评论列表部分 -->
      <div class="comments-list">
        <h3>评论列表：</h3>
        <div v-if="comments.length > 0">
          <div v-for="comment in comments" :key="comment.id" class="comment-item">
            <div class="comment-header" @click="toggleReplyForm(comment.id)">
              <span class="commenter" @click.stop="viewUserInfoDetail(comment.commenter_name)" style="cursor:pointer; color: whitetext-decoration=underline;">{{ comment.nickname }}</span>
              <span class="comment-time">{{ formatTime(comment.create_date) }}</span>
            </div>
            <div class="comment-content">
              <span>{{ comment.content }}</span>
            </div>

            <!-- 可展开的回复表单 -->
            <div v-if="activeCommentId === comment.id" class="reply-section">
              <textarea 
                v-model="newReply[comment.id]"
                placeholder="回复此评论..."
                class="reply-textarea"
              ></textarea>
              <button @click="submitReply(comment.id)" class="reply-button">回复</button>
            </div>
      
            <!-- 回复列表 -->
            <div v-if="comment.replies && comment.replies.length > 0" class="replies">
              <div v-for="reply in comment.replies" :key="reply.id" class="reply-item">
                <div class="comment-header">
                  <span class="reply-commenter" @click="viewUserInfoDetail(reply.commenter_name)" style="cursor:pointer; color: white">{{ reply.nickname }}</span>
                  <span class="reply-time">{{ formatTime(reply.create_date) }}</span>
                </div>
                <div class="comment-content">
                  <span>{{ reply.content }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <p v-else>该帖子暂无评论。</p>
      </div>
    </div>
  </div>
</template>

  <script>
  import SiderView from '@/views/SiderView.vue'
  
  export default {
    name: 'QuestionView',
    components: {
      SiderView
    },
    data() {
      return {
        post: null,
        comments: [],
        newComment: '',
        newReply: {},
        currentUser: null,
        userType: null,
        activeCommentId: null,
        postId: null,
        isFavorited: false // 初始化为 false
      }
    },
    computed: {
      canDeletePost() {
        return this.currentUser === this.post?.poster || 
               ['admin', 'moderator'].includes(this.userType)
      }
    },
    methods: {
      viewUserInfoDetail(user_name) {
        const my_username = localStorage.getItem('username');
        if (user_name!=my_username){
        this.$router.push(`/userinfos/${user_name}`)
        } else {
          this.$router.push(`/dashboard`)
        }
    },
      async fetchPostDetails() {
        try {
          const response = await fetch(`http://127.0.0.1:8000/api/questions/${this.postId}/`)
          if (response.ok) {
            this.post = await response.json()
          } else {
            console.error('加载帖子详情失败:', response.statusText)
          }
        } catch (error) {
          console.error('加载帖子详情失败:', error)
        }
        const likerepsonse = await fetch(`http://127.0.0.1:8000/api/likes/?post_id=${this.postId}&username=${localStorage.getItem('username')}`)
        if(likerepsonse.ok){
          const jb=await likerepsonse.json()
          this.isFavorited=jb['like']
          // alert(this.isFavorited)
        }
      },
      async toggleFavorite() {
        const username = localStorage.getItem('username');
        if (!username) {
          alert('请先登录');
          return;
        }

        try {
          const response = await fetch(`http://127.0.0.1:8000/api/likes/`, {
            method: this.isFavorited ? 'DELETE' : 'POST', // 根据状态发送不同请求
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({
              question: this.postId,
              username: username
            })
          });

          if (response.ok) {
            this.isFavorited = !this.isFavorited; // 切换收藏状态
          } else {
            const errorData = await response.json();
            alert(errorData.error || '操作失败');
          }
        } catch (error) {
          console.error('收藏操作失败:', error);
        }


      },
      async fetchComments() {
        try {
          const response = await fetch(`http://127.0.0.1:8000/api/comments/?question=${this.postId}`)
          if (response.ok) {
            this.comments = await response.json()
          } else {
            console.error('加载评论失败:', response.statusText)
          }
        } catch (error) {
          console.error('加载评论失败:', error)
        }
      },
      async submitComment() {
        if (!this.newComment.trim()) return
        
        const username = localStorage.getItem('username')
        if (!username) {
          alert('请先登录')
          return
        }
  
        try {
          const response = await fetch('http://127.0.0.1:8000/api/comments/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({
              content: this.newComment,
              username: username,
              question: parseInt(this.postId),
              parent: null
            })
          })
  
          if (response.ok) {
            this.newComment = ''
            await this.fetchComments()
          } else {
            const errorData = await response.json()
            alert(errorData.error || '发布评论失败')
          }
        } catch (error) {
          console.error('发布评论失败:', error)
        }
      },
      async submitReply(commentId) {
        const replyContent = this.newReply[commentId]?.trim()
        if (!replyContent) return
  
        const username = localStorage.getItem('username')
        if (!username) {
          alert('请先登录')
          return
        }
  
        try {
          const response = await fetch('http://127.0.0.1:8000/api/comments/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({
              content: replyContent,
              username: username,
              question: parseInt(this.postId),
              parent: commentId
            })
          })
  
          if (response.ok) {
            this.newReply[commentId] = ''
            this.activeCommentId = null
            await this.fetchComments()
          } else {
            const errorData = await response.json()
            alert(errorData.error || '回复失败')
          }
        } catch (error) {
          console.error('回复失败:', error)
        }
      },
      toggleReplyForm(commentId) {
        if (this.activeCommentId === commentId) {
          this.activeCommentId = null
        } else {
          this.activeCommentId = commentId
        }
      },
      formatTime(timeString) {
        return new Date(timeString).toLocaleString()
      },
      getImageUrl(imagePath) {
        // 确保图片路径以 /media/ 开头
        return `http://127.0.0.1:8000/api${imagePath}`;
       
      },
    },

    created() {
      this.currentUser = localStorage.getItem('username')
      this.userType = localStorage.getItem('userType')
      this.postId = this.$route.params.id
      if (!this.postId) {
        console.error('postId 未定义，请检查路由配置和传递参数')
        return
      }
      this.fetchPostDetails()
      console.log(this.isFavorited)
      this.fetchComments()
    }
  }
  </script>
  
  <style scoped src="@/assets/styles/question.css"></style>
  
  <style scoped>
  @import '../assets/styles/question.css';
  
  /* 新增或覆盖的样式 */
  .question-view-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
  }
  
  .content-box {
    background-color: rgba(0, 0, 0, 0.2);
    border-radius: 10px;
    padding: 20px;
    width: 100%;
    max-width: 800px;
  }
  
  .post-header, .comment-header, .reply-commenter {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .comment-header, .reply-header {
    margin-bottom: 10px;
  }
  
  .comment-item, .reply-item {
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 5px;
    padding: 10px;
    margin-bottom: 10px;
  }
  
  .comment-content, .reply-content {
    margin-top: 5px;
    margin-bottom: 10px;
  }
  
  .delete-button, .reply-button, .submit-button {
    background-color: rgba(4, 189, 189, 0.8);
    color: white;
    border: none;
    border-radius: 3px;
    padding: 5px 10px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .delete-button:hover, .reply-button:hover, .submit-button:hover {
    background-color: rgba(4, 189, 189, 1);
  }
  
  .reply-section {
    margin-top: 10px;
  }
  
  .reply-textarea {
    width: 100%;
    height: 60px;
    padding: 5px;
    border-radius: 3px;
    border: 1px solid #4a4a4a;
    resize: vertical;
    background: rgba(0, 0, 0, 0.1);
    color: #fff;
  }
  
  .replies {
    margin-top: 10px;
    padding-left: 20px;
    border-left: 2px solid #ccc;
  }
  
  .reply-item {
    margin-bottom: 10px;
  }
  
  .reply-commenter, .reply-time {
    font-weight: bold;
    color: #fff;
  }
  
  .commenter {
    font-weight: bold;
    color: #fff;
  }
  
  .comment-time {
    color: #fff;
  }
  
  h3 {
    color: #fff;
    margin-bottom: 10px;
  }
  
  .comment-form textarea {
    width: 100%;
    height: 80px;
    padding: 10px;
    border-radius: 5px;
    border: none;
    resize: vertical;
    background: rgba(255, 255, 255, 0.1);
    color: #fff;
  }
  
  .comment-form .submit-button {
    margin-top: 10px;
  }
  
  /* 响应式设计 */
  @media (max-width: 768px) {
    .content-box {
      width: 90%;
    }
  
    .comment-item, .reply-item {
      width: 100%;
    }
  
    #page-post, #comments-section, #page-comment {
      width: 100%;
      position: static;
      margin: 20px 0;
    }
  }

  .favorite-button {
  background-color: #f39c12;
  color: white;
  border: none;
  border-radius: 3px;
  padding: 5px 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.favorite-button:hover {
  background-color: #e67e22;
}
.left-nav {
    width: 200px;
    height: 100vh;
    position: fixed;
    left: 0;
    top: 0;
    padding: 20px;
    background: rgba(255, 255, 255, 0.1);
  }
  
  .link-buttons {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .link-buttons a {
    text-decoration: none;
    color: #4a4a4a;
    padding: 0.5rem;
    border-radius: 3px;
    cursor: pointer;
    font-weight: bold;
    transition: all 0.3s ease;
  }
  
  .link-buttons a:hover {
    background: rgba(112, 91, 91, 0.2);
  }
  
  .link-buttons a.router-link-active {
    background: rgba(4, 189, 189, 0.2);
    color: rgb(4, 189, 189);
  }
  </style>
