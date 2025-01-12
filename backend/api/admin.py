from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import Group, Permission
from .models import Question, Answer, User

# 相对普通用户, 管理员仅增加了'删除任意用户的帖子'的功能 
# (即普通用户只能删除自己的帖子, 管理员能删除任意帖子.其他权限没有区别)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'email', 'create_date', 'is_deleted')
    search_fields = ('username', 'email')
    list_filter = ('is_deleted',)

admin.site.register(User, UserAdmin)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'asker', 'title', 'create_date', 'is_deleted')
    search_fields = ('title',)
    list_filter = ('is_deleted',)
    
    def delete_model(self, request, obj):
        """ 只有管理员可以删除任意帖子，普通用户只能删除自己的帖子 """
        if request.user.is_superuser:
            # 管理员可以删除任何帖子
            obj.delete()
        elif obj.asker == request.user:
            # 普通用户只能删除自己提问的帖子
            obj.delete()
        else:
            raise PermissionError("You do not have permission to delete this post.")

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'answerer', 'question', 'create_date', 'is_deleted')
    search_fields = ('question__title',)
    list_filter = ('is_deleted',)
    
    def delete_model(self, request, obj):
        """ 只有管理员可以删除任意回答，普通用户只能删除自己的回答 """
        if request.user.is_superuser:
            # 管理员可以删除任何回答
            obj.delete()
        elif obj.answerer == request.user:
            # 普通用户只能删除自己的回答
            obj.delete()
        else:
            raise PermissionError("You do not have permission to delete this answer.")

    def get_queryset(self, request):
        """ 管理员看到所有回答，普通用户只看到自己的回答 """
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(answerer=request.user)
        return queryset

# 注册 Question 和 Answer 模型
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
