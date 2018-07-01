from django.shortcuts import render

# Create your views here.


def show_info(request, uid):
    print('show_info')
    return render(request, "personal_page_show_demo.html")


def view_self_info(request):
    print('view_self')

    return render(request, 'personal_page_demo.html')


def edit_info(request):
    print("edit")
    return render(request, 'edit_person_demo.html')
