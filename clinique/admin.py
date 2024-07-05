from django.contrib import admin

from clinique.models import Member

# Register your models here.
class MemberAdmin(admin.ModelAdmin):
    list_display="firstname","lastname"

admin.site.register(Member,MemberAdmin)
# Register your models here.