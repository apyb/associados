# encoding: utf-8
from django.template import RequestContext
from django.utils.translation import ugettext, ugettext_lazy as _

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response

from forms import RegisterForm

from django.contrib import messages


def home(request):
    return render(request,
        'home.html',
            {
            })


def register(request):
    if request.method == 'POST':
        #data = request.POST.copy()  # so we can manipulate data
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, _('You have been registered. Welcome !'))
            return HttpResponseRedirect(reverse('user-register-done'))

    else:
        form = RegisterForm()

    return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))
