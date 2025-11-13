from django.http import HttpResponse, HttpRequest


# Create your views here.

def home_page(request: HttpRequest):
    # DB request

    return HttpResponse(
        "Hello Oleksandra"
    )
