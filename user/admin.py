from django.contrib import admin
from django.contrib.auth import get_user_model
user = get_user_model()
from listings.extras import delete_realtor_listings_data

class UserAdmin(admin.ModelAdmin):
    using = 'users'
    list_display = ('id', 'name', 'email')
    list_display_links = ('id', 'email', 'name')
    search_fields = ('name','email')
    list_per_page = 25

    def save_model(self, request, obj, form, change):
        obj.save(using=self.using)
        

    def delete_model(self, request, obj):
        email = obj.email
        obj.delete(using=self.using)
        delete_realtor_listings_data(email)
        
    def get_queryset(self, request):
        return super().get_queryset(request).using(self.using)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)
    
