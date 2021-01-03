from django.shortcuts import render,HttpResponse,redirect
from blog.models import BlogPost,BlogComment
from django.contrib import messages
from blog.templatetags import extras
# Create your views here.
def  blogHome(request):
    allPosts = BlogPost.objects.all()
    print(allPosts)
    context = {'allPosts':allPosts}
    return render(request,'blog/blogHome.html',context)

def  blogPost(request,slug):
    post = BlogPost.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post=post, parent = None)
    replies = BlogComment.objects.filter(post=post).exclude(parent = None)
    replyDict = {}
    for reply in replies:
        if reply.parent.s_no not in replyDict.keys():
            replyDict[reply.parent.s_no] = [reply]
        else:
            replyDict[reply.parent.s_no].append(reply)

    # print(comments, replies)
    print(replyDict)
    context = {'post':post,'comments':comments, 'replyDict':replyDict}
    return render(request,'blog/postView.html',context)

def  postComment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        post = BlogPost.objects.get(sno = postSno)
        parents_no = request.POST.get("parents_no")
        if parents_no=="":
            comment = BlogComment(comment = comment,user = user, post = post)
            messages.success(request,"Comment has been posted")

        else:
            parent = BlogComment. objects.get(s_no = parents_no)
            comment = BlogComment(comment = comment,user = user, post = post,parent=parent)
            messages.success(request,"reply has been posted")

        comment.save()
    return redirect(f"/blog/{post.slug}")

