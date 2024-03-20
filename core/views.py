from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Post

# Create your views here.
class HomeView(ListView):
            template_name = 'core/home.html'
            queryset = Post.objects.all()
            paginate_by = 2

class PostView(DetailView):
        model = Post
        template_name = 'core/post.html'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            # since our slug field is not unique, we need the primary key to get a unique post
            pk = self.kwargs['pk']
            slug = self.kwargs['slug']

            post = get_object_or_404(Post, pk=pk, slug=slug)
            context['post'] = post
            return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content", "image", "tags"]

    def get_success_url(self):
        messages.success(
            self.request, 'Your post has been created successfully.')
        return reverse_lazy("core:home")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.slug = slugify(form.cleaned_data['title'])
        obj.save()
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ["title", "content", "image", "tags"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        update = True
        context['update'] = update

        return context

    def get_success_url(self):
        messages.success(
            self.request, 'Your post has been updated successfully.')
        return reverse_lazy("core:home")

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post

    def get_success_url(self):
        messages.success(
            self.request, 'Your post has been deleted successfully.')
        return reverse_lazy("core:home")

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)
