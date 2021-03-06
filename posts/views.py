import json
import weasyprint
from weasyprint import HTML
from .models import Post
from .models import HashTag
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.contrib import auth
from django.views import View
from django.contrib.auth.models import User
from posts.forms import PostForm
from posts.forms import SearchForm
from posts.forms import SearchTagForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import logout
from django.conf import settings

User = get_user_model()


def get_data(request):
    return JsonResponse({
        "sales": 100,
        "customers": 10,
    })


class Index(View):
    def get(self, request):
        return render(request, "base.html", {'text': 'Hello World!'})


class Profile(View):
    def get(self, requset, username):
        return render(requset, 'profile.html', {
            'posts': Post.objects.filter(user=User.objects.get(username=username)),
            'user':  User.objects.get(username=username),
            'form': PostForm(),
        })


class PostPost(View):
    def post(self, request, username):
        form = PostForm(self.request.POST)
        if form.is_valid():
            post = Post(text=form.cleaned_data['text'],
                        specialty=form.cleaned_data['specialty'],
                        plan=form.cleaned_data['plan'],
                        plan_rez=form.cleaned_data['plan_rez'],
                        plan_clock=form.cleaned_data['plan_clock'],
                        plan_clock_rez=form.cleaned_data['plan_clock_rez'],
                        plan_defect=form.cleaned_data['plan_defect'],
                        user=User.objects.get(username=username))
            post.save()
            for word in form.cleaned_data['text'].split(' '):
                if word.startswith('#'):
                    hash_tag, created = HashTag.objects.get_or_create(name=word)
                    hash_tag.post.add(post)
        return HttpResponseRedirect('/user/'+username)


class Search(View):
    def get(self, request):
        return render(request, 'search.html', {'search': SearchForm()})

    def post(self, request):
        if SearchForm(request.POST).is_valid():
            return HttpResponse(json.dumps(render_to_string('part_views/_post_search.html', {
                'q': SearchForm(request.POST).cleaned_data['q'],
                'posts': Post.objects.all().filter(
                    text__icontains=SearchForm(request.POST).cleaned_data['q']
                ),
            })), content_type='application/json')
        else:
            HttpResponseRedirect("/search")


class SearchTags(View):
    def get(self, request):
        return render(request, 'search_tag.html', {'searchtag': SearchTagForm()})

    def post(self, request):
        return render(request, 'search_tag.html', {'tags': HashTag.objects.filter(
            name__icontains=request.POST['q']),
            'searchtag': SearchTagForm,
        })


class TagJson(View):
    def get(self, requset):
        taglist = []
        for tag in HashTag.objects.filter(name__icontains=requset.GET.get('q', '')):
            taglist.append({
                'q': tag.name,
                'count': int(len(tag.post.all)),
            })
        return HttpResponse(json.dumps(taglist), content_type="application/json")


class Login(View):
    def get(self, request):
        return render(request, "registration/login.html")

    def post(self, requset):
        if requset.POST:
            user = auth.authenticate(username=requset.POST.get('username', ''),
                                     password=requset.POST.get('password', ''))
            if user is not None:
                auth.login(requset, user)
        return HttpResponseRedirect('user/' + requset.POST.get('username', ''))


class LogOut(View):
    def get(self, request):
        logout(request)
        return render(request, 'logout.html')


class Registr(View):
    def get(self, request):
        return render(request, 'registration/regst.html', {'form': UserCreationForm()})

    def post(self, request):
        if request.POST:
            if UserCreationForm(request.POST).is_valid():
                UserCreationForm(request.POST).save()
                return redirect('/')
            else:
                return render(request, 'registration/regst.html', {
                    'form': UserCreationForm(),
                    'text': 'Вы ввели неверные данные. Попробуйте еще раз'
                })


class ChartData(APIView):
    authentication_classes, permission_classes = [], []

    def get(self, request, username):
        labels, default_items, chart_plan, chart_plan_rez, chart_clock, chart_clock_rez =\
            [], [], [], [], [], []
        for post in Post.objects.filter(user=User.objects.get(username=username)):
            labels.append(post.text)
            chart_plan.append(post.plan)
            chart_plan_rez.append(post.plan_rez)
            chart_clock.append(post.plan_clock)
            chart_clock_rez.append(post.plan_clock_rez)
            default_items.append(post.plan_defect)
        return Response({
            "labels": labels,
            "default": default_items,
            "chartPlan": chart_plan,
            "chartPlanRez": chart_plan_rez,
            "chartClock": chart_clock,
            "chartClockRez": chart_clock_rez,
        })


class Ind(View):
    def get(self, request, username):
        return render(request, "charts.html", {
            'user': username
        })


class RezultCharts(View):
    def get(self, request, username):
        for post in Post.objects.filter(user=User.objects.get(username=username)):
            post.plan_all = int((((post.plan_rez - post.plan_defect) / post.plan_clock_rez) * 100) /
                                (post.plan / post.plan_clock))
            post.plan_rez_all = int((post.plan_rez * 100) / post.plan)
            post.plan_clock_all = int((post.plan_clock_rez * 100) / post.plan_clock)
            post.plan_defect_all = int((post.plan_defect * 100) / post.plan_rez)
            post.save()
        return render(request, "ChartRezult.html", {
            'posts': Post.objects.filter(user=User.objects.get(username=username)),
            'user': User.objects.get(username=username),
            'default': [],
        })


class PdfView(View):
    def pdf_generation(self, username):
        return HttpResponse(HTML(string=render_to_string('pdfCheck.html', {
            'posts': Post.objects.filter(user=User.objects.get(username=username))}
        )).write_pdf(stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'base\\bootstrap.min.css')]),
                     content_type='application/pdf')


class ChartRez(APIView):
    authentication_classes, permission_classes = [], []

    def get(self, request, username):
        labels, default_items = [], []
        for post in Post.objects.filter(user=User.objects.get(username=username)):
            labels.append(post.text)
            default_items.append(int((((post.plan_rez-post.plan_defect) / post.plan_clock_rez) * 100) /
                                     (post.plan / post.plan_clock)))
        return Response({
            "labels": labels,
            "default": default_items,
        })


class Table(View):
    def get(self, requset, username):
        return render(requset, 'table.html', {
            'posts': Post.objects.filter(user=User.objects.get(username=username)),
            'user': User.objects.get(username=username),
        })


class Analitic(View):
    def get(self, request, username):
        global use
        rezultat, rezultat1, rezultat2, index = 0, 0, 0, 0
        default_items, rez_all_plan, rez_all_defect, labels = [], [], [], []
        for use in User.objects.all().values_list('username', flat=True):
            labels.append(User.objects.get(username=use).first_name)
            for post in Post.objects.filter(user=User.objects.get(username=use)):
                rezult_procent = int((((post.plan_rez-post.plan_defect) / post.plan_clock_rez) * 100) /
                                     (post.plan / post.plan_clock))
                rezult_procent_plan = int((post.plan_rez * 100) / post.plan)
                rezult_procent_defect = int((post.plan_defect * 100) / post.plan_rez)
                rezultat += rezult_procent
                rezultat1 += rezult_procent_plan
                rezultat2 += rezult_procent_defect
                index += 1
            default_items.append(int(rezultat/index))
            rez_all_plan.append(int(rezultat1/index))
            rez_all_defect.append(int(rezultat2/index))
        return render(request, "ChartRezAll.html", {
            'posts': Post.objects.filter(user=User.objects.get(username=use)),
            'labels': labels,
            'default': default_items,
            'rez_all': rez_all_plan,
            'rez_all_defect': rez_all_defect,
        })


class ChartRezAll(APIView):
    authentication_classes, permission_classes = [], []

    def get(self, request, username):
        rezultat, rezultat1, rezultat2, index = 0, 0, 0, 0
        default_items, rez_all_plan, rez_all_defect, labels = [], [], [], []

        for use in User.objects.all().values_list('username', flat=True):
            labels.append(User.objects.get(username=use).first_name)
            for post in Post.objects.filter(user=User.objects.get(username=use)):
                rezult_procent = int(
                    (((post.plan_rez - post.plan_defect) / post.plan_clock_rez) * 100) / (post.plan / post.plan_clock))
                rezult_procent_plan = int((post.plan_rez * 100) / post.plan)
                rezult_procent_defect = int((post.plan_defect * 100) / post.plan_rez)
                rezultat += rezult_procent
                rezultat1 += rezult_procent_plan
                rezultat2 += rezult_procent_defect
                index += 1
            default_items.append(int(rezultat / index))
            rez_all_plan.append(int(rezultat1 / index))
            rez_all_defect.append(int(rezultat2 / index))
        return Response({
            "labels": labels,
            "default": default_items,
            'rez_all': rez_all_plan,
            'rez_all_defect': rez_all_defect,
        })


class EditPerson(View):
    def edit(self, username, id):
        try:
            person = Post.objects.get(id=id)
            if self.POST:
                person.text = self.POST.get("text")
                person.specialty = self.POST.get("specialty")
                person.plan = self.POST.get("plan")
                person.plan_rez = self.POST.get("plan_rez")
                person.plan_clock = self.POST.get("plan_clock")
                person.plan_clock_rez = self.POST.get("plan_clock_rez")
                person.plan_defect = self.POST.get("plan_defect")
                person.save()
                return HttpResponseRedirect('/user/' + username)
            else:
                return render(self, "edit.html", {"person": person})
        except Post.DoesNotExist:
            return HttpResponseNotFound("<h2>Person not found</h2>")


class DeletePerson(View):
    def delete(self, username, id):
        try:
            Post.objects.get(id=id).delete()
            return HttpResponseRedirect('/user/' + username)
        except Post.DoesNotExist:
            return HttpResponseNotFound("<h2>Person not found</h2>")
