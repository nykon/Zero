# -*- coding: utf-8 -*-
from django.views.generic import CreateView, UpdateView, DeleteView, FormView, View
from django.db.models import get_model
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django import  forms
from django.template.defaultfilters import slugify
import datetime

from zero.tools.tools import RegionViewMixin
#from synergy.templates.regions.views import RegionViewMixin

       
class CreateIssueCommentView(RegionViewMixin, CreateView):
        
    def get_success_url(self):
        return reverse('issue_details', args=[self.kwargs.get('issue_id')])
     
    def get_form_class(cls):
        class IssueForm(forms.ModelForm):
            class Meta:
                model = get_model('zero','Comment')
                exclude = ( 'issue',)
        return IssueForm

    def get_initial(self):
        return {'status': self.get_issue().get_current_status(), 'priority': self.get_issue().get_current_status()}

    def get_issue(self):
        return get_model("zero", "issue").objects.get(id=self.kwargs.get('issue_id'))

    def get_context_data(self, *args, **kwargs):
        ctx = super(CreateIssueCommentView, self).get_context_data(*args, **kwargs)
        issue = self.get_issue()
        ctx['title'] = "Comment for %s" % issue
        ctx['navlinks'] = {'X': reverse('list_x_issues', args=[issue.x.id]),
                           'Issue': reverse('issue_details', args=[issue.id]),
                           }

        return ctx

    def form_valid(self, form):
        
        self.object = form.save(commit = False)
        self.object.issue_id = self.kwargs.get('issue_id')
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
        #return super(CreateIssueCommentView, self).form_valid(form)


class UpdateCommentView(RegionViewMixin, UpdateView):
    """ Handle x issue updates. """
    model = get_model('zero', 'Comment')

    def get_success_url(self):
        return reverse('issue_details', args=[self.object.issue.id])
     
    def get_form_class(cls):
        class IssueForm(forms.ModelForm):
            class Meta:
                model = get_model('zero','Comment')
                exclude = ('issue', )
        return IssueForm

    def get_context_data(self, *args, **kwargs):
        ctx = super(UpdateCommentView, self).get_context_data(*args, **kwargs)
        ctx['title'] = "Comment for %s" % self.get_object().issue
        ctx['navlinks'] = {'Issue': reverse('issue_details', args=[self.get_object().issue.id]),
                           }

        return ctx


class CreateTaskView(RegionViewMixin, CreateView):
    #model = get_model('zero','Issue')
    #form_class = get_form()
        
    def get_success_url(self):
        return reverse('issue_details', args=[self.kwargs.get('issue_id')])

    def get_initial(self):
        return {'asignee': self.request.user}
     
    def get_form_class(cls):
        class IssueForm(forms.ModelForm):
            class Meta:
                model = get_model('zero', 'Task')
                exclude = ( 'issue',)
        return IssueForm

    def get_issue(self):
        return get_model("zero", "issue").objects.get(id=self.kwargs.get('issue_id'))
        
    def form_valid(self, form):
        
        self.object = form.save(commit = False)
        self.object.issue_id=self.kwargs.get('issue_id')
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


    def get_context_data(self, *args, **kwargs):
        ctx = super(CreateTaskView, self).get_context_data(*args, **kwargs)
        ctx['title'] = "Task for for %s" % self.get_issue()
        ctx['navlinks'] = {'Issue': reverse('issue_details', args=[self.get_issue().id]),
                           }

        return ctx

class UpdateTaskView(RegionViewMixin, UpdateView):
    """ Handle x issue updates. """
    model = get_model('zero', 'Task')

    def get_success_url(self):
        return reverse('issue_details', args=[self.object.issue.id])
     
    def get_form_class(cls):
        class IssueForm(forms.ModelForm):
            class Meta:
                model = get_model('zero','Task')
                exclude = ('issue', )
        return IssueForm

    def get_context_data(self, *args, **kwargs):
        ctx = super(UpdateTaskView, self).get_context_data(*args, **kwargs)
        ctx['title'] = "Update task %s" % self.get_object()
        ctx['navlinks'] = {'Issue': reverse('issue_details', args=[self.get_object().issue.id]),
                           }

        return ctx


class DeleteObjectView(DeleteView):
    template_name = 'zero/edit/confirm_delete.html'

    def get_queryset(self):
        """
        Get the queryset to look an object up against. May not be called if
        `get_object` is overridden.
        """
        self.model = get_model('contenttypes','ContentType').objects.get(model=self.kwargs.get('model')).model_class()
        return super(DeleteView, self).get_queryset()

    def get_success_url(self):
        reverse_names = {'issue': ('list_x_issues', 'x_id'),
                         'comment': ('issue_details', 'issue_id'),
                         'task': ('issue_details', 'issue_id'),
                         'x': ('list_xs', None)
                         }
        if reverse_names[self.kwargs.get('model')][1]:
            attr = getattr(self.object, reverse_names[self.kwargs.get('model')][1])
            return reverse(reverse_names[self.kwargs.get('model')][0], args=[attr])
        return reverse(reverse_names[self.kwargs.get('model')][0])


    def get_context_data(self, **kwargs):
        context = super(DeleteObjectView, self).get_context_data(**kwargs)

        # Templete is provided with the URL that should be used if the user wants to
        # cancel the delete decision.
        # -----------------
        
        reverse_names = {'issue': ('issue_details', 'id'),
                         'comment': ('issue_details', 'issue_id'),
                         'x': ('list_x_issues', 'id'),
                         'task': ('issue_details', 'issue_id'),
                         }
        attr = getattr(self.object, reverse_names[self.kwargs.get('model')][1])
        context['cancel_url'] = reverse(reverse_names[self.kwargs.get('model')][0], args=[attr])

        return context


class CreateDeadlineView(View):
    def post(self, request, *args, **kwargs):
        obj = get_model('zero', self.kwargs.get('model')).objects.get(id=self.kwargs.get('pk'))
        obj.due_date = datetime.date(int(request.POST.get('year')), int(request.POST.get('month')), int(request.POST.get('day')))
        #obj.due_time = datetime.time(int(request.POST.get('year')), int(request.POST.get('month')), int(request.POST.get('day')))
        obj.save()
        
        return HttpResponse()

class UpdateDeadlineView(View):
    def post(self, request, *args, **kwargs):
        obj = get_model('zero', self.kwargs.get('model')).objects.get(id=self.kwargs.get('pk'))
        obj.due_date += datetime.timedelta(days=int(request.POST.get('days')))


        minutes = int(request.POST.get('minutes'))
        if minutes:
            year = obj.due_date.year
            month = obj.due_date.month
            day = obj.due_date.day
            if obj.due_time:
                hour = obj.due_time.hour
                minute = obj.due_time.minute
            else:
                hour = 0
                minute = 0
            dt = datetime.datetime(year, month, day, hour, minute) + datetime.timedelta(minutes=minutes)
            obj.due_time = dt.time()


        duration =  int(request.POST.get('duration_minutes'))
        if duration:
            if obj.time_spent:
                obj.time_spent += duration
            else:
                obj.time_spent = duration

        
        if request.POST.get('all_day') == 'true':
            obj.due_time = None
        obj.save()
        return HttpResponse()

