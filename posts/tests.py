from django.test import TestCase
from django.test.client import Client
from rest_framework.utils import json
from posts.views import *
from posts.models import Post
from posts.apps import PostsConfig
from django.http import HttpRequest
from importlib import import_module
from django.conf import settings


class UnitTesting(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='vlad', email='vlad@mail.ru', password='top')
		self.c = Client()
		self.form = PostForm()
		self.post = Post()
		self.conf = PostsConfig
		self.profile = Profile()
		self.request = HttpRequest()
		self.posts = PostPost()
		self.search = Search()
		self.login = Login()
		self.logout = LogOut()
		self.ind = Ind()
		self.table = Table()
		self.registrat = Registr()
		self.chart = ChartRez()
		self.chartall = ChartRezAll()
		self.analitic = Analitic()
		self.result = RezultCharts()
		self.pdf = PdfView()
		self.data = ChartData()
		self.posts.request = self.request
		self.request.user = self.user

	def test_basic_auth_and_requests(self):
		response = self.c.get('/')
		response_user = self.c.get('/user/admin/')
		search = self.c.get('/search/')
		schema = self.c.get('/schema/')
		api = self.c.get('/api/data/')
		registration = self.c.get('/registration/')
		reg_user = self.c.login(username=self.user.username, password='top')
		data = json.loads(api.content.decode('utf-8'))['sales']
		self.assertEqual(response.status_code, 200)
		self.assertEqual(registration.status_code, 200)
		self.assertEqual(search.status_code, 302)
		self.assertEqual(schema.status_code, 200)
		self.assertEqual(response_user.status_code, 302)
		self.assertEqual(reg_user, True)
		self.assertEqual(data, 100)

	def test_template_used_and_model_validation(self):
		response = self.c.get('/')
		registration = self.c.get('/registration/')
		self.post.text = 'Dedd'
		self.conf.name = 'app'
		self.assertTemplateUsed(response, 'registration/login.html')
		self.assertTemplateUsed(registration, 'registration/regst.html')
		self.assertEqual(str(self.post), 'Dedd')
		self.assertEqual(self.conf.name, 'app')

	def test_view(self):
		test_profile = self.profile.get(self.request, self.user.username)
		test_post = self.posts.post(self.request, self.user.username)
		test_search = self.search.get(self.request)
		self.request.session = import_module(settings.SESSION_ENGINE).SessionStore(None)
		test_registrat = self.registrat.get(self.request)
		self.assertEqual(test_registrat.status_code, 200)
		test_login = self.login.get(self.request)
		self.assertEqual(test_login.status_code, 200)
		test_ind = self.ind.get(self.request, self.user.username)
		self.assertEqual(test_ind.status_code, 200)
		test_table = self.table.get(self.request, self.user.username)
		self.assertEqual(test_table.status_code, 200)
		test_chart = self.chart.get(self.request, self.user.username)
		self.assertEqual(test_chart.status_code, 200)
		test_charts = self.chartall.get(self.request, self.user.username)
		self.assertEqual(test_charts.status_code, 200)
		test_analitic = self.analitic.get(self.request, self.user.username)
		self.assertEqual(test_analitic.status_code, 200)
		self.pdf.user = self.user
		test_pdf = self.pdf.pdf_generation(self.user.username)
		self.assertEqual(test_pdf.status_code, 200)
		test_data = self.data.get(self.request, self.user.username)
		self.assertEqual(test_data.status_code, 200)
		test_result = self.result.get(self.request, self.user.username)
		self.assertEqual(test_result.status_code, 200)
		test_logout = self.logout.get(self.request)
		self.assertEqual(test_search.status_code, 200)
		self.assertEqual(test_post.url, '/user/vlad')
		self.assertEqual(test_post.status_code, 302)
		self.assertEqual(test_profile.status_code, 200)
		self.assertEqual(check_auth(self.request), False)
		self.assertEqual(test_logout.status_code, 200)
