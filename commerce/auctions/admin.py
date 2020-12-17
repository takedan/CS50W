from django.contrib import admin
from .models import CreateList, ItemCategory, User, BidItem, ItemActive, Watchlist

# Register your models here.
class WatchlistAdmin(admin.ModelAdmin):
  filter_horizontal = ("items", )


admin.site.register(CreateList)
admin.site.register(ItemCategory)
admin.site.register(User)
admin.site.register(BidItem)
admin.site.register(ItemActive)
admin.site.register(Watchlist, WatchlistAdmin)

