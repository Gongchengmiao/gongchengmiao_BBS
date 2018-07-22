from django.shortcuts import render, redirect, get_object_or_404
from user.models import common_member, common_member_action_log, follower_pair, common_member_star
from article.models import ArticlePost
from django.urls import reverse
from homepage.form import UserInfoChangeForm
from django.contrib.auth.decorators import login_required
from gongchengmiao_BBS import settings
from django.http import HttpResponse, JsonResponse
# Create your views here.


@login_required(login_url='/login/')
def show_info(request, slug):
    user = get_object_or_404(common_member, slug=slug)  # 被浏览者
    actions = common_member_action_log.objects.filter(uid=user).order_by('-dateline')[0:2]

    # if request.method == 'GET' and len(request.GET):
    #     if 'btn' in list(request.GET) and request.GET['btn'] == 'show_more':
    #         actions = common_member_action_log.objects.filter(uid=user).order_by('-dateline')[0:10]
    #     elif 'btn' in list(request.GET) and request.GET['btn'] == 'follow_him'and slug != request.user.slug:
    #         common_member.objects.filter(slug=slug).update(followed=user.followed+1)
    #         common_member.objects.filter(username=request.user.username).update(following=request.user.following+1)
    #         follower_pair.objects.create(followed=user, by=request.user)
    #         user = common_member.objects.filter(slug=slug)  # 被浏览者
    #         user = user[0]
    #     elif 'btn' in list(request.GET) and request.GET['btn'] == 'send_msg':
    #         pass
    #     elif 'star_btn' in list(request.GET):
    #         the_post = ArticlePost.objects.filter(pid=int(request.GET['star_btn']))[0]
    #         common_member_action_log.objects.create(uid=request.user, pid=the_post, action='star')
    #         if len(common_member_star.objects.filter(uid=request.user, pid=the_post)) != 0:
    #             common_member_star.objects.create(uid=request.user, pid=the_post)

    context = {
        'user': user,
        'actions': enumerate(actions)
    }

    return render(request, 'x_personal_page_show_demo.html', context)


@login_required(login_url='/login/')
def view_self_info(request):
    my_actions = common_member_action_log.objects.filter(uid=request.user).order_by('-dateline')[0:10]
    my_following_pair = follower_pair.objects.filter(by=request.user).order_by('-follow_time').all()[0:8]
    my_followings = []
    for fo in my_following_pair:
        my_followings.append(fo.followed)
    following_actions = common_member_action_log.objects.filter(uid__in=my_followings).order_by('-dateline')[0:10]
    my_star_posts = common_member_star.objects.filter(uid=request.user).order_by('-star_time')[0:10]
    portrait = str(request.user.portrait)

    context = {
        'user_self': request.user,
        'portrait': portrait,
        'my_actions': enumerate(my_actions),
        'followings': enumerate(my_followings),
        'following_actions': enumerate(following_actions),
        'my_star_posts': enumerate(my_star_posts)
    }

    return render(request, 'x_personal_page_demo.html', context)


@login_required(login_url='/login/')
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

        return redirect(reverse('view_self_info'))


@login_required(login_url='/login/')
def show_info_ajax_follow(request):
    #print(request.GET.get("user_slug"))
    target_slug = request.GET.get("user_slug")
    if target_slug != request.user.slug:
        target_user = common_member.objects.filter(slug=target_slug).first()
        common_member.objects.filter(slug=target_slug).update(followed=target_user.followed + 1)
        common_member.objects.filter(username=request.user.username).update(following=request.user.following + 1)
        follower_pair.objects.create(followed=target_user, by=request.user)
        return HttpResponse('关注成功')
    else:
        return HttpResponse('不能关注本人')


@login_required(login_url='/login/')
def show_info_ajax_more(request):
    target_slug = request.GET.get("user_slug")
    target_user = common_member.objects.filter(slug=target_slug).first()
    present_ac_num = int(request.GET.get("action_num"))
    if present_ac_num == common_member_action_log.objects.filter(uid=target_user).count():
        context={
            "isFull": '1'
        }
        return JsonResponse(context)
    add_actions = common_member_action_log.objects.filter(uid=target_user).order_by('-dateline')[present_ac_num:]
    action_list = []
    for ac in add_actions:
        item = {'time': '', 'type': '', 'title': ''}
        item['time'] = ac.dateline.strftime('%a %d/%m/%y')
        item['type'] = ac.action
        item['title'] = ac.pid.title
        action_list.append(item)
    context = {
        'isFull': 0,
        'user': str(target_user.username),
        'portrait': settings.MEDIA_URL+target_user.portrait.name,
        'list': action_list
    }

    return JsonResponse(context)


@login_required(login_url='/login/')
def show_info_ajax_star(request):
    the_post = ArticlePost.objects.filter(pid=int(request.GET['pid']))[0]
    if len(common_member_star.objects.filter(uid=request.user, pid=the_post)) == 0:
        common_member_action_log.objects.create(uid=request.user, pid=the_post, action='star')
        common_member_star.objects.create(uid=request.user, pid=the_post)
        return HttpResponse('收藏成功')
    else:
        return HttpResponse('已经收藏该帖')


