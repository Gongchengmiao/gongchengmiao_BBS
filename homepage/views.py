from django.shortcuts import render,redirect
from user.models import common_member, common_member_action_log, follower_pair, common_member_star
from article.models import forum_post
from django.urls import reverse
from homepage.form import UserInfoChangeForm
from gongchengmiao_BBS import settings
from django.http import HttpResponseRedirect
# Create your views here.


def show_info(request, username):
    user = common_member.objects.filter(username=username)  # 被浏览者
    if len(user) == 0:
        return redirect(reverse('index'))
    user = user[0]
    actions = common_member_action_log.objects.filter(uid=user).order_by('-dateline')[0:5]

    if request.method == 'GET' and len(request.GET):
        if 'btn' in list(request.GET) and request.GET['btn'] == 'show_more':
            actions = common_member_action_log.objects.filter(uid=user).order_by('-dateline')[0:10]
        elif 'btn' in list(request.GET) and request.GET['btn'] == 'follow_him'and username != request.user.username:
            common_member.objects.filter(username=username).update(followed=user.followed+1)
            common_member.objects.filter(username=request.user.username).update(following=request.user.following+1)
            follower_pair.objects.create(followed=user, by=request.user)
            user = common_member.objects.filter(username=username)  # 被浏览者
            user = user[0]
        elif 'btn' in list(request.GET) and request.GET['btn'] == 'send_msg':
            pass
        elif 'star_btn' in list(request.GET):
            the_post = forum_post.objects.filter(pid=int(request.GET['star_btn']))[0]
            common_member_action_log.objects.create(uid=request.user, pid=the_post, action='star')
            if len(common_member_star.objects.filter(uid=request.user, pid=the_post)) != 0:
                common_member_star.objects.create(uid=request.user, pid=the_post)

    context = {
        'username': user.username,
        'gender': user.gender,
        'profile': user.profile,
        'posts': user.posts,
        'following': user.following,
        'followed': user.followed,
        'portrait': user.portrait,
        'actions': enumerate(actions)
    }

    return render(request, 'personal_page_show_demo.html', context)



def view_self_info(request):
    # print('view_self')
    if request.user.is_authenticated == False:
        return redirect(reverse('login'))
    my_actions = common_member_action_log.objects.filter(uid=request.user).order_by('-dateline')[0:10]

    my_followings = follower_pair.objects.filter(by=request.user).order_by('-follow_time').all()
    following_id = []
    for following in my_followings:
        following_id.append(following.followed)
    following_actions = common_member_action_log.objects.filter(uid__in=following_id).order_by('-dateline')[0:10]
    following_id = following_id[0:5]
    my_star_posts = common_member_star.objects.filter(uid=request.user).order_by('-star_time')[0:10]
    portrait = str(request.user.portrait)
    context = {
        'username': request.user.username,
        'portrait': portrait,
        'gender': request.user.gender,
        'profile': request.user.profile,
        'posts': request.user.posts,
        'my_actions': enumerate(my_actions),
        'followings': enumerate(following_id),
        'following_actions': enumerate(following_actions),
        'my_star_posts': enumerate(my_star_posts)
    }

    return render(request, 'personal_page_demo.html', context)


def edit_info(request):
    if request.user.is_authenticated == False:
        return redirect(reverse('login'))

    instance_user = common_member.objects.filter(username=request.user.username).all()[0]
    if request.method == 'GET':
        myform = UserInfoChangeForm(instance=instance_user)
        return render(request, "edit_person_demo.html", {"form": myform, "portrait": request.user.portrait})
    else:
        myform = UserInfoChangeForm(request.POST, request.FILES, instance=instance_user)
        if myform.is_valid():
            # print('valid')
            myform.save()
            # print(myform.errors)
        else:
            # print(myform.errors)
            pass
        return render(request, 'edit_person_demo.html', {"form": myform, "portrait": request.user.portrait})
