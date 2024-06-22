from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Categories, Nft, Tags, Binance


class NftAdminForm(forms.ModelForm):

    description = forms.CharField(widget=CKEditorUploadingWidget(), label='Описание NFT')

    class Meta:
        model = Nft
        fields = '__all__'



@admin.register(Binance)
class NinanceAdmin(admin.ModelAdmin):
    list_display = ('id','email')
    list_display_links = ('id','email')
    readonly_fields = ('created_at', 'updated_at')




@admin.register(Nft)
class NftAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'get_image',)
    list_display_links = ('name',)
    readonly_fields = ('created_at', 'updated_at', 'get_big_image', 'token')
    filter_horizontal = ('tags',)
    search_fields = ('name', 'token')
    list_filter = ('category', 'tags', 'created_at', 'updated_at')
    form = NftAdminForm


    @admin.display(description='Изображение')
    def get_image(self, item):
        if item.image:
            return mark_safe(f'<img src="{item.image.url}" width="100px">')
        return '-'
    
    @admin.display(description='Изображение')
    def get_big_image(self, item):
        if item.image:
            return mark_safe(f'<img src="{item.image.url}" width="100%">')
        return '-'


admin.site.register(Categories)
admin.site.register(Tags)

# Register your models here.
