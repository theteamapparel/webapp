from django.urls import path
from . import views

urlpatterns = [
    path("blog", views.homepage, name="homepage"),
    path("newsletter", views.newsletter, name="newsletter"),
    path("new_post", views.new_post, name="post-create"),
    path("<str:article>", views.article, name="article"),
    path("<article>/update", views.article_update, name="article_update"),
    path("<article>/delete", views.article_delete, name="article_delete"),
    path("<article>/upload_image", views.upload_image, name="upload_image"),
]

