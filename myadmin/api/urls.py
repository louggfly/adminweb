# 后台管理子路由文件
from django.urls import path

from myadmin.api import user_api, shop_api, area_api, group_api, comment_api, auto_api, recommend_api

urlpatterns = [
    # 用户api
    path('register/', user_api.Register.as_view()),
    path('login/', user_api.Login.as_view()),
    path('userinfo/', user_api.UserInfo.as_view()),
    path('user/', user_api.AllUser.as_view()),
    path('userfavourite/', user_api.UserFavouriteShop.as_view()),
    path('userfavouritecreate/', user_api.UserFavouriteCreate.as_view()),
    path('userfavouritedelete/', user_api.UserFavouriteDelete.as_view()),
    path('usercomment/', user_api.UserCommentList.as_view()),
    path('userupdateinfo/', user_api.UpdateUserInfo.as_view()),
    path('userupdatearea/', user_api.UpdateUserArea.as_view()),
    path('userupdateavatar/', user_api.UpdateUserAvatar.as_view()),
    path('userupdatephone/', user_api.UpdateUserPhone.as_view()),
    path('searchuser/', user_api.SearchUser.as_view()),

    # 店铺api
    path('shop/', shop_api.AllShop.as_view()),
    path('searchshop/', shop_api.SearchShop.as_view()),
    path('queryshop/', shop_api.QueryShop.as_view()),
    path('queryshopcommentlist/', shop_api.QueryShopCommentList.as_view()),
    path('queryshopcomment/', shop_api.QueryShopComment.as_view()),
    path('recommendedshop/', shop_api.RecommendedShop.as_view()),
    path('popularshop/', shop_api.PopularShop.as_view()),
    # 评论api
    path('comment/', comment_api.AllComment.as_view()),
    path('commentsearch/', comment_api.SearchComment.as_view()),
    path('commentrelease/', comment_api.ReleaseComment.as_view()),
    path('commentupdate/', comment_api.UpdateComment.as_view()),
    path('commentdelete/', comment_api.DeleteComment.as_view()),
    # 地区api
    path('area/', area_api.AllArea.as_view()),
    path('areasearch/', area_api.SearchArea.as_view()),
    # 小队api
    path('group/', group_api.UserGroup.as_view()),
    path('groupcreate/', group_api.CreateGroup.as_view()),
    path('groupupdate/', group_api.UpdateGroup.as_view()),
    path('groupdelete/', group_api.DeleteGroup.as_view()),
    # 自动评分api
    path('autoscoresenta/', auto_api.SentaAutoScore.as_view()),
    path('autoscorebert/', auto_api.BertAutoScore.as_view()),
    # 推荐算法api
    path('category/', recommend_api.AllCategory.as_view()),
    path('userpreference/', recommend_api.UserPreferenceList.as_view()),
    path('userpreferencecreate/', recommend_api.UserPreferenceCreate.as_view()),
    path('userpreferencedelete/', recommend_api.UserPreferenceDelete.as_view()),
]
