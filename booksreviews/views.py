from django.shortcuts import render,resolve_url, redirect
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseServerError
from django.views.generic import TemplateView,CreateView,DetailView,UpdateView,DeleteView,ListView
from .models import Post,Like,Category
from django.urls import reverse_lazy
from .forms import PostForm,LoginForm,SignupForm,SearchForm
from django.contrib import messages
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
#関数で定義したものはデコレータ
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.csrf import requires_csrf_token


class OnlyMyPostMinin(UserPassesTestMixin):
    raise_exception = True
    def test_func(self):
        post = Post.objects.get(id = self.kwargs['pk'])
        return post.author==self.request.user

class Index(TemplateView):
    template_name = 'app/index.html'

    #標準搭載されている関数
    def get_context_data(self,*args ,**kwargs):
        #おまじない
        context = super().get_context_data(**kwargs)
        #投稿された内容を作成日順に全てとってくる
        post_list = Post.objects.all().order_by('-created_at')[:6]
        context = {
            "post_list":post_list,
        }
        return context


class PostCreate(LoginRequiredMixin,CreateView):
    template_name = 'app/post_form.html' 
    
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('booksreviews:index')

    def form_valid(self,form):
        # 著者のidはログインしているユーザと一致
        form.instance.author_id = self.request.user.id
        # 上書き
        return super(PostCreate, self).form_valid(form)
    
    def get_success_url(self):
        messages.success(self.request,'Postを登録しました。')
        return resolve_url('booksreviews:index')

class PostDetail(DetailView):
    template_name = 'app/post_detail.html' 

    model = Post

    def get_context_data(self, *args ,**kwargs):
        detail_data = Post.objects.get(id=self.kwargs['pk'])
        category_posts = Post.objects.filter(category = detail_data.category).order_by('-created_at')[:5]
        params = {
            'object':detail_data,
            'category_posts':category_posts,
        }
        return params

class PostUpdate(OnlyMyPostMinin,UpdateView):
    template_name = 'app/post_form.html' 

    model = Post
    form_class = PostForm

    def get_success_url(self):
        messages.info(self.request,"Postを更新しました。")
        return resolve_url('booksreviews:post_detail',pk = self.kwargs['pk'])

class PostDelete(OnlyMyPostMinin,DeleteView):
    template_name = 'app/post_confirm_delete.html' 

    model = Post

    def get_success_url(self):
        messages.info(self.request,"Postを削除しました。")
        return resolve_url('booksreviews:index')

class PostList(ListView):
    template_name = 'app/post_list.html'
    model = Post
    pagenate_by = 2

    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')

class Login(LoginView):
    form_class = LoginForm
    template_name = 'app/login.html'

class Logout(LogoutView):
    template_name = 'app/logout.html'

class Signup(CreateView):
    form_class = SignupForm
    template_name = 'app/signup.html'
    success_url = reverse_lazy('booksreviews:index')

    def form_valid(self, form):
        user = form.save()
        login(self.request,user)
        self.object = user
        messages.info(self.request,'ユーザー登録をしました')
        return HttpResponseRedirect(self.get_success_url())

@login_required
def Like_add(request,post_id):
    post = Post.objects.get(id = post_id)
    is_liked = Like.objects.filter(user=request.user).filter(post = post_id).count()
    if is_liked > 0:
        messages.info(request,'すでにお気に入りに追加済みです')
        return redirect('booksreviews:post_detail',post.id)

    like = Like()
    like.user = request.user
    like.post = post
    like.save()
    
    messages.success(request,'お気に入りに追加しました！')
    return redirect('booksreviews:post_detail', post.id)

class CategoryList(ListView):
    template_name = 'app/category_list.html'
    model = Category

class CategoryDetail(DetailView):
    template_name = 'app/category_detail.html'
    model = Category
    #URLで使用する場合は次の記述が必要
    slug_field = 'name_en'
    slug_url_kwarg = 'name_en'
    
    def get_context_data(self, *args,**kwargs):
        detail_data = Category.objects.get(name_en = self.kwargs['name_en'])
        category_posts = Post.objects.filter(category = detail_data.id).order_by('-created_at')

        params = {
            'object':detail_data,
            'category_posts':category_posts,
        }

        return params

def Search(request):
    if request.method == 'POST':
        searchform = SearchForm(request.POST) 

        if searchform.is_valid():
           #claened_data(is_validした結果のデータ)
           freeword = searchform.cleaned_data['freeword'] 
           search_list = Post.objects.filter(Q(title__icontains = freeword) |Q(content__icontains = freeword))
        
        params = {
            'search_list':search_list,
        }
        return render(request, 'app/search.html',params)


@requires_csrf_token
def my_customized_server_error(request, template_name='500.html'):
    import sys
    from django.views import debug
    error_html = debug.technical_500_response(request, *sys.exc_info()).content
    return HttpResponseServerError(error_html)
