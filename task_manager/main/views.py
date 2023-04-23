from django.shortcuts import render
# from django.utils.translation import gettext as _
from django.views.generic.base import View
# Create your views here.


class IndexViews(View):

    def get(self, request, *args, **kwargs):
        # output = (_('title'),
        #           _('users'),
        #           _('enter'),
        #           _('registration'),
        #           _('WelcomeMessages'),
        #           _('LeadMessage'),
        #           _('KnowMore'),
        #           )
        return render(request, 'main/index.html')
