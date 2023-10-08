from django.urls import path
from posts.views import PostListView,Like_article_button_click_V,AddCommentView,Like_comment_button_click_V,CommentDeleteView,Clear_likes_model
from posts.views import Clear_likes_model, Create_articleView,Get_logined_id
from posts.views import LoginView,logout_view,signup, GuestLoginView
from posts.views import Get_profile_image

app_name = 'posts'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('like_article/<int:pk>', Like_article_button_click_V.as_view(), name='like_article_button_click'),
    path('like_comment/<int:pk>', Like_comment_button_click_V.as_view(), name='like_comment_button_click'),    
    path('add_comment/<int:pk>', AddCommentView.as_view(), name="add_comment"),
    path('delete_comment/<int:pk>', CommentDeleteView.as_view(), name="delete_comment"),
    path('d/', Clear_likes_model.as_view(), name="d"),
    path('create_article/', Create_articleView.as_view(), name="create_article"),
    path('logined_id/', Get_logined_id.as_view(), name="logined_id"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup, name='signup'),
    path('get_profile_image/', Get_profile_image.as_view(), name='get_profile_image' ),
    path('guest_login/', GuestLoginView.as_view(), name="guest_login"),
]
