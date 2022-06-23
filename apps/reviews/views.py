from distutils import errors
from multiprocessing import context
from urllib import response
from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages

# the index function is called when root is visited
def index(request):
    return render(request, "reviews/index.html")

def create(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    if request.method == "POST":
        user = User.objects.create(first_name=request.POST["fn"], last_name=request.POST["ln"], email=request.POST['email'], password=request.POST["password"])
        request.session["id"] = user.id
        messages.success(request, "User was successfully created")
        return redirect('/books')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    print(user)
    request.session['id'] = user.id
    messages.success(request, "User was successfully logged in")
    return redirect('/books')


def books(request):
    if 'id' not in request.session:
        messages.success(request, "Not logged in!")
        return redirect('/')
    context = {
        "books": Book.objects.all().order_by("-created_at")[:3],
        "user": User.objects.get(id=request.session['id']),
        "other_books": Book.objects.all().order_by("-created_at")[3:],
        "count": {1,2,3,4,5}
    }
    x = Book.objects.all()

    for b in x:
        print(b.ratings)
    return render(request, "reviews/books.html", context)

def add_book(request):
    context = {
        "authors": Author.objects.all()
    }
    return render(request, 'reviews/add-book.html', context)

def create_book(request):
    user = User.objects.get(id=request.session['id'])
    errors = Book.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/add-book')
    if request.method == "POST":
        if request.POST['add_author']:
            errors1 = Author.objects.basic_validator(request.POST)
            if len(errors1) > 0:
                for key, value in errors1.items():
                    messages.error(request, value)
                return redirect('/add-book')
            author = Author.objects.create(name=request.POST['add_author'])
        else:
            author = Author.objects.get(id=request.POST['author'])
        rating = Rating.objects.create(rating=request.POST['rating'], user = user, review=request.POST['review'])
        book = Book.objects.create(title = request.POST['title'], author= author)
        book.ratings.add(rating)
        return redirect(f'/book/{book.id}')

def show_book(request, num):
    context = {
        "book": Book.objects.get(id=num),
        "count": {1,2,3,4,5}
    }
    return render(request, 'reviews/show-book.html', context)

def book_review(request):
    current_page = request.POST['book']
    book = Book.objects.get(id=request.POST['book'])
    user = User.objects.get(id=request.session['id'])
    errors = Rating.objects.basic_validator(request.POST)
    test = user.my_ratings.filter(book=book)
    if len(test) > 0:
        messages.success(request, "Can not leave multiple reviews")
        return redirect(f'/book/{current_page}')
    print(test)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/book/{current_page}')
    if request.method == "POST":
        rating = Rating.objects.create(rating=request.POST['rating'], user = user, review=request.POST['review'])
        book.ratings.add(rating)
        return redirect(f'/book/{current_page}')

def users(request, num):
    context = {
        "user": User.objects.get(id=num)
    }
    return render(request, 'reviews/user.html', context)


def destroy(request, num):
    rating = Rating.objects.get(id=num)
    rating.delete()
    return redirect("/")

def error_404(request, exception):
    data = {}
    return render(request, 'reviews/404.html', data)


def logout(request):
    del request.session['id']
    return redirect("/")