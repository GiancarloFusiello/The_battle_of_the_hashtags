from django.contrib import admin

from battles.forms import BattleAdmin
from .models import Battle

admin.site.register(Battle, BattleAdmin)
