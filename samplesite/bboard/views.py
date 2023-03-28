from django.shortcuts import render, get_list_or_404
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.views.generic.dates import ArchiveIndexView, MonthArchiveView

from .models import Bb, Rubric
from .forms import BbForm

def index(request):
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.all()
    context = {'bbs':bbs, 'rubrics': rubrics}
    return render(request, 'bboard/index.html', context=context) 

def by_rubric(request, rubric_id):
    bbs = get_list_or_404(Bb, rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {'bbs':bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
    return render(request, 'bboard/by_rubric.html', context)

@require_http_methods(['GET','POST'])
def add(request):
    bbf = BbForm()
    context = {'form': bbf}
    return render(request, 'bboard/create.html', context)

def add_save(request):
    bbf = BbForm(request.POST)
    if bbf.is_valid():
        bbf.save()
        return HttpResponseRedirect(reverse('by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
    else:
        context = {'form': bbf}
        return render(request, 'bboard/create.html', context)

def add_and_save(request):
    if request.method == 'POST':
        if bbf.is_valid():
            bbf.save()
            return HttpResponseRedirect(reverse('by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
        else:   
            context = {'form': bbf}
            return render(request, 'bboard/create.html', context)
    else:
        bbf = BbForm()
        context = {'form': bbf}
        return render(request, 'bboard/create.html', context)


class BbCreateView(CreateView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

class BbByRubricView(TemplateView):
    template_name = 'bboard/by_rubrick.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bbs'] = Bb.objects.filter(rubric=context['rubric_id'])
        context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = Rubric.objects.get(pk=context['rubric_id'])
        return context

class BbDetailView(DetailView):
    model = Bb

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

class BbByRubricView(ListView, SingleObjectMixin):
    template_name = 'bboard/by_rubric.html'
    pk_url_kwarg = 'rubric_id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Rubric.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.object.bb_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = self.object 
        context['bbs'] = context['object_list']
        return context

class BbAddView(FormView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    initial = {'prioce': 0.0}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

    def form_valid(self,form):
        form.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        self.object = super().get_form(form_class)
        return self.object

    def get_success_url(self):
        return reverse('bboard:by_rubric', kwargs={'rubric_id': self.object.cleaned_data['rubric'].pk})

class BbEditView(UpdateView):
    model = Bb
    form_class = BbForm
    success_url = '/'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

class BbDeleteView(DeleteView):
   model = Bb
   success_url = '/'

   def get_context_data(self, *args, **kwargs):
       context = super().get_context_data(*args, **kwargs)
       context['rubrics'] = Rubric.objects.all()
       return context

class BbIndexView(ArchiveIndexView):
    model = Bb
    date_field = 'published'
    date_list_period = 'year'
    template_name = 'bboard/index.html'
    context_object_name = 'bbs'
    allow_empty = True

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

class BbMonthArchiveView(MonthArchiveView):
    model = Bb
    date_field = 'published'
    month_format = '%m'

class BbRedirectView(RedirectView):
    url = '/detail/%(pk)d/'
