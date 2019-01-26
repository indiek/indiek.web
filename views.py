from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import (
        ListView, 
        DetailView, 
        CreateView,
        UpdateView,
        DeleteView
        )
from .models import dbItem, dbTopic


@login_required
def home(request):
    context = {'author': request.user,
            'page_title': 'User Home'}
    return render(request, 'indiek_web/home.html', context)


class ItemListView(ListView):
    model = dbItem
    template_name = ''
    context_object_name = ''
    ordering = ['-date_created']
    paginate_by = 5


class TopicListView(ListView):
    model = dbTopic
    template_name = ''
    context_object_name = ''
    ordering = ['-date_created']
    paginate_by = 5


class UserItemListView(ListView):
    model = dbItem
    template_name = 'indiek_web/user_items.html'
    context_object_name = 'items'
    paginate_by = 5
    page_title = 'Your Items'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['page_title'] = self.page_title
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return dbItem.objects.filter(author=user).order_by('-date_created')


class UserTopicListView(ListView):
    model = dbTopic
    template_name = 'indiek_web/user_topics.html'
    context_object_name = 'topics'
    paginate_by = 5
    page_title = 'Your Topics'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['page_title'] = self.page_title
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return dbTopic.objects.filter(author=user).order_by('-date_created')


# note, for the class below, Django by default looks for 
# a template with name <app>/<model>_<view_type>.html
# but I decided to override it with template_name attribute
class ItemDetailView(DetailView):
    model = dbItem
    template_name = 'indiek_web/item_detail.html'
#    context_object_name = 'item'
    page_title = 'Item Details'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['page_title'] = self.page_title
        return context


class TopicDetailView(DetailView):
    model = dbTopic
    template_name = 'indiek_web/topic_detail.html'
#    context_object_name = 'topic'
    page_title = 'Topic Details'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['page_title'] = self.page_title
        return context


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = dbItem
    fields = ['quickname', 'description', 'item_url']
    page_title = 'Create Item'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['page_title'] = self.page_title
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TopicCreateView(LoginRequiredMixin, CreateView):
    model = dbTopic
    fields = ['name', 'description']
    page_title = 'Create Topic'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['page_title'] = self.page_title
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = dbItem
    fields = ['quickname', 'description', 'item_url']
    page_title = 'Update Item'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['page_title'] = self.page_title
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class TopicUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = dbTopic
    fields = ['name', 'description']
    page_title = 'Update Topic'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['page_title'] = self.page_title
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    
    model = dbItem
    success_url = '/'  # this redirects to home page on deletion of item
    page_title = 'Delete Item'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['page_title'] = self.page_title
        return context

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class TopicDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    
    model = dbTopic
    success_url = '/'  # this redirects to home page on deletion of topic
    page_title = 'Delete Topic'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['page_title'] = self.page_title
        return context

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
