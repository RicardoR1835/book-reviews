from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index), 
    url(r'create$', views.create),
    url(r'login$', views.login),
    url(r'books$', views.books),
    url(r'add-book$', views.add_book),
    url(r'create-book$', views.create_book),
    url(r'book/(?P<num>\d+)$', views.show_book),
    url(r'users/(?P<num>\d+)$', views.users),
    url(r'destroy/(?P<num>\d+)$', views.destroy),
    url(r'book-review$', views.book_review),
    url(r'logout$', views.logout),
]
