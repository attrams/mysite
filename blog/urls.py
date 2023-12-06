from django.urls import path

from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'

urlpatterns = [
    path(route='', view=views.post_list, name='post_list'),
    # path(route='', view=views.PostListView.as_view(), name='post_list'),
    path(route='tag/<slug:tag_slug>/',
         view=views.post_list, name='post_list_by_tag'),
    path(
        route='<int:year>/<int:month>/<int:day>/<slug:post>/',
        view=views.post_detail,
        name='post_detail'
    ),
    path('<int:post_id>/share/', view=views.post_share, name='post_share'),
    path('<int:post_id>/comment/', view=views.post_comment, name='post_comment'),
    path('feed/', LatestPostsFeed(), name='post_feed')
]
