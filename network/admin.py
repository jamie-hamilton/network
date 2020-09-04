from django.contrib import admin
# import model here

# Register your models here.

"""
# Example of customising admin view:
class UserProfileAdmin(admin.ModelAdmin):
    # Display these columns
    list_display = ["user", "user_info", "city"]

    # Renaming an admin column from desc to user_info:
    def user_info(self, obj):
        return obj.desc

# Register models:
admin.site.register(User, UserProfile)
"""