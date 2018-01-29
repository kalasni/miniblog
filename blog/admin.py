from django.contrib import admin
from .models import Post

# Register the Admin classes for Post using the decorator
@admin.register(Post)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish',
                            'status')

#admin.site.register(Post)
