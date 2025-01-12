from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    hashed_password = models.CharField(max_length=40)
    email = models.EmailField(max_length=40, unique=True)
    create_date = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    def __str__(self):
        return self.username

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50,null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    intro = models.TextField(blank=True, null=True)
    update_date = models.DateField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.nickname
class Question(models.Model):
    asker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=100)
    content = models.TextField()
    images = models.ImageField(upload_to='question/images/', blank=True, null=True)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    delete_date = models.DateField(null=True, blank=True)
    comment_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Answer(models.Model):
    answerer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    delete_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Answer to {self.question.title}"

class Comment(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    commenter = models.ForeignKey('User', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-create_date']

    def __str__(self):
        return f"Comment by {self.commenter.username} on {self.question.title}"
class LoginLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()
    login_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Login by {self.user.username} from {self.ip} on {self.login_date}"

# 收藏
class Like(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Like by {self.user.username} on {'question' if self.question else 'answer'}"
    
# 点赞
class Agree(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Agree by {self.user.username} on answer {self.answer.id}"
    
class Follow(models.Model):
    follower = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='following')
    followee = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return f"{self.follower.username} follows {self.followee.username}"
