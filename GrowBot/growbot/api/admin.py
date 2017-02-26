from django.contrib import admin
from solo.admin import SingletonModelAdmin
from config.models import *

admin.site.register(SiteConfiguration, SingletonModelAdmin)

# There is only one item in the table, you can get it this way:
from .models import SiteConfiguration
config = SiteConfiguration.objects.get()

# get_solo will create the item if it does not already exist
config = SiteConfiguration.get_solo()


