# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from zero.views import lists, edit, details

urlpatterns = patterns('',
                       url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'grains2/login.html'}, name='login'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
                       # Dashboard
                       url(r'^dashboard/(?P<model>issue|comment)/$', lists.Dashboard.as_view(), name='dashboard'),
                       # Issue
                       url(r'^issue/(?P<pk>\d+)/$', details.IssueView.as_view(), name="issue_details"),
                       url(r'^issues/$', lists.FilteredIssuesView.as_view(), name="filtered_issues"),
                       url(r'^issue/(?P<issue_id>\d+)/comments/create/$', edit.CreateIssueCommentView.as_view(), name="create_issue_comment"),
                       url(r'^comment/(?P<pk>\d+)/edit/$', edit.UpdateCommentView.as_view(), name="edit_comment"),
                       url(r'^issue/(?P<issue_id>\d+)/tasks/create/$', edit.CreateTaskView.as_view(), name="create_task"),
                       url(r'^task/(?P<pk>\d+)/edit/$', edit.UpdateTaskView.as_view(), name="edit_task"),
                       # TASK
                       url(r'^tasks/(?P<status>open|closed)/$', lists.TasksView.as_view(), name='list_tasks'),
                       url(r'^calendar/$', lists.CalendarView.as_view(), name='calendar'),
                       url(r'^json-events/$', lists.JSONEventsView.as_view(), name='json_events'),
                       url(r'^create-deadline/(?P<model>task|issue)/(?P<pk>\d+)/$', edit.CreateDeadlineView.as_view(), name='create_deadline'),
                       url(r'^update-deadline/(?P<model>task|issue)/(?P<pk>\d+)/$', edit.UpdateDeadlineView.as_view(), name='update_deadline'),
                       # Generic handlers
                       url(r'^delete/(?P<model>.+)/(?P<pk>\d+)/$', edit.DeleteObjectView.as_view(), name="delete_object"),
)

