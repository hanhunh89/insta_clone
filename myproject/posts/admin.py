from django.contrib import admin

# Register your models here.

from .models import Article,ProfileImage,InstaImage, Comment, Likes_table, Image, Video

#admin.site.register(Article)
admin.site.register(ProfileImage)
admin.site.register(InstaImage)
#admin.site.register(Comment)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'content', 'article', 'parent_comment', 'likes_num','child_comments_num', 'created_at')  # 여기서 'pk'를 추가
    list_display_links = ('pk', 'user')  # PK와 user 필드를 링크로 만듦

admin.site.register(Comment, CommentAdmin)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'caption', 'content', 'likes_num', 'comments_num', 'content_type','created_at')  # 여기서 'pk'를 추가
    list_display_links = ('pk', 'author')  # PK와 user 필드를 링크로 만듦

admin.site.register(Article, ArticleAdmin)


class Likes_table_Admin(admin.ModelAdmin):
    list_display=('user', 'article', 'comment', 'timestamp')
    
    
    
admin.site.register(Likes_table,Likes_table_Admin)

admin.site.register(Image)
admin.site.register(Video)