from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
# post views
path('', views.post_list_view, name='post_list'),
path('tag/<slug:tag_slug>/',views.post_list_view, name='post_list_view_by_tag'),
path('<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_detail_view,name='post_detail'),
path('<int:post_id>/share/',views.mial_send_view, name='post_share'),
]
