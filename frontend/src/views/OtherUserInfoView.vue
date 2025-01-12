<template>
  <div sidebox>
    <SiderView />
  </div>
  <div class="dashboard-container">
    <div class="profile_body">
      <!-- 用户资料部分 -->
      <div class="user-profile">
        <img :src="userInfo.avatar" alt="用户头像" class="avatar">
        <div class="user-info">
          <div class="username">{{ userInfo.username }}</div>
          <!-- 新增个性签名显示部分 -->
          <div class="signature" v-if="userInfo.signature">
            <span>个性签名: </span>
            <span>{{ userInfo.signature }}</span>
          </div>
        </div>
        <!-- 新增关注按钮 -->
        <button class="follow-btn" @click="handleFollow">
          {{ is_followed ? '取消关注' : '关注' }}
        </button>
      </div>


      <!-- 标签页导航 -->
      <div class="tabs">
        <a v-for="tab in tabs" :key="tab.id" :class="{ active: currentTab === tab.id }" @click="currentTab = tab.id">
          {{ tab.name }}
        </a>
      </div>

      <!-- 关注列表 -->
      <div id="follower-list" v-if="currentTab === 'follower'">
        <ul class="thread-list">
          <li v-for="item in followerList" :key="item.id" class="user-profile"
            @click="viewUserInfoDetail(item.user_name)">
            <img :src="item.avatar" alt="用户头像" class="avatar">
            <div class="user-info">
              <div class="username">{{ item.nickname || 'momo' }}</div>
              <div class="signature" v-if="item.intro">
                <span>个人简介: </span>
                <span>{{ item.intro }}</span>
              </div>
            </div>
          </li>
        </ul>
      </div>

      <!-- 发帖历史 -->
      <div id="post-history" v-if="currentTab === 'posts'">
        <ul class="thread-list">
          <li v-for="post in postHistory" :key="post.id" class="thread-item" @click="viewPostDetail(post.id)">
            <div class="title">{{ post.title }}</div>
            <div class="date">{{ post.createTime }}</div>
          </li>
        </ul>
      </div>

      <!-- 收藏列表 -->
      <div id="collection-list" v-if="currentTab === 'collections'">
        <ul class="thread-list">
          <li v-for="item in collectionList" :key="item.id" class="thread-item" @click="viewPostDetail(item.id)">
            <div class="title">
              <!-- 判断条件，优先显示 question 或 answer -->
              {{ item.question ? item.question.title : (item.answer ? item.answer.content : '') }}
            </div>
          </li>
        </ul>
      </div>

    </div>
  </div>
</template>

<script>
import SiderView from '@/views/SiderView.vue'

export default {
  props: ['id'],
  name: 'DashboardView',
  components: {
    SiderView
  },
  data() {
    return {
      is_followed: false,
      userInfo: {
        username: '',
        avatar: require('../assets/img/头像.jpg'),
        signature: ''  // 新增默认值
      },
      tabs: [
        { id: 'posts', name: '发帖历史' },
        { id: 'follower', name: '关注列表' },
        { id: 'collections', name: '收藏列表' },
      ],
      currentTab: 'posts',
      followerList: [
        { id: 1, avatar: require('../assets/img/头像.jpg'), nickname: 'testname', intro: 'testintro' },
        { id: 2, avatar: require('../assets/img/头像.jpg'), nickname: 'testname', intro: 'testintro' }
      ],
      postHistory: [
        { id: 1, title: '我的第一篇帖子', createTime: '2024-03-18 10:00' },
        { id: 2, title: '分享经验', createTime: '2024-03-17 09:30' }
      ],
      collectionList: [
        { id: 1, question: { title: 'Test Question 1' } },
        { id: 2, answer: { content: 'Test Answer 1' } },
        { id: 3, question: { title: 'Test Question 2' } },
        { id: 4, answer: { content: 'Test Answer 2' } },
        { id: 5 } // 空数据，测试边界条件
      ]
    }
  },
  created() {
    this.fetchUserInfo();
  },
  methods: {
    viewPostDetail(postId) {
      this.$router.push(`/questions/${postId}`)
    },
    viewUserInfoDetail(user_name) {
      this.$router.push(`/userinfos/${user_name}`)
    },
    async handleFollow() {
      const followeeId = this.id // 被关注用户username
      const followerId = localStorage.getItem("username");// 关注的发起者
      // alert(followeeId)
      // alert(followerId)
      try {
        // 修改为带有查询参数的请求，使用用户名 (username) 作为查询参数
        // alert(user_id);
        const response = await fetch(`http://127.0.0.1:8000/api/follows/`, {
          method: this.is_followed ? 'DELETE' : 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          credentials: 'include',
          body: JSON.stringify({
            follower: followerId, // 关注者的 ID
            followee: followeeId, // 被关注者的 ID
          }),
        });

        if (response.ok) {
          alert('操作成功！');
          this.fetchUserInfo();
        } else {
          console.error('关注失败:', response.statusText);
          alert('操作失败，请稍后重试。');
        }
      } catch (error) {
        console.error('请求失败:', error);
        alert('网络错误，请稍后重试。');
      }
    },
    async fetchUserInfo() {
      // alert("local:"+localStorage.getItem("username"))
      const user_id = this.id
      const followeeId = this.id // 被关注用户username
      const followerId = localStorage.getItem("username");// 关注的发起者
      // alert('followeeId:'+followeeId)
      // alert('followerId:'+followeeId)
      try {
        // 修改为带有查询参数的请求，使用用户名 (username) 作为查询参数
        // alert(user_id);//lyc
        const response = await fetch(`http://127.0.0.1:8000/api/userinfos/?username=${user_id}`, {
          method: 'GET',
        });

        if (response.ok) {
          const data = await response.json();
          // 更新用户信息
          // alert(data.user_info.nickname)
          this.userInfo = {
            username: data.user_info.nickname || 'momo',
            avatar: data.user_info.avatar || require('../assets/img/头像.jpg'),
            signature: data.user_info.intro || '这是一个个性签名的默认值',  // 后端返回的 intro 字段作为个性签名
          };
          this.followerList = (data.followerList || []).map(item => ({
              ...item, // 保留原有数据
              nickname: item.nickname || 'momo', // 如果 nickname 为空则设为 'momo'
              avatar: require('../assets/img/头像.jpg'), // 设置固定的头像路径
          }));
          this.postHistory = data.postHistory || []; // 假设后端返回发帖历史
          this.collectionList = data.collectionList || [];
        } else {
          console.error('获取用户信息失败:', response.statusText);
        }
      } catch (error) {
        console.error('获取用户信息失败:', error);
      }

      const followresponse = await fetch(`http://127.0.0.1:8000/api/follows/?followee=${followeeId}&follower=${followerId}`, {
          method: 'GET',
        });
      if (followresponse.ok){
        const jb=await followresponse.json()
        this.is_followed=jb['follow']
      } else {
        console.error('获取是否关注信息失败:', followresponse.statusText);
      }
    }
  }
}
</script>

<style scoped>
@import '../assets/styles/dashboard.css';
@import '../assets/styles/SiderV.css';

.user-info .signature {
  margin-top: 10px;
  font-style: italic;
  color: #777;
}

.follow-btn {
  margin-left: auto;
  background-color: #f39c12;
  color: white;
  border: none;
  border-radius: 3px;
  padding: 10px 20px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
</style>