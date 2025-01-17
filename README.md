# DB-Course
数据库系统概论大作业repo
## 部署
### 环境
- python3
- nodejs
- npm
- vue-cli
- django
- django-cors-headers
- django-rest-framework
- dashscope (api)
### backend
```shell
cd backend
python manage.py migrate
python manage.py runserver
```
### frontend
```shell
cd frontend
npm install
npm run serve
```

默认后端监听8000端口，前端监听8080端口，请根据需要修改