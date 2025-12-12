from django.contrib import admin
from django.utils.html import format_html
from .models import Produit, Achat, Vente, Order, OrderItem


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'quantite', 'prix_achat', 'prix_vente')
    list_display_links = ('nom',)
    search_fields = ('nom',)
    list_filter = ('quantite',)
    readonly_fields = ('image_preview',)
    fields = ('nom', 'quantite', 'prix_achat', 'prix_vente', 'image', 'image_preview', 'description')

    def get_readonly_fields(self, request, obj=None):
        # Make image_preview readonly only when not in popup
        if '_popup' in request.GET:
            return ()
        return self.readonly_fields

    def get_fields(self, request, obj=None):
        # Don't show image_preview in popup or when adding new object
        if '_popup' in request.GET or obj is None:
            return ('nom', 'quantite', 'prix_achat', 'prix_vente', 'image', 'description')
        return self.fields

    def image_thumbnail(self, obj):
        if obj.image and obj.image.url:
            try:
                return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" alt="{}" />',
                                 obj.image.url, obj.nom)
            except:
                return format_html('<span style="color: #999; font-style: italic;">خطأ في الصورة</span>')
        return format_html('<span style="color: #999; font-style: italic;">لا توجد صورة</span>')
    image_thumbnail.short_description = 'صورة'

    def image_preview(self, obj):
        if obj.image and obj.image.url:
            try:
                return format_html('<img src="{}" width="150" height="150" style="object-fit: cover; border-radius: 5px;" alt="{} - معاينة" />',
                                 obj.image.url, obj.nom)
            except:
                return format_html('<span style="color: #999; font-style: italic;">خطأ في تحميل الصورة</span>')
        return format_html('<span style="color: #999; font-style: italic;">لا توجد صورة للمعاينة</span>')
    image_preview.short_description = 'معاينة الصورة'
    
    def has_description(self, obj):
        if obj.description:
            return format_html('<span style="color: green;">✓</span>')
        return format_html('<span style="color: red;">✗</span>')
    has_description.short_description = 'له وصف'


@admin.register(Achat)
class AchatAdmin(admin.ModelAdmin):
    list_display = ('produit', 'quantite', 'date_achat')
    list_filter = ('date_achat',)
    search_fields = ('produit__nom',)


@admin.register(Vente)
class VenteAdmin(admin.ModelAdmin):
    list_display = ('produit', 'quantite', 'date_vente', 'get_total')
    list_filter = ('date_vente',)
    search_fields = ('produit__nom',)
    
    def get_total(self, obj):
        return f"{obj.total()} د.ت"
    get_total.short_description = 'الإجمالي'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('produit', 'quantite', 'prix', 'get_total')
    readonly_fields = ('get_total',)
    
    def get_total(self, obj):
        if obj.id:
            return f"{obj.total()} د.ت"
        return "-"
    get_total.short_description = 'الإجمالي'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'telephone', 'wilaya', 'ville', 'status', 'date_commande', 'get_total')
    list_filter = ('status', 'date_commande', 'wilaya')
    search_fields = ('nom', 'telephone', 'ville')
    inlines = [OrderItemInline]
    readonly_fields = ('date_commande',)
    
    fieldsets = (
        ('معلومات العميل', {
            'fields': ('nom', 'telephone', 'wilaya', 'ville')
        }),
        ('معلومات الطلب', {
            'fields': ('status', 'date_commande', 'notes')
        }),
    )
    
    def get_total(self, obj):
        return f"{obj.total()} د.ت"
    get_total.short_description = 'المجموع الكلي'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'produit', 'quantite', 'prix', 'get_total')
    list_filter = ('order__date_commande',)
    search_fields = ('order__nom', 'produit__nom')
    
    def get_total(self, obj):
        return f"{obj.total()} د.ت"
    get_total.short_description = 'الإجمالي'
