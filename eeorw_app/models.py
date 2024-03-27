from ckeditor_uploader.fields import RichTextUploadingField
from django.core.mail import send_mail
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import FileField
from django.urls import reverse
from django.utils import timezone
from django_resized import ResizedImageField

from eeorw.settings import EMAIL_HOST_USER


class Region(models.Model):
    class Meta:
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'

    title_en = models.CharField(max_length=255)
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    lat = models.CharField(max_length=255)
    lng = models.CharField(max_length=255)
    zoom = models.IntegerField()

    def __str__(self):
        return self.title_en


class District(models.Model):
    class Meta:
        verbose_name = 'District'
        verbose_name_plural = 'Districts'

    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    title_en = models.CharField(max_length=255)
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    lat = models.CharField(max_length=255, blank=True, null=True)
    lng = models.CharField(max_length=255, blank=True, null=True)
    zoom = models.IntegerField(blank=True, null=True)

    num_of_vil = models.IntegerField(default=None, blank=True, null=True)
    budget = models.IntegerField(default=None, blank=True, null=True)

    def __str__(self):
        return self.title_en


class Village(models.Model):
    class Meta:
        verbose_name = 'Village'
        verbose_name_plural = 'Villages'

    district = models.ForeignKey(District, on_delete=models.CASCADE)
    title_en = models.CharField(max_length=255, unique=True)
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    id_villages = models.IntegerField(null=True, blank=True, unique=True)
    lat = models.CharField(max_length=255)
    lng = models.CharField(max_length=255)
    zoom = models.IntegerField()

    def __str__(self):
        return self.title_en


class VillageDocuments(models.Model):
    class Meta:
        verbose_name = 'Village Document'
        verbose_name_plural = 'Village Documents'

    village = models.ForeignKey(Village, on_delete=models.CASCADE)

    title_en = models.CharField(max_length=255, null=True)
    title_uz = models.CharField(max_length=255, null=True)
    title_ru = models.CharField(max_length=255, null=True)

    file = models.FileField(upload_to='documents/village_documents/',
                            validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True)

    date = models.DateField(null=True)

    def __str__(self):
        return self.title_en


class SocialAudit(models.Model):
    class Meta:
        verbose_name = 'Social Audit'
        verbose_name_plural = 'Social Audit'

    village = models.OneToOneField(Village, on_delete=models.CASCADE)
    number_of_audits = models.IntegerField(blank=True, null=True,
                                           validators=[MinValueValidator(0), MaxValueValidator(3)],
                                           verbose_name="Number of social audits that have been "
                                                        "completed across the targeted rural qishloqs")
    one_a = models.IntegerField(blank=True,
                                null=True,
                                verbose_name="1(a). Percentage of sampled respondents who report improvements "
                                             "in the quality of basic rural infrastructure",
                                validators=[MinValueValidator(0), MaxValueValidator(100)])
    one_b = models.IntegerField(blank=True,
                                null=True,
                                verbose_name="1(b). of which female ",
                                validators=[MinValueValidator(0), MaxValueValidator(100)])
    two_a = models.IntegerField(blank=True,
                                null=True,
                                verbose_name="2(a). Percentage of beneficiaries who participate in planning, "
                                             "decision-making, or monitoring subprojects",
                                validators=[MinValueValidator(0), MaxValueValidator(100)])
    two_b = models.IntegerField(blank=True,
                                null=True,
                                verbose_name="2(b). of which female ",
                                validators=[MinValueValidator(0), MaxValueValidator(100)])
    one_point_two = models.IntegerField(blank=True,
                                        null=True,
                                        verbose_name="1.2(a). Percentage of sampled respondents reporting improved "
                                                     "access to basic rural infrastructure",
                                        validators=[MinValueValidator(0), MaxValueValidator(100)])
    one_point_two_b = models.IntegerField(blank=True,
                                          null=True,
                                          verbose_name="1.2(b). of which female ",
                                          validators=[MinValueValidator(0), MaxValueValidator(100)])
    one_point_three = models.IntegerField(blank=True,
                                          null=True,
                                          verbose_name="1.3(a) Percentage of sampled respondents "
                                                       "who report that the project "
                                                       "investments in basic rural infrastructure meet their needs",
                                          validators=[MinValueValidator(0), MaxValueValidator(100)])
    one_point_three_b = models.IntegerField(blank=True,
                                            null=True,
                                            verbose_name="1.3(b). of which female ",
                                            validators=[MinValueValidator(0), MaxValueValidator(100)])
    improved_water = models.IntegerField(blank=True,
                                         null=True,
                                         verbose_name="1.5 Percentage of beneficiaries in targeted rural qishloqs "
                                                      "with improved quality of water supply as a result of "
                                                      "project investments",
                                         validators=[MinValueValidator(0), MaxValueValidator(100)])
    woman_funding = models.IntegerField(blank=True,
                                        null=True,
                                        verbose_name="2.4 Percentage of women's priorities that "
                                                     "receive subproject funding",
                                        validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return self.village.title_en


class News(models.Model):
    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'

    title_en = models.CharField(max_length=255, null=True, blank=True)
    title_ru = models.CharField(max_length=255, null=True, blank=True)
    title_uz = models.CharField(max_length=255, null=True)

    description_en = RichTextUploadingField(null=True, blank=True)
    description_ru = RichTextUploadingField(null=True, blank=True)
    description_uz = RichTextUploadingField(null=True)

    date = models.DateField(null=True)

    views = models.IntegerField(default=0, null=True, blank=True)

    image = ResizedImageField(upload_to='news/images/',
                              validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg', 'webp'])],
                              null=True, blank=True, quality=65, force_format='JPEG')

    image_uz = ResizedImageField(upload_to='news/images/',
                                 validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg', 'webp'])],
                                 null=True, blank=True, quality=65, force_format='JPEG')

    image_ru = ResizedImageField(upload_to='news/images/',
                                 validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg', 'webp'])],
                                 null=True, blank=True, quality=65, force_format='JPEG')

    video_title = models.CharField(max_length=255, null=True, blank=True)
    video = FileField(upload_to='news/videos/',
                      validators=[
                          FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mov', 'wmv', 'flv', 'gif'])],
                      null=True, blank=True)

    video_title_uz = models.CharField(max_length=255, null=True, blank=True)
    video_uz = FileField(upload_to='news/videos/',
                         validators=[
                             FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mov', 'wmv', 'flv', 'gif'])],
                         null=True, blank=True)

    video_title_ru = models.CharField(max_length=255, null=True, blank=True)
    video_ru = FileField(upload_to='news/videos/',
                         validators=[
                             FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mov', 'wmv', 'flv', 'gif'])],
                         null=True, blank=True)

    file_uz_one = models.FileField(upload_to='news/documents/uz',
                                   validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True,
                                   blank=True)
    file_uz_two = models.FileField(upload_to='news/documents/uz',
                                   validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True,
                                   blank=True)
    file_uz_three = models.FileField(upload_to='news/documents/uz',
                                     validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True,
                                     blank=True)
    file_uz_four = models.FileField(upload_to='news/documents/uz',
                                    validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True,
                                    blank=True)
    file_uz_five = models.FileField(upload_to='news/documents/uz',
                                    validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True,
                                    blank=True)
    file_uz_six = models.FileField(upload_to='news/documents/uz',
                                   validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True,
                                   blank=True)

    file_en_one = models.FileField(upload_to='news/documents/en',
                                   validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True,
                                   blank=True)
    file_en_two = models.FileField(upload_to='news/documents/en',
                                   validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True,
                                   blank=True)
    file_en_three = models.FileField(upload_to='news/documents/en',
                                     validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True,
                                     blank=True)
    file_en_four = models.FileField(upload_to='news/documents/en',
                                    validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True,
                                    blank=True)
    file_en_five = models.FileField(upload_to='news/documents/en',
                                    validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True,
                                    blank=True)
    file_en_six = models.FileField(upload_to='news/documents/en',
                                   validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True,
                                   blank=True)
    file_ru_one = models.FileField(upload_to='news/documents/ru',
                                   validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True,
                                   blank=True)
    file_ru_two = models.FileField(upload_to='news/documents/ru',
                                   validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True,
                                   blank=True)
    file_ru_three = models.FileField(upload_to='news/documents/ru',
                                     validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True,
                                     blank=True)
    file_ru_four = models.FileField(upload_to='news/documents/ru',
                                    validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True,
                                    blank=True)
    file_ru_five = models.FileField(upload_to='news/documents/ru',
                                    validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True,
                                    blank=True)
    file_ru_six = models.FileField(upload_to='news/documents/ru',
                                   validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True,
                                   blank=True)
    extra_img_one = ResizedImageField(upload_to='news/extra/images',
                                      validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg'])],
                                      null=True, blank=True, quality=65, force_format='JPEG')
    extra_img_two = ResizedImageField(upload_to='news/extra/images',
                                      validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg'])],
                                      null=True, blank=True, quality=65, force_format='JPEG')
    extra_img_three = ResizedImageField(upload_to='news/extra/images',
                                        validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg'])],
                                        null=True, blank=True, quality=65, force_format='JPEG')

    english = models.BooleanField(blank=True, default=1)

    russian = models.BooleanField(blank=True, default=1)

    uzbek = models.BooleanField(blank=True, default=1)

    def __str__(self):
        return self.title_uz

    def get_absolute_url(self):
        return reverse('news_details', args=[str(self.pk)])


class Document(models.Model):
    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    title_en = models.CharField(max_length=255, null=True, blank=True)
    title_uz = models.CharField(max_length=255, null=True, blank=True)
    title_ru = models.CharField(max_length=255, null=True, blank=True)

    file_en = models.FileField(upload_to='documents/en',
                               validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True, blank=True)
    file_uz = models.FileField(upload_to='documents/uz',
                               validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True, blank=True)
    file_ru = models.FileField(upload_to='documents/ru',
                               validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True, blank=True)

    date = models.DateField(null=True)

    def __str__(self):
        return self.title_en


class Contact(models.Model):
    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contact'

    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True)
    message = models.CharField(max_length=1000, blank=True)
    received_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    # for moderator
    reply_subject = models.CharField(max_length=255, blank=True, null=True)
    reply_message = RichTextUploadingField(max_length=1000, blank=True, null=True)
    replied_date = models.DateTimeField(blank=True, null=True, editable=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.reply_subject and self.reply_message:
            self.replied_date = timezone.now()
            send_mail(self.reply_subject, self.reply_message, EMAIL_HOST_USER, [self.email], fail_silently=False)
            super(Contact, self).save()
        else:
            super(Contact, self).save()

    def __str__(self):
        return self.name


class AboutPage(models.Model):
    class Meta:
        verbose_name = 'About Page Content'
        verbose_name_plural = 'About Page Content'

    about_en = RichTextUploadingField(blank=True, null=True)
    about_ru = RichTextUploadingField(blank=True, null=True)
    about_uz = RichTextUploadingField(blank=True, null=True)

    image_en = ResizedImageField(upload_to='images/about_page/',
                                 validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg'])],
                                 null=True, blank=True, quality=65, force_format='JPEG')

    image_ru = ResizedImageField(upload_to='images/about_page/',
                                 validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg'])],
                                 null=True, blank=True, quality=65, force_format='JPEG')

    image_uz = ResizedImageField(upload_to='images/about_page/',
                                 validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg'])],
                                 null=True, blank=True, quality=65, force_format='JPEG')

    def __str__(self):
        return self.about_en


class FAQ(models.Model):
    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'

    question_en = models.TextField(blank=True, null=True)
    question_uz = models.TextField(blank=True, null=True)
    question_ru = models.TextField(blank=True, null=True)

    answer_en = models.TextField(blank=True, null=True)
    answer_uz = models.TextField(blank=True, null=True)
    answer_ru = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.question_en


class PIUStaff(models.Model):
    class Meta:
        verbose_name = 'PIU_Staff'
        verbose_name_plural = 'PIU Staff'

    title_en = models.CharField(max_length=255, null=True)
    title_ru = models.CharField(max_length=255, null=True, blank=True)
    title_uz = models.CharField(max_length=255, null=True, blank=True)

    name = models.CharField(max_length=255, null=True)
    name_en = models.CharField(max_length=255, null=True)
    name_ru = models.CharField(max_length=255, null=True)

    rank = models.IntegerField(blank=True, default=100, null=True)

    office = models.IntegerField(default=0, blank=False, )  # 0-JPIU, 1-Toshkent, 2-Djizzak, 3-Namangan, 4-Buxoro, 5-QQR

    image = ResizedImageField(upload_to='images/piu/staff',
                              validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg'])], null=True,
                              blank=True, quality=65)

    def __str__(self):
        return self.title_en


class Gallery(models.Model):
    class Meta:
        verbose_name = 'Gallery'
        verbose_name_plural = 'Galleries'

    title_en = RichTextUploadingField(max_length=255, null=True)
    title_ru = RichTextUploadingField(max_length=255, null=True, blank=True)
    title_uz = RichTextUploadingField(max_length=255, null=True, blank=True)
    date = models.DateTimeField(auto_now=True, null=True)

    image = ResizedImageField(upload_to='gallery/images/',
                              validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg'])], null=True,
                              blank=True, quality=65)

    video = FileField(upload_to='gallery/videos/',
                      validators=[
                          FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mov', 'wmv', 'flv', 'gif'])],
                      null=True, blank=True)
