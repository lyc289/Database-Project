### RESTful API 设计

### 1. 用户信息（users）

#### 1.1 注册用户
- **URL**: `POST /users`
- **描述**: 创建新用户。
- **请求体**:
  ```json
  {
    "username": "string",
    "password": "string",
    "email": "string"
  }
  ```
- **响应**:
  ```json
  {
    "user_id": "int",
    "username": "string",
    "email": "string",
    "create_date": "date"
  }
  ```

#### 1.2 获取用户信息
- **URL**: `GET /users/{user_id}`
- **描述**: 根据用户 ID 获取用户信息。
- **响应**:
  ```json
  {
    "user_id": "int",
    "username": "string",
    "email": "string",
    "create_date": "date"
  }
  ```

#### 1.3 删除用户
- **URL**: `DELETE /users/{user_id}`
- **描述**: 删除用户。
- **响应**:
  ```json
  {
    "message": "User deleted successfully"
  }
  ```

---

### 2. 个人页面（user_info）

#### 2.1 更新个人页面
- **URL**: `PUT /user_info/{user_id}`
- **描述**: 更新用户个人页面。
- **请求体**:
  ```json
  {
    "nickname": "string",
    "avatar": "string",
    "intro": "string"
  }
  ```
- **响应**:
  ```json
  {
    "user_id": "int",
    "nickname": "string",
    "avatar": "string",
    "intro": "string",
    "update_date": "date"
  }
  ```

#### 2.2 获取个人页面
- **URL**: `GET /user_info/{user_id}`
- **描述**: 获取用户的个人页面信息。
- **响应**:
  ```json
  {
    "user_id": "int",
    "nickname": "string",
    "avatar": "string",
    "intro": "string",
    "update_date": "date"
  }
  ```

---

### 3. 提问（questions）

#### 3.1 创建提问
- **URL**: `POST /questions`
- **描述**: 用户创建新的提问。
- **请求体**:
  ```json
  {
    "asker_id": "int",
    "title": "string",
    "content": "string"
  }
  ```
- **响应**:
  ```json
  {
    "id": "int",
    "asker_id": "int",
    "title": "string",
    "content": "string",
    "create_date": "date"
  }
  ```

#### 3.2 获取所有问题
- **URL**: `GET /questions`
- **描述**: 获取所有提问列表。
- **响应**:
  ```json
  [
    {
      "id": "int",
      "asker_id": "int",
      "title": "string",
      "content": "string",
      "create_date": "date"
    }
  ]
  ```

#### 3.3 获取单个问题
- **URL**: `GET /questions/{id}`
- **描述**: 获取指定提问的详细信息。
- **响应**:
  ```json
  {
    "id": "int",
    "asker_id": "int",
    "title": "string",
    "content": "string",
    "create_date": "date",
    "update_date": "date"
  }
  ```

---

### 4. 回答（answers）

#### 4.1 提交回答
- **URL**: `POST /answers`
- **描述**: 为某个提问添加回答。
- **请求体**:
  ```json
  {
    "answerer_id": "int",
    "question_id": "int",
    "content": "string"
  }
  ```
- **响应**:
  ```json
  {
    "id": "int",
    "answerer_id": "int",
    "question_id": "int",
    "content": "string",
    "create_date": "date"
  }
  ```

#### 4.2 获取问题的所有回答
- **URL**: `GET /questions/{question_id}/answers`
- **描述**: 获取某个问题下的所有回答。
- **响应**:
  ```json
  [
    {
      "id": "int",
      "answerer_id": "int",
      "content": "string",
      "create_date": "date"
    }
  ]
  ```

---

### 5. 评论（comments）

#### 5.1 添加评论
- **URL**: `POST /comments`
- **描述**: 添加评论。
- **请求体**:
  ```json
  {
    "user_id": "int",
    "answer_id": "int",
    "content": "string"
  }
  ```
- **响应**:
  ```json
  {
    "id": "int",
    "user_id": "int",
    "answer_id": "int",
    "content": "string",
    "create_date": "date"
  }
  ```

#### 5.2 获取回答的所有评论
- **URL**: `GET /answers/{answer_id}/comments`
- **描述**: 获取某个回答下的所有评论。
- **响应**:
  ```json
  [
    {
      "id": "int",
      "user_id": "int",
      "content": "string",
      "create_date": "date"
    }
  ]
  ```

---

### 6. 点赞（agree）

#### 6.1 点赞回答
- **URL**: `POST /agree`
- **描述**: 用户点赞回答。
- **请求体**:
  ```json
  {
    "user_id": "int",
    "answer_id": "int"
  }
  ```
- **响应**:
  ```json
  {
    "message": "Agree added successfully"
  }
  ```

#### 6.2 获取回答的点赞数
- **URL**: `GET /answers/{answer_id}/agree_count`
- **描述**: 获取某个回答的点赞数。
- **响应**:
  ```json
  {
    "answer_id": "int",
    "agree_count": "int"
  }
  ```

---

### 7. 收藏（likes）

#### 7.1 收藏问题或回答
- **URL**: `POST /likes`
- **描述**: 用户收藏问题或回答。
- **请求体**:
  ```json
  {
    "user_id": "int",
    "question_id": "int", // 如果是问题收藏
    "answer_id": "int"    // 如果是回答收藏
  }
  ```
- **响应**:
  ```json
  {
    "message": "Like added successfully"
  }
  ```

#### 7.2 获取用户的收藏
- **URL**: `GET /users/{user_id}/likes`
- **描述**: 获取用户收藏的所有问题和回答。
- **响应**:
  ```json
  [
    {
      "question_id": "int",
      "answer_id": "int",
      "create_date": "date"
    }
  ]
  ```

---

当然可以，以下是补全的RESTful API设计，包括关注用户（follow）部分的响应和可能缺失的部分：

### 8. 关注用户（follow）

#### 8.1 关注用户
- **URL**: `POST /follow`
- **描述**: 关注其他用户。
- **请求体**:
  ```json
  {
    "follower_id": "int",
    "followee_id": "int"
  }
  ```
- **响应**:
  ```json
  {
    "message": "User followed successfully",
    "follower_id": "int",
    "followee_id": "int"
  }
  ```

#### 8.2 获取用户的关注列表
- **URL**: `GET /users/{user_id}/follows`
- **描述**: 获取用户关注的所有用户列表。
- **响应**:
  ```json
  [
    {
      "followee_id": "int",
      "create_date": "date"
    }
  ]
  ```

#### 8.3 获取用户的粉丝列表
- **URL**: `GET /users/{user_id}/followers`
- **描述**: 获取关注该用户的所有用户列表。
- **响应**:
  ```json
  [
    {
      "follower_id": "int",
      "create_date": "date"
    }
  ]
  ```

#### 8.4 取消关注用户
- **URL**: `DELETE /follow`
- **描述**: 取消关注其他用户。
- **请求体**:
  ```json
  {
    "follower_id": "int",
    "followee_id": "int"
  }
  ```
- **响应**:
  ```json
  {
    "message": "User unfollowed successfully",
    "follower_id": "int",
    "followee_id": "int"
  }
  ```

#### 8.5 检查是否关注
- **URL**: `GET /users/{follower_id}/follows/{followee_id}`
- **描述**: 检查用户是否关注了另一个用户。
- **响应**:
  ```json
  {
    "is_following": "boolean"
  }
  ```

