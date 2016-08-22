import floppyforms
from django.contrib import admin
from django import forms
from redactor.widgets import RedactorEditor

from reversion.admin import VersionAdmin

from ojoalplato.blog.models import Post, PostMeta, Comment, Term, Taxonomy


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
    list_filter = ['title', 'author', 'status']
    list_display = ['title', 'author']
    advanced_options = ['guid', 'post_type', 'excerpt', 'content_filtered', 'post_date', 'modified',
                        'comment_status', 'comment_count', 'ping_status', 'to_ping', 'pinged',
                        'password', 'parent_id', 'menu_order', 'mime_type']
    fieldsets = (
        (None, {
            'fields': ('status', 'title', 'slug', 'author', 'tags', 'category', 'image_header', 'content')
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


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_filter = ['comment_type', 'author_name']


@admin.register(Term)
class TermAdmin(VersionAdmin):
    pass


@admin.register(Taxonomy)
class TaxonomyAdmin(VersionAdmin):
    pass
