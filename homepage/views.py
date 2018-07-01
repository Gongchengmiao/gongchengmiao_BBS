from django.shortcuts import render

# Create your views here.


def show_info(request, uid):
    print(uid)
    return render(request, "personal_page_demo.html")
