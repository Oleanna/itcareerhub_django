from django.http import HttpResponse, HttpRequest



def home_page(request: HttpRequest):
    # DB request

    return HttpResponse(
        "Task Manager",
    )