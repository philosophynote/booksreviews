from django.contrib import admin
from .models import Post,Like,Category

#管理サイトで登録できるようにする
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    #管理画面で表示されるリストの場所
    list_display = ('id','author','title','created_at')
    #リストとして認識させるために()を追加する
    #管理画面から詳細画面に飛ぶ際のリンクの場所
    list_display_links=('title',)
    #管理画面における並び順
    order_by = ('-created_at',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id','post','user')
    list_display_links=('post',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)


