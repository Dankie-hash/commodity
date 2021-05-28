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

def list2(request):

    return render(request, 'omega/list2.html')

def list3(request):

    return render(request, 'omega/list3.html')

def list4(request):

    return render(request, 'omega/list4.html')

def available(request):

    return render(request, 'omega/available1.html')

def admin(request):

    return render(request, 'omega/upload.html')

def detail(request):

    return render(request, 'omega/detail.html')





def upload(request):

    return render(request, 'omega/admin.html')



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

class CommodityCreateView(CreateView):
    model = Commodity
    template_name = 'omega/list.html'



class CategoryCreateView(CreateView):
    model = Commodity
    template_name = 'omega/list.html'



class AvailableView(ListView):
    model = Commodity
    template_name = 'omega/list.html'


class CommodityDetailView(DetailView):
    model = Commodity
    template_name = 'omega/list.html'


class CategoryListView(ListView):
    model = Commodity
    template_name = 'omega/list.html'
    paginate_by = 12

    def get_queryset(self):
        queryset = Commodity.objects.filter(available=True, category=self.kwargs['name']).order_by('-updated')

        return queryset


class AvailableListView(ListView):
    model = Commodity
    template_name = 'omega/available.html'
    paginate_by = 12

    def get_queryset(self):
        queryset = Commodity.objects.filter(available=True).order_by('-updated')

        return queryset



@login_required
def logout(request):
    auth.logout(request)
    return render(request,'omega/publix.html')

#def user_details(request):
#    user = get_object_or_404(User, id=request.user.id)
#    return render(request, '', {'user': user})


def signup(request):
    if request.user.is_authenticated:
        messages.success(request, "You're already logged in.")
        return redirect('app:index')

    if request.method == 'POST':
        f = CreateUserForm(request.POST)
        if f.is_valid():
            f.save()

            messages.success(request, 'Account created successfully. This is your new password:')
            return redirect('login')
    else:
        f = CreateUserForm()
    return render(request, 'omega/r-signup.html', {'form': f})


def login(request):
    f = LoginForm()
    if request.user.is_authenticated:
        return redirect('omega:index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # correct username and password login the user
            auth.login(request, user)
            return redirect('omega:index')

        else:
            messages.error(request, 'Error wrong username/password')

    return render(request, 'omega/r-login.html', {'form':f})

