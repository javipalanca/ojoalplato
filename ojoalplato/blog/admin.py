from django.contrib import admin
from django import forms
from redactor.widgets import RedactorEditor

from reversion.admin import VersionAdmin

from ojoalplato.blog.models import Post, PostMeta, Comment, Term, Taxonomy


class PostMetaAdmin(admin.TabularInline):
    model = PostMeta


class PostChangeForm(forms.ModelForm):
    class Meta:
        model = Post
        widgets = {
            'content': RedactorEditor(),
        }
        fields = '__all__'


@admin.register(Post)
class PostAdmin(VersionAdmin):
    form = PostChangeForm
    list_filter = ['title', 'author', 'status']
    list_display = ['title', 'author']
    inlines = [PostMetaAdmin]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_filter = ['comment_type', 'author_name']


@admin.register(Term)
class TermAdmin(VersionAdmin):
    pass

@admin.register(Taxonomy)
class TaxonomyAdmin(VersionAdmin):
    pass
