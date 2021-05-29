from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect, get_object_or_404, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
import datetime
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from easy_password_generator import PassGen


from .forms import *
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def index(request):

    return render(request, 'omega/index.html')

def summary(request):

    return render(request, 'omega/summaries.html')

def list(request):

    return render(request, 'omega/list.html')


def available(request):

    return render(request, 'omega/available1.html')

def admin(request):

    return render(request, 'omega/upload.html')

#def detail(request):

#    return render(request, 'omega/detail.html')


def upload(request):

    return render(request, 'omega/admin.html')

def welcome(request):

    return render(request, 'omega/new.html')



class SearchResultsView(ListView):
    model = Commodity
    template_name = 'omega/available.html'

    def get_queryset(self):
        name = self.kwargs.get('search', '')
        object_list = self.objects.all()
        if name:
            object_list = object_list.filter(name__icontains=name)
        return object_list


        return query



class AvailableView(ListView):
    model = Commodity
    template_name = 'omega/list.html'

class CommodityListViews(ListView):
    model = Commodity
    template_name = 'omega/list.html'


class CommodityDetailView(DetailView):
    model = Commodity
    template_name = 'omega/detail.html'


class CategoryView(ListView):
    model = Commodity
    template_name = 'omega/list.html'
    paginate_by = 12

    def get_queryset(self):
        queryset = Commodity.objects.filter(available=True, category=self.kwargs['name']).order_by('-updated')

        return queryset


class AvailableListView(ListView):
    model = Commodity
    template_name = 'omega/available1.html'
    paginate_by = 12

    def get_queryset(self):
        queryset = Commodity.objects.filter(available=True).order_by('-updated')

        return queryset

class CategoryListView(ListView):
    model = Category
    template_name = 'omega/summaries.html'


def unitlist(request, pk):
    category = Category.objects.get(pk=pk)
    object_list = Commodity.objects.filter(category=category, available=True)
    page = request.GET.get('page', 1)

    paginator = Paginator(object_list, 4)

    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)
    return render(request, 'omega/list.html', {'category': category, 'object_list': object_list})


def logout(request):
    auth.logout(request)
    return render(request,'omega/index.html')

#def user_details(request):
#    user = get_object_or_404(User, id=request.user.id)
#    return render(request, '', {'user': user})


def signu(request):
    if request.user.is_authenticated:
        messages.success(request, "You're already logged in.")
        return redirect('app:index')

    if request.method == 'POST':
        f = CreateUserForm(request.POST)
        p = PassGen(minlen=9, maxlen=10, minsc=1)
        word = p.generate()
        print('assign')
        print(word)
        if f.is_valid():
            f.save(password=word)
            print('saved')
            messages.success(request, f'Account created successfully. This is your new password: {word}')
            return redirect('omega:welcome')
    else:
        f = CreateUserForm()
    print('fail')
    return render(request, 'omega/r-signup.html', {'form': f})

def signup(request):
    if request.user.is_authenticated:
        messages.success(request, "You're already logged in.")
        return redirect('omega:index')
    if request.method == 'POST':
        p = PassGen(minlen=9, maxlen=10, minsc=1)
        word = p.generate()
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('first_name')
        password = word
        email = request.POST.get('email')
        try:
            b = User.objects.create_user(username=username, password=password, email=email, first_name=first_name,
                    last_name=last_name)
            b.save()
        except:
            messages.warning(request, 'This user already exists.')
            return redirect('omega:signup')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # correct username and password login the user
            auth.login(request, user)
            messages.success(request, f'Account created successfully. This is your new password: {word}')
            return redirect('omega:summary')
    else:
        f = CreateUserForm()
    print('fail')
    return render(request, 'omega/r-signup.html', {'form': f})

def login(request):
    f = LoginForm()
    if request.user.is_authenticated:
        return redirect('omega:summary')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email)[0]

        user = auth.authenticate(username=user.username, password=password)

        if user is not None:
            # correct username and password login the user
            auth.login(request, user)
            return redirect('omega:summary')

        else:
            messages.error(request, 'Error wrong username/password')

    return render(request, 'omega/r-login.html', {'form': f})

