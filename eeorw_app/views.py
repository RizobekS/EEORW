from django.contrib import messages
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import ContactForm
from .models import News, AboutPage, PIUStaff, FAQ


def home(request):
    # filter news based on date and language availability
    if request.LANGUAGE_CODE == 'en':
        news_home = News.objects.filter(english=True).order_by('-pk')
    elif request.LANGUAGE_CODE == 'ru':
        news_home = News.objects.filter(russian=True).order_by('-pk')
    else:
        news_home = News.objects.filter(uzbek=True).order_by('-pk')
    info_about = AboutPage.objects.first()

    return render(request, "home.html", {'news_home': news_home[:5], 'info_about': info_about, })


def news(request):
    if request.LANGUAGE_CODE == 'en':
        list_news = News.objects.filter(english=True).order_by('-pk')
    elif request.LANGUAGE_CODE == 'ru':
        list_news = News.objects.filter(russian=True).order_by('-pk')
    else:
        list_news = News.objects.filter(uzbek=True).order_by('-pk')

    page = request.GET.get('page', 1)
    paginator = Paginator(list_news, 10)  # number of news in each page

    try:
        list_news = paginator.page(page)
    except PageNotAnInteger:
        list_news = paginator.page(1)
    except EmptyPage:
        list_news = paginator.page(paginator.num_pages)

    return render(request, 'news.html', {'news': list_news})


def news_details(request, pk):
    detail = News.objects.get(pk=pk)
    if request.LANGUAGE_CODE == 'en' and not detail.english:
        return HttpResponseRedirect(f"/{request.LANGUAGE_CODE}/news/")
    elif request.LANGUAGE_CODE == 'uz' and not detail.uzbek:
        return HttpResponseRedirect(f"/{request.LANGUAGE_CODE}/news/")
    elif request.LANGUAGE_CODE == 'ru' and not detail.russian:
        return HttpResponseRedirect(f"/{request.LANGUAGE_CODE}/news/")

    # increment views number by one every request
    detail.views += 1
    detail.save()

    return render(request, "news-details.html", {'detail': detail})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid() and request.POST['address'] == "":
            form.save()
            name = request.POST['name']
            messages.success(request, 'Success!')
            return render(request, 'contact.html', {'name': name})
        else:
            name = "Ooops, something went wrong!"
            return render(request, 'contact.html', {'name': name})
    else:
        return render(request, 'contact.html', {})


def about(request):
    info_about = AboutPage.objects.first()
    return render(request, 'about_us.html', {'info_about': info_about})


def faq(request):
    questions_and_answers = FAQ.objects.all().order_by('id')
    return render(request, 'faq.html', {'questions_and_answers': questions_and_answers})


def piu_staff(request):
    context = {
        'staff_piu': PIUStaff.objects.filter(office=0).order_by('rank'),
        'staff_jizzakh': PIUStaff.objects.filter(office=1).order_by('rank'),
        'staff_fergana': PIUStaff.objects.filter(office=2).order_by('rank'),
    }
    return render(request, 'piu_staff.html', context)
