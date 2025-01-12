## tables

**entities**

* 用户信息 users
* 个人页面 user_info
* 提问 questions
* 回答 answers
* 评论 comments
* 登录日志 login_logs

#### 用户信息表

```sql
create table users(
	user_id primary key bigint,
    username varchar(20),
    hashed_password() varchar(128),
    email varchar(40),
    create_date DATE,
    is_deleted BOOL,
    is_administrator BOOL
);
```

#### 个人页面

```sql
create table user_info(
	user_id,
    nickname,
    avatar,
    intro,
    update_date DATE,
    is_deleted BOOL,
    foreign key (user_id) references users(user_id)
);
```

#### 提问

```sql
create table questions(
	id primary key,
	asker_id,
	title VARCHAR(20),
	content,
	create_date DATE,
    update_date DATE,
    is_deleted BOOL,
    delete_date DATE,
    foreign key (asker_id) references users(user_id)
);
```

#### 回答

```sql
create table answers(
	id,
    answerer_id,
    question_id,
    content,
    create_date DATE,
    update_date DATE,
    is_deleted BOOL,
    delete_date DATE,
    foreign key (answerer_id) references users(user_id),
    foreign key (question_id) references questions(id)
);
```

#### 评论

```sql
create table comments(
	id,
    answer_id,
    user_id,
    content,
    create_date DATE,
    is_deleted BOOL,
    foreign key (question_id) references questions(id),
    foreign key (user_id) references users(user_id)
);
```

#### 日志

```sql
create table login_logs(
	id,
    user_id,
    ip,
    login_date DATE,
    foreign key (user_id) references users(user_id)
)
```



#### 收藏

```sql
create table likes(
	question_id,
    answer_id,
    user_id,
    foreign key (user_id) references users(user_id),
    foreign key (question_id) references questions(id)
)
```

#### 点赞

```sql
create tabel agree(
	answer_id,
    user_id,
    foreign key (question_id) references questions(id),
    foreign key (user_id) references users(user_id)
);
```

#### 关注用户

```sql
create table follow(
	follower_id,//关注者
    followee_id,//被关注者
    foreign key (follower_id) references users(user_id),
    foreign key (followee_id) references users(user_id)
);
```

