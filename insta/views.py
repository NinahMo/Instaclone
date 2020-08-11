from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse
from .forms import PostForm
from .models import Post
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    RedirectView,
)
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.
class PostListView(ListView):
    template_name = "insta/post_list.html"
    queryset = Post.objects.all().filter(created_date__lte=timezone.now()).order_by('-created_date')
    context_object_name = 'posts'

class PostCreateView(CreateView):
    template_name = 'insta/post_create.html'
    form_class = PostForm
    queryset = Post.objects.all()
    success_url = '/'

    def form_valid(self, form):
        print(form.cleaned_data)
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostDetailView(DetailView):
    template_name = 'insta/post_detail.html'
    queryset = Post.objects.all().filter(created_date__lte=timezone.now())
    
    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Post, id=id_)

class PostUpdateView(UpdateView):
    template_name = 'insta/post_create.html'
    form_class = PostForm 

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Post, id=id_)

    def form_valid(self, form):
        form.instance.author = self.request.user 
        return super().form_valid(form) 

class PostDeleteView(DeleteView):
    template_name = 'insta/post_delete.html'

    def get_object(self):
        id_=self.kwargs.get("id")
        return get_object_or_404(Post, id=id_)

    def get_success_url(self):
        return reverse('insta:post_list')

def register(request):
    if request.method == 'POST':
        print("This shit is working bro.")
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            print(username,"This shit is working")
            messages.success(request, f'Account created for {username} successfully!')
            return redirect('/')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'users/profile.html')

class Profile(DetailView):
    template_name = 'users/profile.html'
    queryset = User.objects.all()
    success_url = '/'

    def get_object(self):
        id_ = self.kwargs.get("username")
        user = get_object_or_404(User, username=id_)
        return user 
        
    def get_context_data(self, *args, **kwargs):
        context = super(Profile,self).get_context_data(*args, **kwargs)
        user = self.get_object()
        context.update({
            'posts' : user.posts.all().filter(created_date__lte=timezone.now()).order_by('-created_date')
        })
        return context 
    def add_follow(self, request):
        user = self.get_object() 
        user.profile.followed_by.add(request.user.profile) 

def edit_profile(request):
    if request.method == "POST":

        user_form = UserUpdateForm(request.POST,instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, f'Your account has been updated successfully!')
            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'users/edit_profile.html', context)

def saved_posts(request):
    posts = Post.objects.filter(saved=True)
    context = {'saved_posts': posts}
    return render(request, 'insta/saved_posts.html', context) 

