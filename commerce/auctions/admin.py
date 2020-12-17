from django.contrib import admin
from .models import CreateList, ItemCategory, User, BidItem

# Register your models here.
admin.site.register(CreateList)
admin.site.register(ItemCategory)
admin.site.register(User)
admin.site.register(BidItem)