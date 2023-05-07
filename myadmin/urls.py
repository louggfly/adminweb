# 后台管理子路由文件
from django.urls import path

from myadmin.views import admin
from myadmin.views import area
from myadmin.views import index, shopPicture, commentPicture, groupMember, group, notice
from myadmin.views import shop, shopCategory
from myadmin.views import user, userComment, userFavourite, userBehavior, userPreference

urlpatterns = [
    path('', index.index, name="myadmin_index"),

    path('login', index.login, name="myadmin_login"),
    path('dologin', index.dologin, name="myadmin_dologin"),
    path('logout', index.logout, name="myadmin_logout"),
    path('verify', index.verify, name="myadmin_verify"),

    path('admin/<int:pIndex>', admin.index, name="myadmin_admin_index"),
    path('admin/add', admin.add, name="myadmin_admin_add"),
    path('admin/insert', admin.insert, name="myadmin_admin_insert"),
    path('admin/del/<int:uid>', admin.delete, name="myadmin_admin_delete"),
    path('admin/edit/<int:uid>', admin.edit, name="myadmin_admin_edit"),
    path('admin/update/<int:uid>', admin.update, name="myadmin_admin_update"),

    path('shop/<int:pIndex>', shop.index, name="myadmin_shop_index"),
    path('shop/add', shop.add, name="myadmin_shop_add"),
    path('shop/insert', shop.insert, name="myadmin_shop_insert"),
    path('shop/del/<int:sid>', shop.delete, name="myadmin_shop_delete"),
    path('shop/edit/<int:sid>', shop.edit, name="myadmin_shop_edit"),
    path('shop/update/<int:sid>', shop.update, name="myadmin_shop_update"),

    path('shoppicture/<int:pIndex>', shopPicture.index, name="myadmin_shoppicture_index"),
    path('shoppicture/check/<int:pid>', shopPicture.check, name="myadmin_shoppicture_check"),
    path('shoppicture/add', shopPicture.add, name="myadmin_shoppicture_add"),
    path('shoppicture/insert', shopPicture.insert, name="myadmin_shoppicture_insert"),
    path('shoppicture/del/<int:pid>', shopPicture.delete, name="myadmin_shoppicture_delete"),
    path('shoppicture/edit/<int:pid>', shopPicture.edit, name="myadmin_shoppicture_edit"),
    path('shoppicture/update/<int:pid>', shopPicture.update, name="myadmin_shoppicture_update"),

    path('shopcategory/<int:pIndex>', shopCategory.index, name="myadmin_shopcategory_index"),
    path('shopcategory/add', shopCategory.add, name="myadmin_shopcategory_add"),
    path('shopcategory/insert', shopCategory.insert, name="myadmin_shopcategory_insert"),
    path('shopcategory/del/<int:cid>', shopCategory.delete, name="myadmin_shopcategory_delete"),
    path('shopcategory/edit/<int:cid>', shopCategory.edit, name="myadmin_shopcategory_edit"),
    path('shopcategory/update/<int:cid>', shopCategory.update, name="myadmin_shopcategory_update"),

    path('area/<int:pIndex>', area.index, name="myadmin_area_index"),
    path('area/add', area.add, name="myadmin_area_add"),
    path('area/insert', area.insert, name="myadmin_area_insert"),
    path('area/del/<int:cid>', area.delete, name="myadmin_area_delete"),
    path('area/edit/<int:cid>', area.edit, name="myadmin_area_edit"),
    path('area/update/<int:cid>', area.update, name="myadmin_area_update"),

    path('user/<int:pIndex>', user.index, name="myadmin_user_index"),
    path('user/add', user.add, name="myadmin_user_add"),
    path('user/insert', user.insert, name="myadmin_user_insert"),
    path('user/del/<int:uid>', user.delete, name="myadmin_user_delete"),
    path('user/edit/<int:uid>', user.edit, name="myadmin_user_edit"),
    path('ser/update/<int:uid>', user.update, name="myadmin_user_update"),

    path('userfavourite/<int:pIndex>', userFavourite.index, name="myadmin_userfavourite_index"),
    path('userfavourite/add', userFavourite.add, name="myadmin_userfavourite_add"),
    path('userfavourite/insert', userFavourite.insert, name="myadmin_userfavourite_insert"),
    path('userfavourite/del/<int:fid>', userFavourite.delete, name="myadmin_userfavourite_delete"),
    path('userfavourite/edit/<int:fid>', userFavourite.edit, name="myadmin_userfavourite_edit"),
    path('userfavourite/update/<int:fid>', userFavourite.update, name="myadmin_userfavourite_update"),

    path('usercomment/<int:pIndex>', userComment.index, name="myadmin_usercomment_index"),
    path('usercomment/add', userComment.add, name="myadmin_usercomment_add"),
    path('usercomment/insert', userComment.insert, name="myadmin_usercomment_insert"),
    path('usercomment/del/<int:cid>', userComment.delete, name="myadmin_usercomment_delete"),
    path('usercomment/edit/<int:cid>', userComment.edit, name="myadmin_usercomment_edit"),
    path('usercomment/update/<int:cid>', userComment.update, name="myadmin_usercomment_update"),

    path('commentpicture/<int:pIndex>', commentPicture.index, name="myadmin_commentpicture_index"),
    path('commentpicture/check/<int:pid>', commentPicture.check, name="myadmin_commentpicture_check"),
    path('commentpicture/add', commentPicture.add, name="myadmin_commentpicture_add"),
    path('commentpicture/insert', commentPicture.insert, name="myadmin_commentpicture_insert"),
    path('commentpicture/del/<int:pid>', commentPicture.delete, name="myadmin_commentpicture_delete"),
    path('commentpicture/edit/<int:pid>', commentPicture.edit, name="myadmin_commentpicture_edit"),
    path('commentpicture/update/<int:pid>', commentPicture.update, name="myadmin_commentpicture_update"),

    path('group/<int:pIndex>', group.index, name="myadmin_group_index"),
    path('group/add', group.add, name="myadmin_group_add"),
    path('group/insert', group.insert, name="myadmin_group_insert"),
    path('group/del/<int:gid>', group.delete, name="myadmin_group_delete"),
    path('group/edit/<int:gid>', group.edit, name="myadmin_group_edit"),
    path('group/update/<int:gid>', group.update, name="myadmin_group_update"),

    path('groupmember/<int:pIndex>', groupMember.index, name="myadmin_groupmember_index"),
    path('groupmember/check/<int:mid>', groupMember.check, name="myadmin_groupmember_check"),
    path('groupmember/add', groupMember.add, name="myadmin_groupmember_add"),
    path('groupmember/insert', groupMember.insert, name="myadmin_groupmember_insert"),
    path('groupmember/del/<int:mid>', groupMember.delete, name="myadmin_groupmember_delete"),
    path('groupmember/edit/<int:mid>', groupMember.edit, name="myadmin_groupmember_edit"),
    path('groupmember/update/<int:mid>', groupMember.update, name="myadmin_groupmember_update"),

    path('notice/<int:pIndex>', notice.index, name="myadmin_notice_index"),
    path('notice/add', notice.add, name="myadmin_notice_add"),
    path('notice/insert', notice.insert, name="myadmin_notice_insert"),
    path('notice/del/<int:nid>', notice.delete, name="myadmin_notice_delete"),
    path('notice/edit/<int:nid>', notice.edit, name="myadmin_notice_edit"),
    path('notice/update/<int:nid>', notice.update, name="myadmin_notice_update"),

    path('userpreference/<int:pIndex>', userPreference.index, name="myadmin_userpreference_index"),
    path('userpreference/add', userPreference.add, name="myadmin_userpreference_add"),
    path('userpreference/insert', userPreference.insert, name="myadmin_userpreference_insert"),
    path('userpreference/del/<int:uid>', userPreference.delete, name="myadmin_userpreference_delete"),
    path('userpreference/edit/<int:uid>', userPreference.edit, name="myadmin_userpreference_edit"),
    path('userpreference/update/<int:uid>', userPreference.update, name="myadmin_userpreference_update"),

    path('userbehavior/<int:pIndex>', userBehavior.index, name="myadmin_userbehavior_index"),
    path('userbehavior/add', userBehavior.add, name="myadmin_userbehavior_add"),
    path('userbehavior/insert', userBehavior.insert, name="myadmin_userbehavior_insert"),
    path('userbehavior/del/<int:uid>', userBehavior.delete, name="myadmin_userbehavior_delete"),
    path('userbehavior/edit/<int:uid>', userBehavior.edit, name="myadmin_userbehavior_edit"),
    path('userbehavior/update/<int:uid>', userBehavior.update, name="myadmin_userbehavior_update"),
]
