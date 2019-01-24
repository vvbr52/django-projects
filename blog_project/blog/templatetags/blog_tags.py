
from blog.models import Post
from django import template

register=template.Library()

#to show count of totoal publised posts
@register.simple_tag()
def total_posts():
    return Post.objects.count()

#to show latest posts 3

@register.inclusion_tag('blog/latest_posts.html')
def show_latest_posts(count=3):
    latest_posts=Post.objects.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}

from django.db.models import Count
#to display most commented posts
@register.simple_tag
def get_most_commented_posts(count=3):
    return Post.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
