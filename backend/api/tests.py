from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import User, LoginLog
import hashlib

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.test_user_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'test@example.com',
        }

    def test_user_registration(self):
        # 测试成功注册
        response = self.client.post(self.register_url, self.test_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())

        # 测试重复用户名注册
        response = self.client.post(self.register_url, self.test_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login(self):
        # 先创建用户
        self.client.post(self.register_url, self.test_user_data)

        # 测试成功登录
        login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user_id', response.data)
        
        # 验证登录日志是否创建
        self.assertTrue(LoginLog.objects.filter(user__username='testuser').exists())

    def test_login_wrong_password(self):
        # 先创建用户
        self.client.post(self.register_url, self.test_user_data)

        # 测试错误密码
        wrong_login_data = {
            'username': 'testuser',
            'password': 'wrongpass'
        }
        response = self.client.post(self.login_url, wrong_login_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_nonexistent_user(self):
        # 测试不存在的用户
        login_data = {
            'username': 'nonexistent',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

from django.test import TestCase
from django.utils import timezone
from .models import User, Question
from django.core.files.uploadedfile import SimpleUploadedFile


class QuestionModelTest(TestCase):

    def setUp(self):
        """创建一个用户并准备一些测试数据"""
        # 创建用户
        self.user = User.objects.create(
            user_id=1,
            username="testuser",
            email="testuser@example.com",
            hashed_password="hashedpassword"
        )

        # 创建一个带有图片的示例问题
        self.image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        self.question = Question.objects.create(
            asker=self.user,
            title="What is Django?",
            content="Django is a web framework.",
            images=self.image,
            is_deleted=False
        )

    def test_question_creation(self):
        """测试问题是否能正确创建"""
        question = Question.objects.get(id=self.question.id)
        self.assertEqual(question.title, "What is Django?")
        self.assertEqual(question.content, "Django is a web framework.")
        self.assertEqual(question.asker, self.user)
        self.assertFalse(question.is_deleted)

    def test_question_image_upload(self):
        """测试问题图片是否上传并且能被访问"""
        question = Question.objects.get(id=self.question.id)
        self.assertTrue(question.images.name.startswith('images/'))
        self.assertEqual(question.images.name.split('/')[0], 'images')

    def test_question_update(self):
        """测试问题内容的更新"""
        question = Question.objects.get(id=self.question.id)
        question.title = "Updated title"
        question.content = "Updated content"
        question.save()

        updated_question = Question.objects.get(id=self.question.id)
        self.assertEqual(updated_question.title, "Updated title")
        self.assertEqual(updated_question.content, "Updated content")

    def test_question_soft_delete(self):
        """测试问题的软删除"""
        question = Question.objects.get(id=self.question.id)
        question.is_deleted = True
        question.delete_date = timezone.now().date()
        question.save()

        deleted_question = Question.objects.get(id=self.question.id)
        self.assertTrue(deleted_question.is_deleted)
        self.assertIsNotNone(deleted_question.delete_date)

    def test_question_delete(self):
        """测试物理删除问题"""
        question = Question.objects.get(id=self.question.id)
        question.delete()

        with self.assertRaises(Question.DoesNotExist):
            Question.objects.get(id=self.question.id)

    # def test_question_create_without_image(self):
    #     """测试没有图片的情况"""
    #     question_without_image = Question.objects.create(
    #         asker=self.user,
    #         title="What is Python?",
    #         content="Python is a programming language.",
    #         images=None,
    #         is_deleted=False
    #     )
    #     self.assertIsNone(question_without_image.images)

    def test_question_create_with_deleted_flag(self):
        """测试问题创建时默认未删除标志"""
        question = Question.objects.create(
            asker=self.user,
            title="What is Django REST Framework?",
            content="Django REST Framework is a powerful toolkit.",
            images=None,
            is_deleted=False
        )
        self.assertFalse(question.is_deleted)
    # 测试直接返回所有问题的情况
    def test_get_all_questions(self):
        response = self.client.get(reverse('questions'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)