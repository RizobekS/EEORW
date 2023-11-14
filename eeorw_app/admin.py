from django.contrib import admin
from .models import News, Contact, AboutPage, FAQ


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


class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'message', 'received_date', 'replied_date', 'reply_subject', 'reply_message']
    search_fields = ['name', 'email', 'message']


class AboutPageAdmin(admin.ModelAdmin):
    list_display = ['about_en', 'about_ru', 'about_uz']


class FAQAdmin(admin.ModelAdmin):
    list_display = ['question_en', 'question_uz', 'question_ru', 'answer_en', 'answer_uz', 'answer_ru']
    search_fields = ['question_en', 'question_uz', 'question_ru']


admin.site.site_header = "Enhancing economic opportunities for rural women"
admin.site.register(News, NewsAdmin)
admin.site.register(AboutPage, AboutPageAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(FAQ, FAQAdmin)
