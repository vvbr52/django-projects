from django.contrib import admin
from blog.models import Post,Comment

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display=['title','slug','author','body','publish','created','updated','status'] #to display the fields in Admin page
    prepopulated_fields={'slug':('title',)} #To auto populate based on title
    list_filter=('status','author','publish','created') #To show filter option in Admin page
    search_fields=('title','body',)
    raw_id_fields=('author',)
    date_hierarchy='publish'
    ordering=['status','publish']
class CommentAdmin(admin.ModelAdmin):
    list_display=('name','email','post','body','created','update','active')
    list_filter=('active','created','update')
    search_fields=('name','email','body')

admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)
