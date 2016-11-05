from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category,Page
from rango.forms import CategoryForm,PageForm

def index(request):
	category_list = Category.objects.order_by('-likes')
	best_pages = Page.objects.order_by("-views")[:5]
	
	context_dict = {'categories':category_list,'topviews':best_pages}
	"""context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}"""
	return render(request,'rango/index.html',context=context_dict)
	#return HttpResponse("Rango says hey there partner!<br/><a href='/rango/about'>About</a>")
	
def about(request):
	context_dict = { 'name': "Jaskaran" }
	return render(request,'rango/about.html',context=context_dict)
	#return HttpResponse("Rango about page<br/><a href='/rango/index'>Index</a>")
	
def show_category(request,category_slug):
	context_dict = {}
	try:
		cat = Category.objects.get(slug=category_slug)
		catpages = Page.objects.filter(category=cat)
		context_dict["category"] = cat
		context_dict["pages"] = catpages
	except Category.DoesNotExist:
		context_dict["category"] = None
		context_dict["pages"] = None
	return render(request,'rango/category.html',context=context_dict)

def add_category(request):
	form = CategoryForm()
	
	if request.method == 'POST':
		form = CategoryForm(request.POST)
		if form.is_valid():
			form.save(commit=True)
			return index(request)
		else:
			print(form.errors)
	return render(request, 'rango/add_category.html', {'form': form})

def add_page(request,category_name_slug):
	try:
		c = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		c = None
	form = PageForm()	
	
	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			if c:
				p = form.save(commit=False)
				p.views = 0
				p.category = c
				p.save()
				return show_category(request,category_name_slug)
		else:
			print(form.errors)
	return render(request,'rango/add_page.html',{'form':form,"category":c})
