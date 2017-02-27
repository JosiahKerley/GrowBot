import os
from django.http import request
from django.conf import settings
from django.template import loader
from django.core.files import File
from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect, HttpResponse


## Growbot
import growbot
from growbot.api.models import *



class DashboardView(TemplateView):
  template_name = 'dashboard/base.html'
  success_url = '/dashboard/'

  def get_context_data(self, **kwargs):
    context = super(DashboardView, self).get_context_data(**kwargs)
    context['outlets'] = PowerOutlet.objects.all()
    context['snapshots'] = CameraSnapshot.objects.all()
    return(context)

  def post(self, request, *args, **kwargs):
    context = self.get_context_data()
    current = []
    present = []
    for outlet in PowerOutlet.objects.all():
      current.append(outlet.name)
    for name in request.POST:
      if name in current:
        present.append(name)
    #print(set(present) ^ set(current))
    for switch in current:
      outlet = PowerOutlet.objects.filter(name=switch)
      if switch in present:
        print 'turning {} on'.format(switch)
        for i in outlet:
          i.state = True
      else:
        print 'turning {} off'.format(switch)
        for i in outlet:
          i.state = False
      for i in outlet:
        i.save()

    #   switches = PowerOutlet.objects.filter(name=name)
    #   for switch in switches:
    #     switch.state = not switch.state
    #     switch.save()
    return super(TemplateView, self).render_to_response(context)



