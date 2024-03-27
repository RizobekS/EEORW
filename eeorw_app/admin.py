from django.contrib import admin
from .models import News, Contact, AboutPage, FAQ, Document, PIUStaff, Gallery, Region, District, Village, \
    VillageDocuments, SocialAudit
from eeorw import settings


class VillageAdmin(admin.ModelAdmin):
    list_display = ['district', 'id_villages', 'title_en', 'title_uz', 'title_ru', 'lat', 'lng', 'zoom']
    search_fields = ['district__title_en', 'title_en', 'title_uz', 'title_ru', 'id_villages']

    def unique_id(self, obj):
        return f"{obj.district.region.id:02}{obj.district.id:02}{obj.id:03}"

    fieldsets = (
        (None, {
            'fields': ('district', 'title_en', 'title_uz', 'title_ru', 'id_villages', 'lat', 'lng', 'zoom')
        }),
    )

    class Media:
        if hasattr(settings, 'GOOGLE_MAP_API') and settings.GOOGLE_MAP_API:
            css = {
                'all': ('admin/css/location_picker.css',),
            }
            js = (
                'https://maps.googleapis.com/maps/api/js?key={}'.format(settings.GOOGLE_MAP_API),
                'admin/js/location_picker.js',
            )


class VillageDocumentsAdmin(admin.ModelAdmin):
    list_display = ['village', 'title_en', 'title_uz', 'title_ru', 'date']
    search_fields = ['village__title_en', 'title_en', 'title_uz', 'title_ru']


class DistrictAdmin(admin.ModelAdmin):
    list_display = ['region', 'title_en', 'title_uz', 'title_ru', 'lat', 'lng', 'zoom', 'num_of_vil', 'budget']
    search_fields = ['region__title_en', 'title_en']
    list_editable = ['num_of_vil', 'budget']

    fieldsets = (
        (None, {
            'fields': ('region', 'title_en', 'title_uz', 'title_ru', 'lat', 'lng', 'zoom', 'num_of_vil', 'budget')
        }),
    )

    class Media:
        if hasattr(settings, 'GOOGLE_MAP_API') and settings.GOOGLE_MAP_API:
            css = {
                'all': ('admin/css/location_picker.css',),
            }
            js = (
                'https://maps.googleapis.com/maps/api/js?key={}'.format(settings.GOOGLE_MAP_API),
                'admin/js/location_picker.js',
            )


class RegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title_en', 'title_uz', 'title_ru', 'lat', 'lng', 'zoom']
    search_fields = ['id', 'title_en']

    fieldsets = (
        (None, {
            'fields': ('title_en', 'title_uz', 'title_ru', 'lat', 'lng', 'zoom')
        }),
    )

    class Media:
        if hasattr(settings, 'GOOGLE_MAP_API') and settings.GOOGLE_MAP_API:
            css = {
                'all': ('admin/css/location_picker.css',),
            }
            js = (
                'https://maps.googleapis.com/maps/api/js?key={}'.format(settings.GOOGLE_MAP_API),
                'admin/js/location_picker.js',
            )


class SocialAuditAdmin(admin.ModelAdmin):

    class Media:
        css = {
            'all': ('admin/css/fancy.css',),
        }

    list_display = ['village', 'number_of_audits',
                    # 'one_a', 'one_b', 'two_a', 'two_b', 'one_point_two',
                    # 'one_point_two_b',
                    # 'one_point_three', 'one_point_three_b', 'improved_water', 'woman_funding'
                    ]
    search_fields = ['village__title_en', 'village__title_ru', 'village__title_uz']

    fields = ['village', 'number_of_audits',
              # ('one_a', 'one_b'), ('two_a', 'two_b'),
              # ('one_point_two', 'one_point_two_b'),
              # ('one_point_three', 'one_point_three_b'), 'improved_water', 'woman_funding'
              ]


class NewsAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'title_uz', 'title_ru', 'image_uz',
                    'english', 'russian', 'uzbek', 'date', 'views']

    list_editable = ['english', 'russian', 'uzbek', 'views']

    fields = ['title_uz', 'description_uz', 'image_uz',
              ('file_uz_one', 'file_uz_two', 'file_uz_three', 'file_uz_four', 'file_uz_five', 'file_uz_six',),
              'video_title_uz', 'video_uz', 'title_en', 'description_en', 'image',
              ('file_en_one', 'file_en_two', 'file_en_three', 'file_en_four', 'file_en_five', 'file_en_six',),
              'video_title', 'video', 'title_ru', 'description_ru', 'image_ru',
              ('file_ru_one', 'file_ru_two', 'file_ru_three', 'file_ru_four', 'file_ru_five', 'file_ru_six',),
              'video_title_ru', 'video_ru', 'date', 'extra_img_one', 'extra_img_two', 'extra_img_three',
              'english', 'russian', 'uzbek']

    search_fields = ['title_en', 'title_uz', 'title_ru']


class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'title_uz', 'title_ru', 'file_en', 'file_uz', 'file_ru', 'date']
    search_fields = ['title_en', 'title_uz', 'title_ru']


class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'message', 'received_date', 'replied_date', 'reply_subject', 'reply_message']
    search_fields = ['name', 'email', 'message']


class AboutPageAdmin(admin.ModelAdmin):
    list_display = ['about_en', 'about_ru', 'about_uz']


class FAQAdmin(admin.ModelAdmin):
    list_display = ['question_en', 'question_uz', 'question_ru', 'answer_en', 'answer_uz', 'answer_ru']
    search_fields = ['question_en', 'question_uz', 'question_ru']


class PIUStaffAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'name', 'rank', 'office', 'image']
    search_fields = ['title_en', 'title_ru', 'title_uz', 'name', 'name_ru', 'name_uz']


class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'title_ru', 'title_uz', 'image', 'video', 'date']
    search_fields = ['title_en', 'title_ru', 'title_uz']


admin.site.site_header = "Enhancing economic opportunities for rural women"
admin.site.register(News, NewsAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Village, VillageAdmin)
admin.site.register(VillageDocuments, VillageDocumentsAdmin)
admin.site.register(SocialAudit, SocialAuditAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(AboutPage, AboutPageAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(PIUStaff, PIUStaffAdmin)
admin.site.register(Gallery, GalleryAdmin)
