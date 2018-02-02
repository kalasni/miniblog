from django.contrib import admin
from .models import Post

# Register the Admin classes for Post using the decorator
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish',
                            'status')

    # Fields in the right side bar
    list_filter =('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body') # Search bar

    #Prepopulate the slug field with the input of the title field attribute.
    prepopulated_fields = {'slug': ('title',)}

    # Author field is displayed with a lookup widget
    raw_id_fields = ('author',)

    # Bar below the search bar
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']




#admin.site.register(Post)
