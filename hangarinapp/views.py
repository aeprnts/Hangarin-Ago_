from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q 
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task, Priority, Category, Note, SubTask
from .forms import TaskForm, PriorityForm, CategoryForm, NoteForm, SubTaskForm

class HomePageView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'hangarinapp'
    template_name = "home.html"
    login_url = '/accounts/login/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_tasks'] = Task.objects.count()
        context['pending_count'] = Task.objects.filter(status='Pending').count()
        context['inprogress_count'] = Task.objects.filter(status='In Progress').count()
        context['completed_count'] = Task.objects.filter(status='Completed').count()
        context['total_categories'] = Category.objects.count()
        context['total_priorities'] = Priority.objects.count()
        context['total_notes'] = Note.objects.count()
        context['recent_tasks'] = Task.objects.all().order_by('-id')[:5]
        return context

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'object_list'
    template_name = 'task_list.html'
    paginate_by = 5
    login_url = '/accounts/login/'
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related('category', 'priority')
        
        query = self.request.GET.get('q')
        sort_by = self.request.GET.get('sort_by')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(status__icontains=query) |
                Q(category__name__icontains=query) |
                Q(priority__name__icontains=query)
            )

        allowed_sorts = {
            'title': 'title',
            '-created_at': '-id',
            'deadline': 'deadline',
            'status': 'status',
            'priority__name': 'priority__name'
        }
        
        order_field = allowed_sorts.get(sort_by, '-id')
        return queryset.order_by(order_field)

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')
    login_url = '/accounts/login/'

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')
    login_url = '/accounts/login/'

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task_del.html'
    success_url = reverse_lazy('task-list')
    login_url = '/accounts/login/'

class PriorityList(LoginRequiredMixin, ListView):
    model = Priority
    context_object_name = 'priorities'
    template_name = 'priority_list.html'
    paginate_by = 5
    login_url = '/accounts/login/'
    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-id')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(name__icontains=query))
        return queryset

class PriorityCreateView(LoginRequiredMixin, CreateView):
    model = Priority
    form_class = PriorityForm
    template_name = 'priority_form.html'
    success_url = reverse_lazy('priority-list')
    login_url = '/accounts/login/'

class PriorityUpdateView(LoginRequiredMixin, UpdateView):
    model = Priority
    form_class = PriorityForm
    template_name = 'priority_form.html'
    success_url = reverse_lazy('priority-list')
    login_url = '/accounts/login/'

class PriorityDeleteView(LoginRequiredMixin, DeleteView):
    model = Priority
    template_name = 'priority_del.html'
    success_url = reverse_lazy('priority-list')
    login_url = '/accounts/login/'

class CategoryList(LoginRequiredMixin, ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'category_list.html'
    paginate_by = 5
    login_url = '/accounts/login/'
    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-id')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(name__icontains=query))
        return queryset

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_form.html'
    success_url = reverse_lazy('category-list')
    login_url = '/accounts/login/'

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_form.html'
    success_url = reverse_lazy('category-list')
    login_url = '/accounts/login/'

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'category_del.html'
    success_url = reverse_lazy('category-list')
    login_url = '/accounts/login/'

class NoteList(LoginRequiredMixin, ListView):
    model = Note
    context_object_name = 'notes'
    template_name = 'note_list.html'
    paginate_by = 10
    login_url = '/accounts/login/'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-id')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(content__icontains=query) | 
                Q(task__title__icontains=query)
            )
        return queryset

class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('note-list')
    login_url = '/accounts/login/'

class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('note-list')
    login_url = '/accounts/login/'

class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'note_del.html'
    success_url = reverse_lazy('note-list')
    login_url = '/accounts/login/'

class SubTaskList(LoginRequiredMixin, ListView):
    model = SubTask
    context_object_name = 'subtasks'
    template_name = 'subtask_list.html'
    paginate_by = 10
    login_url = '/accounts/login/'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-id')
        status_filter = self.request.GET.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset

class SubTaskCreateView(LoginRequiredMixin, CreateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = 'subtask_form.html'
    success_url = reverse_lazy('subtask-list')
    login_url = '/accounts/login/'

class SubTaskUpdateView(LoginRequiredMixin, UpdateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = 'subtask_form.html'
    success_url = reverse_lazy('subtask-list')
    login_url = '/accounts/login/'

class SubTaskDeleteView(LoginRequiredMixin, DeleteView):
    model = SubTask
    template_name = 'subtask_del.html'
    success_url = reverse_lazy('subtask-list')
    login_url = '/accounts/login/'