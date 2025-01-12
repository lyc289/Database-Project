from rest_framework import serializers
from .models import User, UserInfo, Question, Answer, Comment, LoginLog, Like, Agree, Follow

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'create_date']

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    asker = serializers.CharField(source='asker.username', read_only=True)
    nickname = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = '__all__'
        
    def get_nickname(self, obj):  # 修改方法名为 get_nickname
        # 确保 userinfo 存在并且 nickname 不为 null，否则返回 'momo'
        userinfo = getattr(obj.asker, 'userinfo', None)
        if userinfo and userinfo.nickname:
            return userinfo.nickname
        return 'momo'

   
        
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    commenter_name = serializers.CharField(source='commenter.username', read_only=True)
    nickname = serializers.SerializerMethodField()  # 添加 nickname 字段

    class Meta:
        model = Comment
        fields = ['id', 'question', 'content', 'commenter_name', 'nickname', 'parent', 'create_date', 'replies']
        read_only_fields = ['commenter_name', 'nickname', 'create_date']

    def get_replies(self, obj):
        replies = Comment.objects.filter(parent=obj).order_by('-create_date')
        return CommentSerializer(replies, many=True).data

    def get_nickname(self, obj):  # 修改方法名为 get_nickname
        # 确保 userinfo 存在并且 nickname 不为 null，否则返回 'momo'
        userinfo = getattr(obj.commenter, 'userinfo', None)
        if userinfo and userinfo.nickname:
            return userinfo.nickname
        return 'momo'

class LoginLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginLog
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class AgreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agree
        fields = '__all__'

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'
        
class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['id', 'nickname', 'intro']
        
class PostHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'create_date']
        
class CollectionSerializer(serializers.ModelSerializer):
    question = serializers.CharField(source='question.title', read_only=True)
    answer = serializers.CharField(source='answer.content', read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'question', 'answer']