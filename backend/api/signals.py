from django.db.models.signals import post_migrate
from django.dispatch import receiver
from api.models import User  # 引入自定义 User 模型

@receiver(post_migrate)
def create_initial_users(sender, **kwargs):
    # 创建第一个用户
    if not User.objects.filter(username='admin').exists():
        User.objects.create(
            username='admin',
            hashed_password='fae0b27c451c728867a567e8c1bb4e53',  # 对应明文666
            email='admin@ruc.edu.com',
            is_superuser=True,
            is_deleted=False
        )
    # 创建第二个用户
    if not User.objects.filter(username='admin1').exists():
        User.objects.create(
            username='admin1',
            hashed_password='fae0b27c451c728867a567e8c1bb4e53',  
            email='admin1@ruc.edu.com',
            is_superuser=True,
            is_deleted=False
        )
    # 创建第三个用户
    if not User.objects.filter(username='admin2').exists():
        User.objects.create(
            username='admin2',
            hashed_password='fae0b27c451c728867a567e8c1bb4e53',  
            email='admin2@ruc.edu.com',
            is_superuser=True,
            is_deleted=False
        )
