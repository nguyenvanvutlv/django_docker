from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest

# models
from blog.models import Reporter, Article
from django.contrib.auth.models import User


# logout
from django.contrib.auth import logout


class HomeView(ListView):
    model = Article
    template_name = "blog/index.html"
    context_object_name = "articles"
    # paginate_by = 2






# Create your views here.
def home_blog(request):    
    
    template = loader.get_template("blog/index.html")
    context = {
        "notification" : 1
    }
      
    return HttpResponse(template.render(context, request))


def article_blog(request):    
    objects = Article.objects.all()
    template = loader.get_template("blog/only_article.html")
    context = {
        "objects" : objects
    }
    return HttpResponse(template.render(context, request))

def question_blog(request):    
    objects = Article.objects.all()
    template = loader.get_template("blog/only_question.html")
    context = {
        "objects" : objects
    }
    return HttpResponse(template.render(context, request))


def article_blogid(request, article_id):    
    
    
    objects = Article.objects.filter(id= article_id)[0]
    # print(objects)
    
    template = loader.get_template("blog/content_article.html")
    context = {
        "objects" : objects
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
        # trả về tên của người dùng đang sử dụng để viết bài
        "usename" : _user.get_username(),
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
