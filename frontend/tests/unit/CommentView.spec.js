import { mount } from '@vue/test-utils'
import CommentView from '@/views/CommentView.vue'
import SiderView from '@/views/SiderView.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: []
})

describe('CommentView.vue 帖子显示测试', () => {
  const mockPost = {
    id: 1,
    poster: '测试用户',
    postTime: '2024-03-21T10:00:00',
    content: '这是一个测试帖子内容',
    imageUrl: 'test.jpg',
    viewsCount: 10,
    likesCount: 5,
    commentsCount: 3
  }

  beforeEach(() => {
    // 模拟Django后端的API响应
    global.fetch = jest.fn((url) => {
      if (url.includes('/api/posts/')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockPost),
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': 'mock-csrf-token'
          }
        })
      }
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve({})
      })
    })
  })

  it('成功发送帖子并显示', async () => {
    const wrapper = mount(CommentView, {
      global: {
        components: { SiderView },
        plugins: [router],
        mocks: {
          $route: {
            params: { id: '1' }
          }
        }
      }
    })

    // 等待初始数据加载
    await wrapper.vm.fetchPostDetails()
    await wrapper.vm.$nextTick()

    // 验证帖子内容是否正确显示
    expect(wrapper.find('.post-content p').text()).toBe(mockPost.content)
    expect(wrapper.find('.post-stats').text()).toContain(`浏览量：${mockPost.viewsCount}`)
    
    // 验证图片是否正确显示
    const img = wrapper.find('.post-image')
    expect(img.exists()).toBe(true)
    expect(img.attributes('src')).toBe(mockPost.imageUrl)

    // 验证发帖时间和作者信息
    expect(wrapper.find('.poster').text()).toBe(`发帖人：${mockPost.poster}`)
    const formattedTime = new Date(mockPost.postTime).toLocaleString()
    expect(wrapper.find('.post-time').text()).toBe(`发布时间：${formattedTime}`)
  })

  afterEach(() => {
    jest.clearAllMocks()
  })
})