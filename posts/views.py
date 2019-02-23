import json
import weasyprint
from weasyprint import HTML
from .models import Post, HashTag
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib import auth
from django.views import View
from django.contrib.auth.models import User
from posts.forms import PostForm, SearchForm, SearchTagForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import logout
from django.conf import settings

User = get_user_model()


class Index(View):
    def get(self, request):
        context = {'text': 'Hello World!'}
        return render(request, "base.html", context)


class Profile(View):
    def get(self, requset, username):
        user = User.objects.get(username=username)
        posts = Post.objects.filter(user=user)
        form = PostForm()
        context = {
            'posts': posts,
            'user': user,
            'form': form,
        }
        return render(requset, 'profile.html', context)


class PostPost(View):
    def post(self, request, username):
        form = PostForm(self.request.POST)
        if form.is_valid():
            user = User.objects.get(username=username)
            post = Post(text=form.cleaned_data['text'],
                        specialty=form.cleaned_data['specialty'],
                        plan=form.cleaned_data['plan'],
                        plan_rez=form.cleaned_data['plan_rez'],
                        plan_clock=form.cleaned_data['plan_clock'],
                        plan_clock_rez=form.cleaned_data['plan_clock_rez'],
                        plan_defect=form.cleaned_data['plan_defect'],
                        user=user)
            post.save()
            words = form.cleaned_data['text'].split(' ')
            for word in words:
                if word.startswith('#'):
                    hash_tag, created = HashTag.objects.get_or_create(name=word)
                    hash_tag.post.add(post)
        return HttpResponseRedirect('/user/'+username)


class Search(View):
    """" Search all posts """
    def get(self, request):
        form = SearchForm()
        context = {'search': form}
        return render(request, 'search.html', context)

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data['q']
            posts = Post.objects.all().filter(text__icontains=q)
            context = {'q': q,
                       'posts': posts,
            }
            return_str = render_to_string('part_views/_post_search.html', context)
            return HttpResponse(json.dumps(return_str), content_type='application/json')
        else:
            HttpResponseRedirect("/search")


class SearchTags(View):
    def get(self, request):
        form = SearchTagForm()
        context = {'searchtag': form}
        return render(request, 'search_tag.html', context)

    def post(self, request):
        q = request.POST['q']
        form = SearchTagForm()
        tags = HashTag.objects.filter(name__icontains=q)
        context = {'tags': tags,
                   'searchtag': form,
        }
        return render(request, 'search_tag.html', context)


class TagJson(View):
    def get(self, requset):
        q = requset.GET.get('q', '')
        taglist = []
        tags = HashTag.objects.filter(name__icontains=q)
        for tag in tags:
            new = {'q': tag.name,
                   'count': int(len(tag.post.all)),
            }
            taglist.append(new)
        return HttpResponse(json.dumps(taglist), content_type="application/json")


class Login(View):
    def get(self, request):
        return render(request, "registration/login.html")

    def post(self, requset):
        if requset.POST:
            username = requset.POST.get('username', '')
            password = requset.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(requset, user)
        return HttpResponseRedirect('user/'+username)


class LogOut(View):
    def get(self, request):
        logout(request)
        '''response = redirect('/')'''
        return render(request, 'logout.html')


class Registr(View):
    def get(self, request):
        form = UserCreationForm()
        forms = {'form': form}
        return render(request, 'registration/regst.html', forms)

    def post(self, request):
        """form = UserCreationForm"""
        """args = {'form': form}"""
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/')
            else:
                form = UserCreationForm()
                args = {'form': form,
                        'text': 'Вы ввели неверные данные. Попробуйте еще раз'
                }
            return render(request, 'registration/regst.html', args)


def get_data(request):
    data = {
        "sales": 100,
        "customers": 10,
    }
    return JsonResponse(data)


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, username):
        labels = []
        default_items = []
        chart_plan = []
        chart_plan_rez = []
        chart_clock = []
        chart_clock_rez = []
        """qs_count = User.objects.all().count()"""
        user = User.objects.get(username=username)
        posts = Post.objects.filter(user=user)
        for post in posts:
            labels.append(post.text)
            chart_plan.append(post.plan)
            chart_plan_rez.append(post.plan_rez)
            chart_clock.append(post.plan_clock)
            chart_clock_rez.append(post.plan_clock_rez)
            default_items.append(post.plan_defect)
        """for post in posts:"""
        """rezult_procent = int(((post.plan_rez / (post.plan_clock_rez-post.plan_defect)) * 100) / (post.plan / post.plan_clock))"""
        """default_items.append(rezult_procent)"""
        """labels = [users, "Blue", "Yellow", "Green", "Purple", "Orange"]"""
        """default_items = [qs_count, 25, 35, 15, 16]"""
        data = {
            "labels": labels,
            "default": default_items,
            "chartPlan": chart_plan,
            "chartPlanRez": chart_plan_rez,
            "chartClock": chart_clock,
            "chartClockRez": chart_clock_rez,
        }
        return Response(data)


class Ind(View):
    def get(self, request, username):
        usert = username
        users = {
            'user': usert
        }
        return render(request, "charts.html", users)


class RezultCharts(View):
    def get(self, request, username):
        default_items = []
        user = User.objects.get(username=username)
        posts = Post.objects.filter(user=user)
        for post in posts:
            rezult_procent = int((((post.plan_rez-post.plan_defect) / post.plan_clock_rez) * 100) / (post.plan / post.plan_clock))
            post.plan_all = rezult_procent
            post.plan_rez_all = int((post.plan_rez*100)/post.plan)
            post.plan_clock_all = int((post.plan_clock_rez*100)/post.plan_clock)
            post.plan_defect_all = int((post.plan_defect*100)/post.plan_rez)
            post.save()
        context = {
            'posts': posts,
            'user': user,
            'default': default_items,
        }
        return render(request, "ChartRezult.html", context)


class PdfView(View):
    def pdf_generation(request, username):
        user = User.objects.get(username=username)
        posts = Post.objects.filter(user=user)
        html_template = render_to_string('pdfCheck.html', {'posts': posts})
        pdf_file = HTML(string=html_template).write_pdf(stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'base\\bootstrap.min.css')])
        response = HttpResponse(pdf_file, content_type='application/pdf')
        """response['Content-Disposition'] = 'filename="ChartRezult.pdf'"""
        return response


class ChartRez(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, username):
        labels = []
        default_items = []
        """qs_count = User.objects.all().count()"""
        user = User.objects.get(username=username)
        posts = Post.objects.filter(user=user)
        for post in posts:
            labels.append(post.text)
        for post in posts:
            rezult_procent = int((((post.plan_rez-post.plan_defect) / post.plan_clock_rez) * 100) / (post.plan / post.plan_clock))
            default_items.append(rezult_procent)
        """labels = [users, "Blue", "Yellow", "Green", "Purple", "Orange"]"""
        """default_items = [qs_count, 25, 35, 15, 16]"""
        data = {
            "labels": labels,
            "default": default_items,
        }
        return Response(data)


class Table(View):
    def get(self, requset, username):
        user = User.objects.get(username=username)
        posts = Post.objects.filter(user=user)
        context = {
            'posts': posts,
            'user': user,
        }
        return render(requset, 'table.html', context)


class Analitic(View):
    def get(self, request, username):
        rezultat = 0
        rezultat1 = 0
        rezultat2 = 0
        index = 0
        default_items = []
        rez_all_plan = []
        rez_all_defect = []
        labels = []
        users = User.objects.all().values_list('username', flat=True)
        """local = User.objects.all()."""
        """print(local)"""
        for use in users:
            user = User.objects.get(username=use)
            labels.append(user.first_name)
            posts = Post.objects.filter(user=user)
            for post in posts:
                rezult_procent = int((((post.plan_rez-post.plan_defect) / post.plan_clock_rez) * 100) / (post.plan / post.plan_clock))
                rezult_procent_plan = int((post.plan_rez*100)/post.plan)
                rezult_procent_defect = int((post.plan_defect*100)/post.plan_rez)
                index = index + 1
                rezultat = rezult_procent + rezultat
                rezultat1 = rezult_procent_plan + rezultat1
                rezultat2 = rezult_procent_defect + rezultat2
            default_items.append(int(rezultat/index))
            rez_all_plan.append(int(rezultat1/index))
            rez_all_defect.append(int(rezultat2/index))
        print(default_items)
        context = {
            'posts': posts,
            'labels': labels,
            'default': default_items,
            'rez_all': rez_all_plan,
            'rez_all_defect': rez_all_defect,
        }
        return render(request, "ChartRezAll.html", context)


class ChartRezAll(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, username):
        rezultat = 0
        rezultat1 = 0
        rezultat2 = 0
        index = 0
        default_items = []
        rez_all_plan = []
        rez_all_defect = []
        labels = []
        """qs_count = User.objects.all().count()"""
        users = User.objects.all().values_list('username', flat=True)
        """for use in users:"""
        """ labels.append(use)"""
        for use in users:
            user = User.objects.get(username=use)
            labels.append(user.first_name)
            posts = Post.objects.filter(user=user)
            for post in posts:
                rezult_procent = int(
                    (((post.plan_rez - post.plan_defect) / post.plan_clock_rez) * 100) / (post.plan / post.plan_clock))
                rezult_procent_plan = int((post.plan_rez * 100) / post.plan)
                rezult_procent_defect = int((post.plan_defect * 100) / post.plan_rez)
                index = index + 1
                rezultat = rezult_procent + rezultat
                rezultat1 = rezult_procent_plan + rezultat1
                rezultat2 = rezult_procent_defect + rezultat2
            default_items.append(int(rezultat / index))
            rez_all_plan.append(int(rezultat1 / index))
            rez_all_defect.append(int(rezultat2 / index))
        """labels = [users, "Blue", "Yellow", "Green", "Purple", "Orange"]"""
        """default_items = [qs_count, 25, 35, 15, 16]"""
        print(default_items)
        print(labels)
        data = {
            "labels": labels,
            "default": default_items,
            'rez_all': rez_all_plan,
            'rez_all_defect': rez_all_defect,
        }
        return Response(data)


class EditPerson(View):
    def edit(request, username, id):
        try:
            person = Post.objects.get(id=id)
            if request.method == "POST":
                person.text = request.POST.get("text")
                person.specialty = request.POST.get("specialty")
                person.plan = request.POST.get("plan")
                person.plan_rez = request.POST.get("plan_rez")
                person.plan_clock = request.POST.get("plan_clock")
                person.plan_clock_rez = request.POST.get("plan_clock_rez")
                person.plan_defect = request.POST.get("plan_defect")
                person.save()
                return HttpResponseRedirect('/user/' + username)
            else:
                return render(request, "edit.html", {"person": person})
        except Post.DoesNotExist:
            return HttpResponseNotFound("<h2>Person not found</h2>")


class DeletePerson(View):
    def delete(request, username, id):
        try:
            person = Post.objects.get(id=id)
            person.delete()
            return HttpResponseRedirect('/user/' + username)
        except Post.DoesNotExist:
            return HttpResponseNotFound("<h2>Person not found</h2>")
