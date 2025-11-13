from django.contrib import admin

from test_app.models import Book, Post, UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'nickname',
        'age',
        'followers_count',
        'posts_count',
        'comments_count',
        'engagement_rate'
    )
    list_filter = (
        'age',
        'posts_count',
        'engagement_rate'
    )
    search_fields = (
        'nickname',
        'age'
    )

# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     list_display = (
#         'title',
#         'created_at'
#      )
#     list_filter = (
#         'created_at'
#     )
#     search_fields = (
#         'title'
#     )


admin.site.register(Book)
admin.site.register(Post)
admin.site.register(UserProfile, UserProfileAdmin)