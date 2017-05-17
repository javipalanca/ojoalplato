import floppyforms
from django.contrib import admin
from django import forms
from redactor.widgets import RedactorEditor

from reversion.admin import VersionAdmin

from .models import Post, PostMeta, Comment, Term, Taxonomy

from django.contrib.admin import site
import adminactions.actions as actions

# register all adminactions
actions.add_to_site(site)


class PostMetaAdmin(admin.TabularInline):
    model = PostMeta


class ImageThumbnailFileInput(floppyforms.ClearableFileInput):
    template_name = 'image_thumbnail.html'


class PostChangeForm(forms.ModelForm):
    class Meta:
        model = Post
        widgets = {
            'content': RedactorEditor(),
            'image_header': ImageThumbnailFileInput,
        }
        fields = '__all__'


@admin.register(Post)
class PostAdmin(VersionAdmin):
    form = PostChangeForm
    save_on_top = True
    list_filter = ['status']
    list_display = ['title', 'author', 'post_date', 'status']
    ordering = ('-post_date',)
    advanced_options = ['guid', 'post_type', 'excerpt', 'content_filtered',
                        'comment_status', 'comment_count', 'ping_status', 'to_ping', 'pinged',
                        'password', 'parent_id', 'menu_order', 'mime_type']
    fieldsets = (
        (None, {
            'fields': ('status', 'title', 'author', 'tags', 'category', 'post_date',
                       'restaurant_card', 'wine_card', 'recipe_card',
                       'image_header', 'content', 'notified', 'notification_delay',
                       'post_to_facebook', 'post_to_twitter')
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            self.inlines = [PostMetaAdmin]
            self.fieldsets = (self.fieldsets[0],
                              ('Opciones avanzadas', {
                                  'classes': ('collapse',),
                                  'fields': tuple(self.advanced_options),
                              }),
                              )
        return super(PostAdmin, self).get_form(request, obj, **kwargs)

    class Media:
        css = {
             'all': ('wpfamily/style_admin.css',)
        }


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_filter = ['comment_type', 'author_name']


@admin.register(Term)
class TermAdmin(VersionAdmin):
    pass


@admin.register(Taxonomy)
class TaxonomyAdmin(VersionAdmin):
    pass
