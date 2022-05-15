from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms

from .models import Category, Racer, Season, Model, Image, RatingStar, Rating, Reviews
from ckeditor_uploader.widgets import CKEditorUploadingWidget
# Register your models here.


class ModelAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Model
        fields = '__all__'



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')
    list_display_links = ('name',)


class ReviewInline(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ('name', 'email')


class MotoImageInline(admin.TabularInline):
    model = Image
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')

    get_image.short_description = 'Изображение'


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ('category', 'year')
    search_fields = ('title', 'category__name')
    inlines = [MotoImageInline, ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ('draft',)
    actions = ['publish', 'unpublish']
    form = ModelAdminForm
    readonly_fields = ('get_image',)
    fieldsets = (
        (None, {
            'fields': (('title', 'tagline'), )
        }),
        (None, {
            'fields': ('description', ('poster', 'get_image'))
        }),
        (None, {
            'fields': (('year', 'world', 'country'),)
        }),
        ('Racers', {
            'classes': ('collapse',),
            'fields': (('racers', 'manufacturers', 'season', 'category'),)
        }),
        (None, {
            'fields': (('price', 'price_in_rus', 'price_market'),)
        }),
        ('Options', {
            'fields': (('url', 'draft'),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height="110"')

    get_image.short_description = 'Постер'

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            messege_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            messege_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    publish.short_description = 'Опубликовать'
    publish.allowed_permission = ('change',)
    unpublish.short_description = 'Снять с публикации'
    unpublish.allowed_permission = ('change',)

@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'parent', 'model', 'id')
    readonly_fields = ('name', 'email')


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')


@admin.register(Racer)
class RacerAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = 'Изображение'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('model', 'ip', 'star')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'model', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = 'Изображение'


admin.site.register(RatingStar)

admin.site.site_title = 'Django Moto'
admin.site.site_header = 'Django Moto'



