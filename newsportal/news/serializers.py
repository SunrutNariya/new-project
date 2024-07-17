
from rest_framework import serializers
from news.models import Tag, Category, Comment, Article, Author

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class ArticleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    author = AuthorSerializer()
    tags = TagSerializer(many=True)
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'category', 'author', 'tags', 'published_at']

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        author_instance, created = Author.objects.get_or_create(**author_data)

        category_data = validated_data.pop('category')
        category_instance, created = Category.objects.get_or_create(**category_data)

        tags_data = validated_data.pop('tags')
        tags_instances = [Tag.objects.get_or_create(**tag_data)[0] for tag_data in tags_data]

        article_instance = Article.objects.create(
            author=author_instance,
            category=category_instance,
            **validated_data
        )
        article_instance.tags.set(tags_instances)
        return article_instance

    def update(self, instance, validated_data):
        category_data = validated_data.pop('category', None)
        author_data = validated_data.pop('author', None)
        tags_data = validated_data.pop('tags', None)

        if category_data:
            category, _ = Category.objects.get_or_create(**category_data)
            instance.category = category

        if author_data:
            author, _ = Author.objects.get_or_create(**author_data)
            instance.author = author

        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.published_at = validated_data.get('published_at', instance.published_at)
        instance.save()

        if tags_data:
            instance.tags.clear()
            for tag_data in tags_data:
                tag, _ = Tag.objects.get_or_create(**tag_data)
                instance.tags.add(tag)

        return instance


class CommentSerializer(serializers.ModelSerializer):
    article = ArticleSerializer()
    
    class Meta:
        model = Comment
        fields = ['id', 'article', 'author', 'content', 'created_at']

    def create(self, validated_data):
        article_title = validated_data.pop('article').get('title')
        article_instance, _ = Article.objects.get_or_create(title=article_title, defaults={})
        
        comment = Comment.objects.create(article=article_instance, **validated_data)
        return comment
    

    def update(self, instance, validated_data):
        article_title = validated_data.pop('article').get('title', instance.article.title)
        article_instance, _ = Article.objects.get_or_create(title=article_title, defaults={})
        
        instance.article = article_instance
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance