from rest_framework.routers import DefaultRouter
from news.views import CategoryViewSet, CommentViewSet, AuthorViewSet, ArticleViewSet,TagViewSet


router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'tags', TagViewSet)
router.register(r'articles', ArticleViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = router.urls
