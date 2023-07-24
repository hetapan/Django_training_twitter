from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from .forms import PostCreateForm, PostUpdateForm
from django.contrib import messages
from django.urls import reverse_lazy, reverse


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'microposts/create.html'
    form_class = PostCreateForm
    success_url = reverse_lazy('microposts:create')

    def form_valid(self, form):
        # formに問題なければ、owner id に自分のUser idを割り当てる
        # request.userが一つのセットでAuthenticationMiddlewareでセットされている。
        form.instance.owner_id = self.request.user.id
        messages.success(self.request, '投稿が完了しました')
        return super(PostCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, '投稿が失敗しました')
        return redirect('microposts:create')


class PostListView(LoginRequiredMixin, ListView):
    # テンプレートを指定
    template_name = 'microposts/postlist.html'
    # 利用するモデルを指定
    model = Post
    # ページネーションの表示件数
    paginate_by = 3

    # Postsテーブルの全データを取得するメソッド定義
    # テンプレートでは、object_listとしてreturnの値が渡される
    def get_queryset(self):
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['favourite_list'] = user.favourite_post.all()

        return context


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostUpdateForm
    template_name = 'microposts/update.html'
    def form_valid(self, form):
        messages.success(self.request, '更新が完了しました')
        return super(PostUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('microposts:update', kwargs={'pk': self.object.id})

    def form_invalid(self, form):
        messages.warning(self.request, '更新が失敗しました')
        return reverse('microposts:update', kwargs={'pk': self.object.id})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'microposts/delete.html'

    success_url = reverse_lazy('microposts:create')
    success_message = "投稿は削除されました。"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(PostDeleteView, self).delete(request, *args, **kwargs)


class MyPostsView(LoginRequiredMixin, ListView):

    template_name = 'microposts/myposts.html'

    model = Post

    paginate_by = 3

    # Postsテーブルのowner_idが自分自身の全データを取得するメソッド定義
    def get_queryset(self): # 自分の投稿オブジェクトを返す。
        return Post.objects.filter(owner_id=self.request.user)

    def get_context_data(self, **kwargs):
        # デフォルトのコンテキストデータを取得
        context = super().get_context_data(**kwargs)

        # Postsテーブルの自分の投稿数をmy_posts_countへ格納
        context['my_posts_count'] = Post.objects.filter(owner_id=self.request.user).count()
        return context


def add_favourite(request, pk):
    # postのpkをhtmlから取得
    post = get_object_or_404(Post, pk=pk)
    # ログインユーザーを取得
    user = request.user
    # ログインユーザーをfavoritePostのUser_idとして、post_idは
    # 上で取得したPostを記録
    user.favourite_post.add(post)
    return redirect('microposts:postlist')

def remove_favourite(request, pk):
    # postのpkをhtmlから取得
    post = get_object_or_404(Post, pk=pk)
    # ログインユーザーを取得
    user = request.user
    # ログインユーザーをfavoritePostのUser_idとして、post_idは
    # 上で取得したPostを記録
    user.favourite_post.remove(post)
    return redirect('microposts:postlist')