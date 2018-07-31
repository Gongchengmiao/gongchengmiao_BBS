from django.shortcuts import render, redirect, get_object_or_404
from user.models import common_member, common_member_action_log, follower_pair, common_member_star
from article.models import ArticlePost, Comment
from django.urls import reverse
from homepage.form import UserInfoChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from gongchengmiao_BBS import settings
from django.http import HttpResponse, JsonResponse
import os
import time
# Create your views here.


@login_required(login_url='/login/')
def show_info(request, slug):
    user = get_object_or_404(common_member, slug=slug)  # 被浏览者
    actions = common_member_action_log.objects.filter(uid=user).order_by('-dateline')[0:5]

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
    my_following_id = follower_pair.objects.filter(by=request.user).order_by('-follow_time').values('followed')
    my_followings = common_member.objects.filter(id__in=my_following_id).all()
    following_actions = common_member_action_log.objects.filter(uid__in=my_followings).order_by('-dateline')[0:10]
    my_star_pids = common_member_star.objects.filter(uid=request.user).order_by('-star_time').values('pid')[0:10]
    my_star_posts = ArticlePost.objects.filter(pid__in=my_star_pids).all()
    portrait = str(request.user.portrait.name)
    my_followings = my_followings[0:8]
    my_articles_id = ArticlePost.objects.filter(author=request.user).values('pid').all()
    comments = Comment.objects.filter(article_id__in=my_articles_id).order_by('-created').all()[0:1]

    context = {
        'user_self': request.user,
        'portrait': portrait,
        'percentage': request.user.points/100,
        'my_actions': enumerate(my_actions),
        'followings': enumerate(my_followings),
        'following_actions': enumerate(following_actions),
        'my_star_posts': enumerate(my_star_posts),
        'comments': enumerate(comments),
    }

    return render(request, 'x_personal_page_demo.html', context)

@login_required(login_url='/login/')
def view_self_ajax_scroll(request):
    if request.GET.get('tab') is None:
        return HttpResponse()
    pre_num = int(request.GET.get('pre_num'))
    tab = request.GET.get('tab')
    item_list = []
    if tab == '1':
        my_following_id = follower_pair.objects.filter(by=request.user).order_by('-follow_time').values('followed')
        my_followings = common_member.objects.filter(id__in=my_following_id).all()
        following_actions = common_member_action_log.objects.filter(uid__in=my_followings).order_by('-dateline')[pre_num :pre_num+5]
        for ac in following_actions:
            item = {}
            item = item.fromkeys(('portrait', 'user_url', 'username', 'date_time', 'action_body', 'post_url', 'post_title', ))
            item['portrait'] = settings.MEDIA_URL+ac.uid.portrait.name
            item['user_url'] = "homepage/uid="+ac.uid.slug+"/"
            item['username'] = ac.uid.username
            item['date_time'] = ac.dateline.strftime('%d/%m/%y')
            if ac.action == 'post':
                item['action_body'] = '发表了'
            elif ac.action == 'star':
                item['action_body'] = '收藏了'
            elif ac.action == 'upload':
                item['action_body'] = '上传了'
            item['post_url'] = ac.pid.get_url()
            item['post_title'] = ac.pid.title
            item_list.append(item)
    elif tab == '2':
        my_actions = common_member_action_log.objects.filter(uid=request.user).order_by('-dateline')[pre_num:pre_num+5]
        for ac in my_actions:
            item = {}
            item = item.fromkeys(('portrait', 'user_url', 'username', 'date_time', 'action_body', 'post_url', 'post_title', ))
            item['portrait'] = settings.MEDIA_URL+ac.uid.portrait.name
            item['user_url'] = "homepage/uid="+ac.uid.slug+"/"
            item['username'] = "你"
            item['date_time'] = ac.dateline.strftime('%d/%m/%y')
            if ac.action == 'post':
                item['action_body'] = '发表了'
            elif ac.action == 'star':
                item['action_body'] = '收藏了'
            elif ac.action == 'upload':
                item['action_body'] = '上传了'
            item['post_url'] = ac.pid.get_url()
            item['post_title'] = ac.pid.title
            item_list.append(item)
    elif tab == '3':
        my_star_pids = common_member_star.objects.filter(uid=request.user).order_by('-star_time').values('pid')[pre_num:pre_num+5]
        my_star_posts = ArticlePost.objects.filter(pid__in=my_star_pids).all()
        for po in my_star_posts:
            item = {}
            item = item.fromkeys(('title', 'isElite', 'post_url', 'pub_time', 'author', 'author_url'))
            item['title'] = po.title
            item['isElite'] = po.isElite
            item['author'] = po.author.username
            item['author_url'] = "homepage/uid="+po.author.uid.slug+"/"
            item['post_url'] = po.get_url()
            item['pub_time'] = po.pub_date.strftime('%d/%m/%y')
            item_list.append(item)
    elif tab == '4':
        my_articles_id = ArticlePost.objects.filter(author=request.user).values('pid').all()
        comments = Comment.objects.filter(article_id__in=my_articles_id).order_by('-created').all()[pre_num:pre_num+5]
        for co in comments:
            item = {}
            item = item.fromkeys(('article_title', 'article_url', 'portrait', 'commentator_name', 'commentator_url', 'comment_body', 'time'))
            item['article_title'] = co.article.title
            item['article_url'] = co.article.get_url()
            item['portrait'] = settings.MEDIA_URL + co.commentator.portrait.name
            item['commentator_name'] = co.commentator.username
            item['commentator_url'] = reverse('show_info', kwargs={'slug':co.commentator.slug})
            item['comment_body'] = str(co.ueditor_body)
            item['time'] = co.created.strftime('%d/%m/%y')
            item_list.append(item)
    is_all = '0'
    if len(item_list) == 0:
        is_all = '1'
    context = {
        'item_list': item_list,
        'is_all': is_all
    }
    return JsonResponse(context)

@login_required(login_url='/login/')
def edit_info(request):

    instance_user = common_member.objects.filter(username=request.user.username).first()
    if request.method == 'GET':
        myform = UserInfoChangeForm(instance=instance_user)
        return render(request, "x_edit_person_demo.html", {"form": myform, "portrait": request.user.portrait})
    else:
        myform = UserInfoChangeForm(request.POST, request.FILES, instance=instance_user)
        if myform.is_valid():
            # print('valid')
            myform.save()
            print(myform.errors)
        else:
            print(myform.errors)
        return render(request, "x_edit_person_demo.html", {"form": myform, "portrait": request.user.portrait})


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
        context = {
            "isFull": '1'
        }
        return JsonResponse(context)
    add_actions = common_member_action_log.objects.filter(uid=target_user).order_by('-dateline')[present_ac_num:present_ac_num+5]
    action_list = []
    for ac in add_actions:
        item = {'time': '', 'type': '', 'title': '', 'post_url':"", 'pid':''}
        item['pid'] = str(ac.pid.pid)
        item['time'] = ac.dateline.strftime('%a %d/%m/%y')
        item['type'] = ac.get_action_display()
        item['title'] = ac.pid.title
        item['post_url'] = ac.pid.get_url()
        action_list.append(item)
    context = {
        'isFull': 0,
        'user': str(target_user.username),
        'user_url': str(reverse('show_info', kwargs={'slug': target_user.slug})),
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


@login_required(login_url='/login/')
@csrf_exempt
def edit_info_ajax_save_portrait(request):
    alt = request.POST.get('portrait_alt')
    if alt == 'image_upload':
        user = common_member.objects.filter(id=request.user.id).first()
        user.portrait.name = 'portraits/'+user.temp_portrait.name
        user.save()
    elif alt != 'image':
        image_dir = {
            'default_img1': "portraits/default_img/boy_glasses.jpg",
            'default_img2': "portraits/default_img/boy_hat.jpg",
            'default_img3': "portraits/default_img/boy_sport.jpg",
            'default_img4': "portraits/default_img/girl_rollhair.jpg",
            'default_img5': "portraits/default_img/girl_shorthair.jpg",
            'default_img6': "portraits/default_img/girl_silent.jpg",
        }
        common_member.objects.filter(id=request.user.id).update(portrait=image_dir[alt])

    return HttpResponse(request.POST.get('portrait_alt'))



@login_required(login_url='/login/')
@csrf_exempt
def edit_info_ajax_upload_temp(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        img = request.FILES.get('img')
        # print(user, img.name)
        path = os.path.join(settings.MEDIA_ROOT+'\\portraits', img.name)
        f = open(path, 'wb')
        for chunk in img.chunks():
           f.write(chunk)
        f.close()
        common_member.objects.filter(id=request.user.id).update(temp_portrait=img.name)
        # common_member.objects.filter(id=request.user.id).temp_portrait.save(name=img.name)
        return HttpResponse('ok')
    return HttpResponse()


@login_required(login_url='/login/')
@csrf_exempt
def edit_info_ajax_get_temp(request):
    user = common_member.objects.filter(id=request.user.id).first()
    ret = settings.MEDIA_URL + 'portraits/' + user.temp_portrait.name
    context = {
        'temp_src': str(ret)
    }

    return JsonResponse(context)


def delete_temp(request):
    user = common_member.objects.filter(id=request.user.id).first()
    if ('portraits/' + user.temp_portrait.name) != user.portrait.name:
        path = os.path.join(settings.MEDIA_ROOT + '\\portraits', user.temp_portrait.name)
        if os.path.exists(path) and user.temp_portrait.name != '':
            os.remove(path)
    return HttpResponse('deleted')
