
INSTALLED_APPS = [
    'rest_framework',
    'api',
    'corsheaders',
]
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_ALLOWED_ORIGINS = True

# 允许特定源访问你的API接口
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8081",
]

# 如果同时处理 CSRF 保护，请设置 trusted origins
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8081",
]


CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
