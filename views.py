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
from .forms import ItemForm

@login_required
def home(request):
    context = {'author': request.user,
            'page_title': 'ik - User Home'}
    return render(request, 'indiek_web/home.html', context)


class UserItemListView(LoginRequiredMixin, ListView):
    model = dbItem
    template_name = 'indiek_web/user_items.html'
    context_object_name = 'items'
    paginate_by = 5
    page_title = 'ik - Your Items'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return dbItem.objects.filter(author=user).order_by('-last_modified')


class UserTopicListView(LoginRequiredMixin, ListView):
    model = dbTopic
    template_name = 'indiek_web/user_topics.html'
    context_object_name = 'topics'
    paginate_by = 5
    page_title = 'ik - Your Topics'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return dbTopic.objects.filter(author=user).order_by('-last_modified')


# note, for the class below, Django by default looks for 
# a template with name <app>/<model>_<view_type>.html
# but I decided to override it with template_name attribute
class ItemDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = dbItem
    template_name = 'indiek_web/item_detail.html'
    page_title = 'ik - Item Details'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

    def test_func(self):
        dbitem = self.get_object()
        if self.request.user == dbitem.author:
            return True
        return False


class TopicDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = dbTopic
    template_name = 'indiek_web/topic_detail.html'
    page_title = 'ik - Topic Details'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

    def test_func(self):
        dbtopic = self.get_object()
        if self.request.user == dbtopic.author:
            return True
        return False


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = dbItem
#    fields = ['quickname', 'description', 'item_url', 'topics']
    page_title = 'ik - Create Item'
    form_class = ItemForm
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        # todo: Here check that requested topics are admissible
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ItemCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class TopicCreateView(LoginRequiredMixin, CreateView):
    model = dbTopic
    fields = ['name', 'description']
    page_title = 'ik - Create Topic'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = dbItem
#    fields = ['quickname', 'description', 'item_url', 'topics']
    page_title = 'ik - Update Item'
    form_class = ItemForm

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        # todo: Here check that requested topics are admissible
        return super().form_valid(form)

    def test_func(self):
        dbitem = self.get_object()
        if self.request.user == dbitem.author:
            return True
        return False
    
    def get_form_kwargs(self):
        kwargs = super(ItemUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class TopicUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = dbTopic
    fields = ['name', 'description']
    page_title = 'ik - Update Topic'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        dbtopic = self.get_object()
        if self.request.user == dbtopic.author:
            return True
        return False


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    
    model = dbItem
    success_url = '/'  # todo: is this okay? Should I rather do success_url = reverse_lazy('user-home')?
    page_title = 'ik - Delete Item'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

    def test_func(self):
        dbitem = self.get_object()
        if self.request.user == dbitem.author:
            return True
        return False


class TopicDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    
    model = dbTopic
    success_url = '/'  # todo: is this ok?
    page_title = 'ik - Delete Topic'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

    def test_func(self):
        dbtopic = self.get_object()
        if self.request.user == dbtopic.author:
            return True
        return False
