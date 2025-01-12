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
          <a href="#" class="edit-link" @click="editProfile">编辑资料</a>
          <!-- 新增个性签名显示部分 -->
          <div class="signature" v-if="userInfo.signature">
            <span>个性签名: </span>
            <span>{{ userInfo.signature }}</span>
          </div>
        </div>
      </div>

      <!-- 标签页导航 -->
      <div class="tabs">
        <a 
          v-for="tab in tabs" 
          :key="tab.id"
          :class="{ active: currentTab === tab.id }"
          @click="currentTab = tab.id"
        >
          {{ tab.name }}
        </a>
      </div>

      <!-- 关注列表 -->
      <div id="follower-list" v-if="currentTab === 'follower'">
        <ul class="thread-list">
          <li v-for="item in followerList" :key="item.id" class="user-profile" @click="viewUserInfoDetail(item.user_name)">
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
              {{ item.question }}
              <!-- 时间展示 -->
            </div>
            <div class="date">{{ item.createTime }}</div>
          </li>
        </ul>
      </div>

    </div>
  </div>
</template>

<script>
import SiderView from '@/views/SiderView.vue'

export default {
  name: 'DashboardView',
  components: {
    SiderView
  },
  data() {
    return {
      userInfo: {
        username: '',
        avatar: require('../assets/img/头像.jpg'),
        signature: ''  // 新增默认值
      },
      tabs: [
        {id: 'posts', name: '发帖历史' },
        {id:'follower',name:'关注列表'},
        {id:'collections',name:'收藏列表'},
      ],
      currentTab: 'posts',
      followerList: [

      ],
      postHistory: [

      ],
      collectionList: [
      // { id: 5 } // 空数据，测试边界条件
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
    editProfile() {
      this.$router.push('/edit');
    },
    async fetchUserInfo() {
  try {
    // 修改为带有查询参数的请求，使用用户名 (username) 作为查询参数
    const user_id = localStorage.getItem("username"); // 使用当前用户名，确保与后端一致
    // alert(user_id);
    const response = await fetch(`http://127.0.0.1:8000/api/userinfos/?username=${user_id}`, {
      method: 'GET',
    });

    if (response.ok) {
      const data = await response.json();
      // 更新用户信息
      (data.user_info.nickname)
      this.userInfo = {
        username: data.user_info.nickname||'momo',
        avatar: data.user_info.avatar || require('../assets/img/头像.jpg'),
        signature: data.user_info.intro || '这是一个个性签名的默认值',  // 后端返回的 intro 字段作为个性签名
      };
      this.followerList = (data.followerList || []).map(item => ({
            ...item, // 保留原有数据
            avatar: require('../assets/img/头像.jpg'), // 设置固定的头像路径
          }));
      this.postHistory = data.postHistory || []; // 假设后端返回发帖历史
      this.collectionList = data.collectionList || [];
      (data.postHistory);
    } else {
      console.error('获取用户信息失败:', response.statusText);
    }
  } catch (error) {
    console.error('获取用户信息失败:', error);
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
</style>
