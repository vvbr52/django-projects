from django.shortcuts import render,get_object_or_404
from blog.models import Post
from taggit.models import Tag
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# Create your views here.

def post_list_view(request,tag_slug=None):
    post_list=Post.objects.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        post_list=post_list.filter(tags__in=[tag])

    paginator = Paginator(post_list,3) # 3 posts in each page
    page_number = request.GET.get('page')
    try:
        post_list = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post_list = paginator.page(paginator.num_pages)
    return render(request,'blog/post_list.html',{'post_list':post_list,'tag':tag})

#display details view of post
from blog.forms import CommentForm
from django.db.models import Count

def post_detail_view(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,
                            status='published',
                            publish__year=year,
                            publish__month=month,
                            publish__day=day)
    # List of active comments for this post
    comments=post.comments.filter(active=True)
    csubmit=False
    new_comment=None
    

    if request.method=="POST":
        form=CommentForm(request.POST)
        if form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment=form.save(commit=False)
             # Assign the current post to the comment
            new_comment.post=post
            new_comment.save()
            csubmit=True
    else:
        form=CommentForm()
    return render(request,'blog/post_detail.html',{'post':post,'form':form,'csubmit':csubmit,
                    'comments':comments,'new_comment':new_comment})

#send email
from django.core.mail import send_mail
from blog.forms import EmailSendForm

def mial_send_view(request,post_id):
    post=get_object_or_404(Post,id=post_id,status='published')
    sent=False
    if request.method=='POST':
        form=EmailSendForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{}({}) recommends you to read "{}"'.format(cd['name'],cd['email'],post.title)
            message='Read Post at:\n {}\n\n{}\'s Comments:\n{} "{}"'.format(post_url,cd['name'],cd['comments'],post.body)
            send_mail(subject,message,'vvbr143@gmail.com',[cd['to']])
            sent=True
    else:
        form=EmailSendForm()
    return render(request,'blog/sharebymail.html',{'form':form,'post':post,'sent':sent})
