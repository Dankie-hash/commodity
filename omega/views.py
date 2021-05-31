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
from django.views.generic import FormView
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

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

def profile(request):

    return render(request, 'omega/profile.html')




def update(request):
    if request.method == 'POST':
        f = UserProfileForm(request.POST, instance=request.user)
        if f.is_valid():
            f.save()
            messages.success(request,'Your Profile has been updated!')
            return redirect('omega:profile')
    else:
        f = UserProfileForm(instance=request.user)

    context={'form': f}
    return render(request, 'omega/r-update.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message, 'sf.rodneydlamini@gmail.com', ['sf.bbb@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("omega:summary")

    form = ContactForm()
    return render(request, "omega/communication.html", {'form': form})

def my_mail(request):
    subject = "Greetings from Programink"
    msg     = "Learn Django at Programink.com"
    to      = "hello@programink.com"
    res     = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
    if(res == 1):
        msg = "Mail Sent Successfully."
    else:
        msg = "Mail Sending Failed."
    return HttpResponse(msg)

def profile(request):

    return render(request, 'omega/profile.html')


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
    template_name = 'omega/search.html'
    paginate_by = 12

    def get_queryset(self):
        name = self.kwargs.get('search', '')
        object_list = Commodity.objects.all()
        if name:
            object_list = object_list.filter(name__icontains=name)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.kwargs.get('search', '')
        return context


def search(request):
    post_list = []
    try:
        query = request.GET.get('search')
    except:
        query = ''
    if query:
        post_list = Commodity.objects.filter(name__icontains=query)

    page = request.GET.get('page', 1)
    paginator = Paginator(post_list, 10)
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)



    return render(request, 'omega/search.html', {'object_list': object_list, 'query': query})

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
            messages.warning(request, 'This user is already registered.')
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


def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get('email')
        associated_users = User.objects.filter(email=email)
        if associated_users.exists():
            for user in associated_users:
                subject = "Password Reset Requested"
                email_template_name = "omega/password/password_reset_email.txt"
                c = {
                    "email": user.email,
                    'domain': '127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                }
                email = render_to_string(email_template_name, c)
                try:
                    send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                except BadHeaderError:

                    return HttpResponse('Invalid header found.')

                messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                return redirect("omega:index")
            messages.error(request, 'An invalid email has been entered.')

    return render(request=request, template_name="main/r-forgot.html",
                  context={"form": 'form'})

