from django.urls import path, include
from .views import HelloWorld
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, QuestionView, AnswerViewSet, CommentViewSet, UserInfoViewSet, LoginLogViewSet, LikeViewSet, AgreeViewSet, FollowViewSet
from .views import RegisterView, LoginView, AIResponseView, EditProfileView
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'answers', AnswerViewSet)
router.register(r'comments', CommentViewSet, basename='comments')
router.register(r'loginlogs', LoginLogViewSet)
# router.register(r'likes', LikeViewSet)
router.register(r'agrees', AgreeViewSet)

urlpatterns = [
    path('hello/', HelloWorld.as_view(), name='hello_world'),
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('ai-response/', AIResponseView.as_view(), name='ai-response'),
    path('questions/', QuestionView.as_view(), name='questions'),
    path('questions/<int:question_id>/', QuestionView.as_view(), name='question-detail'),
    path('edit-profile/', EditProfileView.as_view(), name='edit-profile'),
    path('userinfos/', UserInfoViewSet.as_view(), name='userinfos'),
    path('userinfos/<str:username>/', UserInfoViewSet.as_view(), name='userinfos_detail'),
    path('likes/', LikeViewSet.as_view(), name='likes'),
    path('follows/', FollowViewSet.as_view(), name='follows'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)