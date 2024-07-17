from django.contrib import admin

from news.models import Author, Tag, Category, Comment, Article

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'bio')
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'author', 'published_at')
    list_filter = ('category', 'author', 'tags', 'published_at')
    search_fields = ('title', 'content')
    raw_id_fields = ('category', 'author')
    filter_horizontal = ('tags',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'article', 'author', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('author', 'content')
    raw_id_fields = ('article',)