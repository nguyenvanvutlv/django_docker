from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest

# models
from blog.models import Reporter, Article
from django.contrib.auth.models import User


# logout
from django.contrib.auth import logout


# Create your views here.
class HomeView(ListView):
    model = Article
    template_name = "blog/home_view/index.html"
    context_object_name = "articles"
    # paginate_by = 2




def article_blog(request):    
    objects = Article.objects.all()
    template = loader.get_template("blog/article_view/only_article.html")
    context = {
        "articles" : objects
    }
    return HttpResponse(template.render(context, request))

def question_blog(request):    
    objects = Article.objects.all()
    template = loader.get_template("blog/article_view/only_question.html")
    context = {
        "articles" : objects
    }
    return HttpResponse(template.render(context, request))


def article_blogid(request, article_id):    
    
    
    objects = Article.objects.filter(id= article_id)[0]
    # print(objects)
    
    template = loader.get_template("blog/article_view/content_article.html")
    context = {
        "objects" : objects
    }
      
    return HttpResponse(template.render(context, request))

def edit_article(request, id):    
    views = id
    # lấy session_id của người dùng đang đăng nhập
    user = request.session['_auth_user_id']
    
    # lấy đối tượng từ bảng User
    _user = User.objects.filter(id = user)[0]
    # lấy đối tượng từ bảng Reporter
    _reporter = Reporter.objects.filter(reporter_id= _user)[0]
    
    # lấy tất cả các bài viết của _user
    _article = Article.objects.filter(reporter= _reporter)
    _title = ""
    _pub_date = ""
    _content = ""
    _types_blog = ""
    _tags = ""
    save = None
    alert = False
    error_code = ""
    if views != "0":
        _article = Article.objects.filter(id= int(id))[0]
        _title = _article.title
        _pub_date = _article.pub_date
        _content  = _article.content
        _types_blog = _article.types_blog
        _tags = _article.tag
    
    if request.method == "POST":
        if "delete" in request.POST.keys():
            _article.delete()
            return redirect("/blog/edit/0")
        alert = True
        try:
            _article.title = request.POST['title']
            _article.pub_date = request.POST['pub_date']
            _article.content = request.POST['content']
            _article.types_blog = request.POST['tags']
            _article.tag = request.POST['types_blog']
            _article.save()
            save = "1"
            _article = Article.objects.filter(id= int(id))[0]
            _title = _article.title
            _pub_date = _article.pub_date
            _content  = _article.content
            _types_blog = _article.types_blog
            _tags = _article.tag
        except Exception as e:
            save = "2"
            error_code = e
            
    # print("SAVE", save)
    template = loader.get_template("blog/user/my_article.html")
    context = {
        "username" : _reporter.reporter_id.get_username(),
        "views" : views,
        "articles" : _article,
        "title" : _title,
        "pub_date" :  _pub_date,
        "content" : _content,
        "types_blog" : _types_blog,
        "tags" : _tags,
        "saves": save,
        "alert":alert,
        "error_code" : error_code
    }
    return HttpResponse(template.render(context, request))


def write_article(request):
    
    # lấy session_id của người dùng đang đăng nhập
    user = request.session['_auth_user_id']
    
    # lấy đối tượng từ bảng User
    _user = User.objects.filter(id = user)[0]
    # lấy đối tượng từ bảng Reporter
    _reporter = Reporter.objects.filter(reporter_id= _user)[0]
    
    Error = None
    status = 0
    _title = ""
    _pub_date = ""
    _content = ""
    _types_blog = ""
    _tags = ""
    # nếu người dùng ấn nút gửi
    if request.method == "POST":
        # lấy tiêu đề của bài viết
        _title = request.POST['title']
        # lấy ngày đăng bài
        _pub_date = request.POST['pub_date']
        # nội dung bài đăng
        _content  = request.POST['content']
        # kiểu bài đăng
        _types_blog = request.POST['types_blog']
        # lấy tags bài đăng
        _tags = request.POST['tags']
        
        new_blog = Article(title= _title,
                           reporter= _reporter,
                           pub_date= _pub_date,
                           content= _content,
                           number_view= 0,
                           number_comment= 0,
                           up_vote= 0,
                           down_vote= 0,
                           tag= _tags,
                           types_blog= _types_blog)
        
        try:
            new_blog.save()
            Error = "Đăng bài thành công"
            status = 1
        except Exception as e:
            Error = "Lỗi đăng bài: Error[" + str(e) + "]"
            status = 2
        # print(Error)
    
    
    template = loader.get_template("blog/user/article.html")
    if status == 1:
        _title = ""
        _pub_date = ""
        _content = ""
        _types_blog = ""
        _tags = ""
    context = {
        "username" : _user.get_username(),
        "status" : status,
        "alert" : Error,
        "title" : _title,
        "pub_date" :  _pub_date,
        "content" : _content,
        "types_blog" : _types_blog,
        "tags" : _tags
    }
      
    return HttpResponse(template.render(context, request))   


# đăng xuất
def logout_function(request):
    logout(request)
    return redirect('/')
