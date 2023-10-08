# Create your views here.
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Article, ProfileImage, InstaImage, Likes_table, Comment

from django.views import View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core import serializers
from django.utils import timezone
from .forms import VideoForm, ImageForm
#class PostListView(LoginRequiredMixin, ListView):
class PostListView(ListView):
    model = Article
    template_name = 'posts/post_list.html'
    login_url = '/custom-login-page/'  # 로그인되지 않은 사용자가 접근하면 여기로 리디렉션
    context_object_name = 'posts'

    def get_queryset(self):
        queryset=super().get_queryset()

        user=self.request.user

        for article in queryset:
            article.is_liked=Likes_table.objects.filter(user=user, article=article).exists()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # ProfileImage 모델에서 로그인한 사용자의 프로필 이미지 가져오기
        user = self.request.user
        try:
            profile_image = ProfileImage.objects.get(user=user)
        except ProfileImage.DoesNotExist:
            profile_image = None
        context['profile_image'] = profile_image

        # insta_image 모델에서 title이 like_heart_black인 레코드의 이미지 가져오기
        like_heart_black_image = InstaImage.objects.get(title="like_heart_black")
        like_heart_red_image = InstaImage.objects.get(title="like_heart_red")

        context['like_heart_black_image'] = like_heart_black_image
        context['like_heart_red_image'] = like_heart_red_image
        
        for post in context['posts']:
            post.created_at = post.created_at.astimezone(timezone.utc).isoformat()

        return context
    

class Like_article_button_click_V(View):
    def post(self, request, pk):
        # Get the article using the provided pk
        article = get_object_or_404(Article, pk=pk)
        
        # Check if the user has already liked the article
        liked_by_user = Likes_table.objects.filter(user=request.user, article=article, comment__isnull=True).exists()
        
        if liked_by_user:
            # User has already liked the article, so unlike it
            Likes_table.objects.filter(user=request.user, article=article, comment__isnull=True).delete()
            message = 'cancel'  # 좋아요가 이미 취소되었다는 메시지
        else:
            # User has not liked the article, so like it
            like = Likes_table(user=request.user, article=article)
            like.save()
            message = 'add'  # 좋아요가 추가되었다는 메시지

        likes_num = Likes_table.objects.filter(article=article,comment__isnull=True).count()
        article.likes_num=likes_num
        article.save()
        return JsonResponse({'message': message, 'likes_num': likes_num})



class AddCommentView(View):
#    @method_decorator(login_required)  # 로그인이 필요한 경우 데코레이터 사용
    def post(self, request, *args, **kwargs):
        print("run AddCommentView")
        article = get_object_or_404(Article, pk=kwargs['pk'])
        content = request.POST.get('content', '')  # 댓글 내용 받아오기
        print("content:"+content)
        comment_parent=request.POST.get('comment_parent',-1)
        comment_parent = int(comment_parent)
        new_record_pk=-1
        parent_comment_object=-1
        print("comment_parent : "+str(comment_parent))
        if content:  # 댓글 내용이 비어있지 않을 때만 처리
            print("add content!")
            if(comment_parent==-1):
                comment = Comment(user=request.user, article=article, content=content)
                comment.save()
            else:
                parent_comment_object = Comment.objects.get(pk=comment_parent)
                comment = Comment(user=request.user, article=article, parent_comment=parent_comment_object, content=content)
                comment.save()
                comment_comment_num=Comment.objects.filter(article=article, parent_comment=parent_comment_object).count()
                parent_comment_object.child_comments_num=comment_comment_num
                parent_comment_object.save()

                
            #comment 숫자 정리
            article_comment_num=Comment.objects.filter(article=article).count()
            article.comments_num=article_comment_num
            article.save()

            new_record_pk=comment.pk
        else :
            print("there is no content. don't add comment!")
        

        comments=Comment.objects.filter(article=article)
        comments_data=[]
        for comment in comments:
            try:
                likes_table = Likes_table.objects.get(user=request.user, comment=comment)
                is_liked = True
            except Likes_table.DoesNotExist:
                is_liked = False

            new_record=False
            if(new_record_pk==comment.pk) :
                new_record=True
            
            data={
                'pk':comment.pk,
                'text':comment.content,
                'userName':comment.user.username,
                'created_at':comment.created_at,
                'num_of_like':comment.likes_num,
                'profile_image_url':ProfileImage.objects.get(user=request.user).image.url,
                'is_liked':is_liked,
                'comment_parent': comment.parent_comment.pk if comment.parent_comment else None,
                'num_of_comment':comment.child_comments_num,
                'new_record':new_record
            }
            comments_data.append(data)
        #print(comments_data)
        return JsonResponse({'message': comments_data})





class Like_comment_button_click_V(View):
    def post(self, request, pk):
        # Get the article using the provided pk
        comment = get_object_or_404(Comment, pk=pk)
        article_pk = int(request.POST.get('article', ''))  # 댓글 내용 받아오기
        article=get_object_or_404(Article, pk=article_pk)
        # Check if the user has already liked the article
        liked_by_user = Likes_table.objects.filter(user=request.user, comment=comment, article=article).exists()
        
        if liked_by_user:
            # User has already liked the article, so unlike it
            Likes_table.objects.filter(user=request.user, comment=comment, article=article).delete()
            message = 'cancel'  # 좋아요가 취소되었다는 메시지
        else:
            # User has not liked the article, so like it
            like = Likes_table(user=request.user, comment=comment, article=article)
            like.save()
            message = 'add'  # 좋아요가 추가되었다는 메시지

        likes_num = Likes_table.objects.filter(comment=comment).count()
        comment.likes_num=likes_num
        comment.save()

        return JsonResponse({'message': message, 'likes_num': likes_num})

class CommentDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        print("CommentDeleteView")

        comment = get_object_or_404(Comment, pk=pk)
        parent=comment.parent_comment
        article=comment.article
        print("삭제 전 아티클의 코멘트 수 : "+str(article.comments_num))


        child_comments=Comment.objects.filter(parent_comment=comment)
        for child in child_comments : 
            child.delete()

        try:
            comment.delete()
            
                    # comment의 부모가 있는지 확인.
            if parent is not None:
                print("comment의 부모가 있다.")
                child_comment=Comment.objects.filter(parent_comment=parent).count()
                print("comment의 부모의 댓글 수 :"+str(child_comment))
                parent.child_comments_num=child_comment
                parent.save()
            article.comments_num=Comment.objects.filter(article=article).count()
            article.save()
            print("삭제 후 아티클의 코멘트 수 : "+str(article.comments_num))
            
            
            
            return JsonResponse({'message': 'ok'})
        except Exception as e:
            print(f"Error deleting comment: {str(e)}")
            return JsonResponse({'message': 'fail'})



class Clear_likes_model(View):
    Likes_table.objects.all().delete()


class Create_articleView(View):
    @staticmethod
    def is_image(file):
        try:
            from PIL import Image
            Image.open(file)
            return True
        except Exception as e:
            return False    
    @staticmethod
    def is_video(file):
        video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv']
        return any(file.name.lower().endswith(ext) for ext in video_extensions)
    
    def post(self, request):
        print("Create_articleView post start")
        file_type = request.POST.get('type')
        print("request : "+str(request))
        print("request.POST :"+str(request.POST))
        print("reqeust.FILES : "+str(request.FILES))
        print("file type")
        print(file_type)
        if(file_type=='video'):
            file = request.FILES['video']
            print("파일에다가 비디오 삽입")
        elif(file_type=='image'):
            file = request.FILES['image']
            print("파일에다가 이미지 삽입")
        else :
            return JsonResponse({'message': 'no image no video'})     

        print(request)
        print("file :")
        print(file)
        if self.is_image(file) :
            print("if self.is_image(file) -> image")
            form = ImageForm(request.POST, request.FILES)
            print("form : "+str(form))
            if form.is_valid():
                instance = form.save()
                return JsonResponse({'message': 'ok'})
            else : 
                print("image form is invalid")
                print(form.errors)
                return JsonResponse({'message': 'form_invalid'})            
        elif self.is_video(file) :
            form = VideoForm(request.POST, request.FILES)
            print("form : "+str(form))

            if form.is_valid():
                instance = form.save()
                return JsonResponse({'message': 'ok'})
            else : 
                print("form is invalid")
                print(form.errors)
                return JsonResponse({'message': 'form_invalid'})     
        else :
            return JsonResponse({'message': 'no image no video'})     

        