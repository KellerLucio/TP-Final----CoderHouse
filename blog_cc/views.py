from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from blog_cc.models import Post, Profile, Mensaje
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def about(request):
    return render(request, "blog_cc/about.html")

def index(request):
    context = {
        "posts": Post.objects.all()
    }
    return render(request, "blog_cc/index.html", context)

class PostList(ListView):
    model = Post
    context_object_name = "posts"

class PostDetail(DetailView):
    model = Post
    
class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    success_url = reverse_lazy("post-list")
    fields = ['carousel_caption_title','carousel_caption_description',
                'heading','description','imagen']


    def form_valid(self, form):
        form.instance.publisher = self.request.user
        return super().form_valid(form)

class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    success_url = reverse_lazy("post-list")
    fields = '__all__'

    def test_func(self):
        user_id = self.request.user.id
        post_id = self.kwargs.get('pk')
        return Post.objects.filter(publisher=user_id, id=post_id).exists()

    def handle_no_permission(self):
        return render(self.request, "blog_cc/not_found.html")

class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("post-list")

    def test_func(self):
        user_id = self.request.user.id
        post_id = self.kwargs.get('pk')
        return Post.objects.filter(publisher=user_id, id=post_id).exists()

    def handle_no_permission(self):
        return render(self.request, "blog_cc/not_found.html")


class SignUp(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('post-list')


class Login(LoginView):
    next_page = reverse_lazy("post-list")

class Logout(LogoutView):
    template_name = 'registration/logout.html'
    
#-------------------------------------------------------------------------------------------------
class ProfileCreate(CreateView):
    model = Profile
    fields = ['instagram', 'imagen']

    def form_valid(self, form):
        # comprobar si ya existe un perfil para este usuario
        if hasattr(self.request.user, 'profile'):
            # actualizar el perfil existente
            profile = self.request.user.profile
            profile.instagram = form.cleaned_data['instagram']
            profile.imagen = form.cleaned_data['imagen']
            profile.save()
        else:
            # crear un nuevo perfil
            form.instance.user = self.request.user
            return super().form_valid(form)
    success_url = reverse_lazy("index")

class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['instagram', 'imagen']
#-------------------------------------------------------------------------------------------------


class MensajeCreate(CreateView):
    model = Mensaje
    fields = '__all__'
    success_url = reverse_lazy("post-list")


class  MensajeList(LoginRequiredMixin, ListView):
    model = Mensaje
    context_object_name = "mensajes"
    
    def get_queryset(self):
        return Mensaje.objects.filter(destinatario=self.request.user.id).all()
    

class MensajeDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model= Mensaje
    success_url = reverse_lazy("mensaje-list")

    def test_func(self):
        user_id = self.request.user.id
        mensaje_id = self.kwargs.get('pk')
        return Mensaje.objects.filter(destinatario=user_id).exists()