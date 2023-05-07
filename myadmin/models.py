from datetime import datetime

from django.db import models


# Create your models here.
# 员工账号信息模型
class Admin(models.Model):
    username = models.CharField(max_length=50)  # 员工账号
    nickname = models.CharField(max_length=50)  # 昵称
    password_hash = models.CharField(max_length=100)  # 密码
    password_salt = models.CharField(max_length=50)  # 密码干扰值
    status = models.IntegerField(default=1)  # 状态:1正常/2禁用/6管理员/9删除
    time = models.DateTimeField(default=datetime.now)  # 修改时间

    def toDict(self):
        return {'id': self.id, 'username': self.username, 'nickname': self.nickname,
                'password_hash': self.password_hash, 'password_salt': self.password_salt, 'status': self.status,
                'time': self.time.strftime('%Y-%m-%d %H:%M')}

    class Meta:
        db_table = "admin"  # 更改表名


# 店铺信息模型
class Shop(models.Model):
    name = models.CharField(max_length=255)  # 店铺名称
    cover_pic = models.CharField(max_length=255)  # 封面图片
    address = models.CharField(max_length=255)  # 店铺地址
    phone = models.CharField(max_length=255)  # 联系电话
    status = models.IntegerField(default=1)  # 状态:1正常/2暂停/9删除
    comments = models.IntegerField()  # 评论数
    grade = models.FloatField()  # 评分
    price = models.CharField(max_length=255)  # 人均价格
    opentime = models.CharField(max_length=255)  # 营业时间
    share_link = models.CharField(max_length=255)  # 分享链接
    keyword = models.CharField(max_length=255)  # 关键词
    area_id = models.IntegerField()  # 地区id
    category_id = models.IntegerField()  # 店铺种类
    time = models.DateTimeField(default=datetime.now)  # 修改时间

    def toDict(self):
        return {'id': self.id, 'name': self.name, 'cover_pic': self.cover_pic, 'address': self.address,
                'phone': self.phone, 'status': self.status,
                'comments': self.comments, 'grade': self.grade, 'price': self.price, 'opentime': self.opentime,
                'share_link': self.share_link,
                'keyword': self.keyword, 'area_id': self.area_id, 'category_id': self.category_id,
                'time': self.time.strftime('%Y-%m-%d %H:%M')}

    class Meta:
        db_table = "shop"  # 更改表名


class ShopPicture(models.Model):
    shop_id = models.IntegerField()
    picture_link = models.CharField(max_length=255)
    status = models.IntegerField(default=1)  # 状态:1正常/9删除
    time = models.DateTimeField(default=datetime.now)

    def toDict(self):
        return {'id': self.id, 'shop': self.shop_id, 'picture_link': self.picture_link, 'status': self.status,
                'time': self.time.strftime('%Y-%m-%d %H:%M')}

    class Meta:
        db_table = "shop_picture"


class ShopCategory(models.Model):
    name = models.CharField(max_length=50)  # 分类名称
    status = models.IntegerField(default=1)  # 状态:1正常/9删除
    time = models.DateTimeField(default=datetime.now)

    def toDict(self):
        return {'id': self.id, 'name': self.name, 'status': self.status,
                'time': self.time.strftime('%Y-%m-%d %H:%M')}

    class Meta:
        db_table = "shop_category"


class Area(models.Model):
    name = models.CharField(max_length=50)  # 分类名称
    status = models.IntegerField(default=1)  # 状态:1正常/9删除
    time = models.DateTimeField(default=datetime.now)

    def toDict(self):
        return {'id': self.id, 'name': self.name, 'status': self.status,
                'time': self.time.strftime('%Y-%m-%d %H:%M')}

    class Meta:
        db_table = "area"


# 用户信息模型
class myUser(models.Model):
    username = models.CharField(max_length=50)  # 昵称
    avatar = models.CharField(max_length=255)  # 头像
    mobile = models.CharField(max_length=50)  # 电话
    status = models.IntegerField(default=1)  # 状态:1正常/2禁用/9删除
    password_hash = models.CharField(max_length=100)  # 密码
    password_salt = models.CharField(max_length=50)  # 密码干扰值
    gender = models.IntegerField(default=0)  # 状态:0位置/1男/2女
    introduction = models.CharField(max_length=255)  # 个人介绍
    area_id = models.IntegerField()  # 地区id
    token = models.CharField(max_length=1000)
    time = models.DateTimeField(default=datetime.now)  # 修改时间

    def toDict(self):
        return {'id': self.id, 'username': self.username, 'avatar': self.avatar, 'mobile': self.mobile,
                'status': self.status,
                'password_hash': self.password_hash, 'password_salt': self.password_salt, 'gender': self.gender,
                'introduction': self.introduction, 'area_id': self.area_id, 'token': self.token,
                'time': self.time.strftime('%Y-%m-%d %H:%M')}

    class Meta:
        db_table = "user"  # 更改表名


class UserFavourite(models.Model):
    shop_id = models.IntegerField()  # 店铺id
    user_id = models.IntegerField()
    status = models.IntegerField(default=1)  # 状态:1正常/2禁用/9删除

    def toDict(self):
        return {'id': self.id, 'shop_id': self.shop_id, 'user_id': self.user_id, 'status': self.status}

    class Meta:
        db_table = "user_favourite"


class UserComment(models.Model):
    shop_id = models.IntegerField()  # 店铺id
    user_id = models.IntegerField()
    content = models.CharField(max_length=2550)
    grade = models.FloatField()  # 评分
    time = models.DateTimeField(default=datetime.now)  # 修改时间
    keyword = models.CharField(max_length=255)  # 关键词
    status = models.IntegerField(default=1)  # 状态:1正常/2禁用/9删除

    def toDict(self):
        return {'id': self.id, 'shop_id': self.shop_id, 'user_id': self.user_id, 'content': self.content,
                'grade': self.grade, 'status': self.status, 'keyword': self.keyword,
                'time': self.time.strftime('%Y-%m-%d %H:%M')}

    class Meta:
        db_table = "user_comment"  # 更改表名


class CommentPicture(models.Model):
    comment_id = models.IntegerField()
    picture_link = models.CharField(max_length=255)
    status = models.IntegerField(default=1)  # 状态:1正常/9删除
    time = models.DateTimeField(default=datetime.now)

    def toDict(self):
        return {'id': self.id, 'comment_id': self.comment_id, 'picture_link': self.picture_link, 'status': self.status,
                'time': self.time.strftime('%Y-%m-%d %H:%M')}

    class Meta:
        db_table = "comment_picture"


class Group(models.Model):
    name = models.CharField(max_length=255)
    shop_id = models.IntegerField()  # 店铺id
    leader_id = models.IntegerField()
    share_link = models.CharField(max_length=255)  # 分享链接
    time = models.DateTimeField(default=datetime.now)  # 修改时间
    status = models.IntegerField(default=1)  # 状态:1正常/2禁用/9删除
    reserve_at = models.DateTimeField()

    def toDict(self):
        return {'id': self.id, 'name': self.name, 'shop_id': self.shop_id, 'leader_id': self.leader_id,
                'share_link': self.share_link,
                'time': self.time.strftime('%Y-%m-%d %H:%M'), 'status': self.status,
                'reserve_at': self.reserve_at.strftime('%Y-%m-%d %H:%M')}

    class Meta:
        db_table = "group"  # 更改表名


class GroupMember(models.Model):
    user_id = models.IntegerField()
    group_id = models.IntegerField()
    access = models.IntegerField(default=1)  # 状态：2:组长 1:成员
    location = models.CharField(max_length=255)
    time = models.DateTimeField(default=datetime.now)  # 修改时间
    status = models.IntegerField(default=1)  # 状态:1正常/2禁用/9删除

    def toDict(self):
        return {'id': self.id, 'user_id': self.user_id, 'group_id': self.group_id, 'access': self.access,
                'location': self.location, 'time': self.time.strftime('%Y-%m-%d %H:%M'), 'status': self.status, }

    class Meta:
        db_table = "group_member"  # 更改表名


class Notice(models.Model):
    admin_id = models.IntegerField()
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    time = models.DateTimeField(default=datetime.now)  # 修改时间
    status = models.IntegerField(default=1)  # 状态:1正常/2禁用/9删除

    def toDict(self):
        return {'id': self.id, 'admin_id': self.admin_id, 'title': self.title, 'content': self.content,
                'time': self.time.strftime('%Y-%m-%d %H:%M'), 'status': self.status, }

    class Meta:
        db_table = "notice"  # 更改表名


class UserPreference(models.Model):
    user_id = models.IntegerField()
    category_id = models.IntegerField()
    status = models.IntegerField(default=1)  # 状态:1正常/2禁用/9删除

    def toDict(self):
        return {'id': self.id, 'user_id': self.user_id, 'category_id': self.category_id, 'status': self.status, }

    class Meta:
        db_table = "user_preference"  # 更改表名


class UserBehavior(models.Model):
    user_id = models.IntegerField()
    shop_id = models.IntegerField()
    behavior = models.IntegerField()
    status = models.IntegerField(default=1)  # 状态:1正常/2禁用/9删除

    def toDict(self):
        return {'id': self.id, 'user_id': self.user_id, 'shop_id': self.shop_id, 'behavior': self.behavior,
                'status': self.status, }

    class Meta:
        db_table = "user_behavior"  # 更改表名
