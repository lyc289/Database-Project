from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
class HelloWorld(APIView):
    def get(self, request):
        return Response({"message": "Hello, world!"}, status=status.HTTP_200_OK)

from rest_framework import viewsets
from .models import User, UserInfo, Question, Answer, Comment, LoginLog, Like, Agree, Follow
from .serializers import UserSerializer, UserInfoSerializer, QuestionSerializer, AnswerSerializer, CommentSerializer, LoginLogSerializer, LikeSerializer, AgreeSerializer, FollowSerializer
from .serializers import FollowerSerializer, PostHistorySerializer, CollectionSerializer
import hashlib
from .utils import DataPack, KnowledgeBasedQA 
from rest_framework.parsers import MultiPartParser, FormParser

import os

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_queryset(self):
        # 仅返回当前登录用户的记录
        return User.objects.filter(user_id=self.request.user.user_id)
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            # 如果是查看用户信息操作，不可查询密码字段
            class UserRetrieveSerializer(UserSerializer):
                class Meta(UserSerializer.Meta):
                    fields = ('user_id', 'username', 'email', 'create_date')  # 不包括密码字段
            return UserRetrieveSerializer
        return self.serializer_class

class QuestionView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = QuestionSerializer
    def get(self, request, question_id=None):
        """根据 question_id 获取特定问题，或获取问题列表"""
        if question_id:
            # 获取特定问题
            try:
                question = Question.objects.get(pk=question_id)
            except Question.DoesNotExist:
                return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = QuestionSerializer(question)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # 获取问题列表
            questions = Question.objects.all()
            serializer = QuestionSerializer(questions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """新增一个问题"""
        # 获取请求数据
        title = request.data.get('title')
        content = request.data.get('content')
        images = request.FILES.get('photo')  # 获取文件
        asker = User.objects.get(username=request.data.get('asker')) # 当前用户（通过 JWT 或 Session 认证获取）
        print(title, content, images, asker)
        # 验证字段是否有效
        if not title or not content:
            return Response({"error": "Title and content are required."}, status=status.HTTP_400_BAD_REQUEST)

        # 创建 Question 对象
        question = Question(
            title=title,
            content=content,
            asker=asker,  # 自动设置当前登录用户
            images=images  # 如果有上传文件
        )

        # 保存到数据库
        question.save()
        # 返回成功响应
        return Response({
            "id": question.id,
            "title": question.title,
            "content": question.content,
            "asker": question.asker.username,
            "images": question.images.url if question.images else None,
        }, status=status.HTTP_201_CREATED)
    

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    def get_queryset(self):
        question_id = self.request.query_params.get('question', None)
        if question_id:
            return Comment.objects.filter(question_id=question_id, parent__isnull=True).order_by('-create_date')
        return Comment.objects.filter(parent__isnull=True).order_by('-create_date')

    def perform_create(self, serializer):
        username = self.request.data.get('username')
        question_id = self.request.data.get('question')
        parent_id = self.request.data.get('parent', None)
        
        try:
            user = User.objects.get(username=username)
            question = Question.objects.get(id=question_id)
            parent_comment = None
            if parent_id:
                parent_comment = Comment.objects.get(id=parent_id)
            
            serializer.save(
                commenter=user,
                question=question,
                parent=parent_comment,
                content=self.request.data.get('content')
            )
        except User.DoesNotExist:
            raise serializers.ValidationError({"error": "用户不存在"})
        except Question.DoesNotExist:
            raise serializers.ValidationError({"error": "问题不存在"})
        except Comment.DoesNotExist:
            raise serializers.ValidationError({"error": "父评论不存在"})
        
class UserInfoViewSet(APIView):
    def get(self, request):
        # 验证请求参数
        username = request.query_params.get('username')
        if not username:
            return Response({'error': 'Username parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 获取用户及关联信息
            user = User.objects.get(username=username)
            user_info = UserInfo.objects.get(user=user)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        except UserInfo.DoesNotExist:
            return Response({'error': 'UserInfo not found.'}, status=status.HTTP_404_NOT_FOUND)

        # 获取关注列表
        followers = Follow.objects.filter(follower=user_info).select_related('followee')
        followerList = [
            {
                'id': follow.follower.id,
                'user_name': follow.followee.user.username,
                'nickname': follow.followee.nickname,
                'intro': follow.followee.intro or '这是一个个性签名的默认值',
            }
            for follow in followers
        ]
        print(followerList)
        # 获取发布历史
        questions = Question.objects.filter(asker=user)
        postHistory = [
            {
                'id': question.id,
                'title': question.title,
                'createTime': question.create_date,
            }
            for question in questions
        ]

        # 获取收藏列表
        likes = Like.objects.filter(user=user).select_related('question', 'answer')
        for i in likes:
            print (i.question.create_date)
        collectionList = [
            {
                'id': like.question.id,
                # 'answer': like.answer.content if like.answer else None,
                'question': like.question.title if like.question else None,
                'createTime': like.question.create_date,
            }
            for like in likes
        ]

        # 构造响应数据
        response_data = {
            'user_info': {
                'id': user_info.id,
                'nickname': user_info.nickname or 'momo',
                'intro': user_info.intro or '这是一个个性签名的默认值',
            },
            'followerList': followerList,
            'postHistory': postHistory,
            'collectionList': collectionList,
        }
        print(response_data)

        # 返回响应
        return Response(response_data, status=status.HTTP_200_OK)


class LoginLogViewSet(viewsets.ModelViewSet):
    queryset = LoginLog.objects.all()
    serializer_class = LoginLogSerializer

class LikeViewSet(APIView):
    def get(self, request):
        # 验证请求参数
        username = request.query_params.get('username')
        print (username)
        post_id=request.query_params.get('post_id')
        print(type(post_id))
        t=int(post_id)
        user=User.objects.get(username=username)
        question=Question.objects.get(id=t)
        print(user)
        print(question)
        likes=Like.objects.filter(user=user,question=question)
        print(likes)
        if likes:
            return Response({'like': 1}, status=status.HTTP_200_OK)
        else:
            return Response({'like': 0}, status=status.HTTP_200_OK)
    def post(self,request):
        username = request.data.get('username')
        post_id = request.data.get('question')
        user = User.objects.get(username=username)
        t=int(post_id)
        question = Question.objects.get(id=t)
        like = Like.objects.create(user=user, question=question)
        print(like)
        return Response({'message': '点赞成功'}, status=status.HTTP_201_CREATED)
    def delete(self,request):
        username = request.data.get('username')
        post_id = request.data.get('question')
        user = User.objects.get(username=username)
        t=int(post_id)
        question = Question.objects.get(id=t)
        like = Like.objects.get(user=user, question=question)
        like.delete()
        return Response({'message': '取消点赞成功'}, status=status.HTTP_200_OK)
    
class AgreeViewSet(viewsets.ModelViewSet):
    queryset = Agree.objects.all()
    serializer_class = AgreeSerializer

class FollowViewSet(APIView):
    def get(self, request):
        follower_username = request.query_params.get('follower')
        print('test follower_username: ',follower_username)
        followee_username = request.query_params.get('followee')
        print('test followee_username: ',followee_username)
        followee_user = User.objects.get(username=followee_username)
        followee_userinfo = UserInfo.objects.get(user=followee_user)
        follower_user = User.objects.get(username=follower_username)
        follower_userinfo = UserInfo.objects.get(user=follower_user)
        if Follow.objects.filter(follower=follower_userinfo, followee=followee_userinfo).exists():
            print("follower_username",follower_username,"followee_username",followee_username,"following")
            return Response({'follow': 1}, status=status.HTTP_200_OK)
        else:
            print("follower_username",follower_username,"followee_username",followee_username,"not following")
            return Response({'follow': 0}, status=status.HTTP_200_OK)
    def post(self, request):
        follower_username = request.data.get('follower')
        followee_username = request.data.get('followee')
        followee_user = User.objects.get(username=followee_username)
        followee_userinfo = UserInfo.objects.get(user=followee_user)
        follower_user = User.objects.get(username=follower_username)
        follower_userinfo = UserInfo.objects.get(user=follower_user)
        Follow.objects.create(follower=follower_userinfo, followee=followee_userinfo)
        return Response({"message": f"已成功关注 {followee_username}"}, status=status.HTTP_201_CREATED)
    def delete(self,request):
        follower_username = request.data.get('follower')
        followee_username = request.data.get('followee')
        followee_user = User.objects.get(username=followee_username)
        followee_userinfo = UserInfo.objects.get(user=followee_user)
        follower_user = User.objects.get(username=follower_username)
        follower_userinfo = UserInfo.objects.get(user=follower_user)
        # 查询并删除所有满足条件的 Follow 记录
        deleted_count, _ = Follow.objects.filter(
            follower=follower_userinfo, 
            followee=followee_userinfo
        ).delete()
        print('delete num: ',deleted_count)
        return Response({'message': '取消关注成功'}, status=status.HTTP_200_OK)
    
class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        nickname = request.data.get('nickname')
        
        # 检查用户名是否已存在
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 检查邮箱是否已存在
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
        # 计算密码哈希
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        
        # 创建新用户
        user = User.objects.create(
            user_id=User.objects.count() + 1,
            username=username,
            hashed_password=hashed_password,
            email=email,
        )
        UserInfo.objects.create(user=user, nickname=nickname)
        
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print("username", username)
        print("get POST REQUEST")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # �����证密码
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        if user.hashed_password != hashed_password:
            return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)

        # 记录登录日志
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        LoginLog.objects.create(user=user, ip=ip)
        
        return Response({
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'is_superuser': user.is_superuser  # 是否是管理员
        })

class EditProfileView(APIView):
    def post(self, request):
        try:
            nickname = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            current_username = request.data.get('current_username')
            intro=request.data.get('intro')
            user = User.objects.get(username=current_username)
            # 更新用户信息
            if email:
                # 检查邮箱是否被其他用户使用
                if User.objects.filter(email=email).exclude(username=user.username).exists():
                    return Response({'error': '该邮箱已被使用'}, status=status.HTTP_400_BAD_REQUEST)
                user.email = email

            if password:
                user.hashed_password = hashlib.md5(password.encode()).hexdigest()
            if intro:
                user_info, created = UserInfo.objects.get_or_create(user=user)
                user_info.intro = intro
                user_info.save()
            if nickname:
                user_info, created = UserInfo.objects.get_or_create(user=user)
                user_info.nickname = nickname
                user_info.save()
            user.save()
            
            # 处理头像上传
            if 'avatar' in request.FILES:
                user_info, created = UserInfo.objects.get_or_create(user=user)
                user_info.avatar = request.FILES['avatar']
                user_info.save()
                print("avatar success")
            return Response({'message': '更新成功'}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AIResponseView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 初始化KnowledgeBasedQA实例
        self.qa_system = KnowledgeBasedQA()
    
    def post(self, request):
        try:
            question = request.data.get('question')
            print(question)
            if not question:
                return Response(
                    {"error": "Question is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 使用KnowledgeBasedQA处理问题
            answer = self.qa_system.get_response(question)
            
            # 构造响应
            response_data = {
                "question": question,
                "answer": answer,
                "success": True
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": str(e), "success": False}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get(self, request):
        """可选:获取系统信息或统计数据"""
        try:
            stats = self.qa_system.get_stats()  # 获取系统统计信息
            return Response(stats, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

