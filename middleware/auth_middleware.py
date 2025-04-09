from django import urls
from website import views


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [
            urls.reverse("loginpage"),
            urls.reverse("menuiniciopage"),
        ]

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        try:
            if (views.Login.)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
