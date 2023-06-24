from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest

# models
from blog.models import Reporter, Article, Groups_User
from django.contrib.auth.models import User


# logout
from django.contrib.auth import logout, authenticate, login


# API
from rest_framework.views import APIView
from rest_framework.response import Response


# Session
from django.contrib.sessions.models import Session

def process_name(name: str):
    try:
        name = name.strip()
        name = name.split()
        first, last = " ".join(name[:-1]), name[-1]
    except Exception as error:
        return (False, error)
    # print(first, last)
    return first, last

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


class ViewArticle(APIView):
    def get(self, request):
        objects = Article.objects.all()
        index = 1
        _dict = {}
        for object in objects:
            tmp = object.__dict__
            del tmp['_state']
            _dict[str(index)] = tmp
            index += 1
        
        return Response({"article" : _dict})
    
class MyArticle(APIView):
    
    def get(self, request):
        objects = Article.objects.all()
        index = 1
        result = {}
        for object in objects:
            temp = object.__dict__
            del temp['_state']
            
            dem = 0
            for key in request.data.keys():
                if key in temp.keys() and temp[key] == request.data[key]:
                    dem += 1
            if dem == len(request.data.keys()):
                result[f"{index}"] = temp
                index+=1
            
        
        return Response({"article" : result})
    
class CreateArticle(APIView):
    
    def post(self, request):
        # print(request.session['_auth_user_id'])
        Error = "NONE"
        
        user = Session.objects.get(pk= request.data['session_key']).get_decoded().get('_auth_user_id')
        
        _user = User.objects.filter(id = user)[0]
        _reporter = Reporter.objects.filter(reporter_id= _user)[0]
        
        
        _title = request.data['title']
        # lấy ngày đăng bài
        _pub_date = request.data['pub_date']
        # nội dung bài đăng
        _content  = request.data['content']
        # kiểu bài đăng
        _types_blog = request.data['types_blog']
        # lấy tags bài đăng
        _tags = request.data['tags']
            
        try:
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
        
        
            new_blog.save()
            Error = "Đăng bài thành công"
        except Exception as e:
            Error = e
    

        return Response({"result" : Error})
    
    
class API_Login(APIView):
    def get(self, request):
        status = ""
        id_user = "-"
        username = request.data["Username"]
        password = request.data["Password"]
        user = authenticate(username= request.data["Username"], password= request.data["Password"])
        session_key = ""
        if user is not None:
            login(request, user)
            print(Session.objects.all())
            print("OK")
            status = "Đăng nhập thành công"
            session_key = ""
            session_list = Session.objects.all()
            for item in session_list:
                print("CALLING")
                uid = item.get_decoded().get('_auth_user_id')
                if uid is None:
                    continue
                user = User.objects.get(pk=uid)
                if user.username == username and user.check_password(password):
                    session_key = item.session_key
                    break
            
            
        else:
            status = "Đăng nhập không thành công"
        
        return Response({"result" : status, "session_key" : session_key})


class API_Register(APIView):
    
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        rpassword = request.data['rpassword']
        name = request.data['name']
        email = request.data['email']
        phone = request.data['phone']
        address = request.data['address']
        company = request.data['company']
        gender = request.data['gender']
        
        if rpassword == password:
            pass
        else:
            return Response({"status" : "Mật khẩu nhập lại không đúng"})
        
        first_result, last_result = process_name(name)
        
        if first_result != False:
            try:
                _users = User(username= username,
                        email= email, 
                        first_name= last_result,
                        last_name= first_result)
                _users.set_password(raw_password= password)
                _users.save()
                new_userblog = Groups_User(user= _users, group_name= "blog")
                new_userblog.save()
                
                
                new_reporter = Reporter(reporter_id= _users,
                                        gender= gender,
                                        phone_number= phone,
                                        address= address,
                                        company= company)
                new_reporter.save()
                return Response({"status" : "Tạo tài khoản thành công"})
                
            except Exception as error:
                return Response({"status" : str(error)})
        else:
            return Response({"status" : "Tên không đúng định dạng"})
        
        
class API_Edit(APIView):
    def post(self, request):
        data = request.data
        if data["delete"] == True:
            try:
                user = Session.objects.get(pk= request.data['session_key']).get_decoded().get('_auth_user_id')
                _user = User.objects.filter(id = user)[0]
                _reporter = Reporter.objects.filter(reporter_id= _user)[0]
            except:
                return Response({"status" : "Session key không đúng"})
            id_article = data["id_article"]
            deleted = False
            articles = Article.objects.all()
            for index, article in enumerate(articles):
                if articles[index].id == id_article:
                    articles[index].delete()
                    deleted = True
            
            if deleted:
                return Response({"status" : "Xoá bài viết thành công"})
            else:
                return Response({"status" : "Xoá bài viết không thành công"})
        else:
            try:
                user = Session.objects.get(pk= request.data['session_key']).get_decoded().get('_auth_user_id')
                _user = User.objects.filter(id = user)[0]
                _reporter = Reporter.objects.filter(reporter_id= _user)[0]
            except:
                return Response({"status" : "Session key không đúng"})
            
            id_article = data["id_article"]
            edit = False
            articles = Article.objects.all()
            for index, article in enumerate(articles):
                if articles[index].id == id_article:
                    articles[index].title = request.data['title']
                    articles[index].pub_date = request.data['pub_date']
                    articles[index].content = request.data['content']
                    articles[index].types_blog = request.data['tags']
                    articles[index].tag = request.data['types_blog']
                    articles[index].save()
                    edit = True
            
            if edit:
                return Response({"status" : "Chỉnh sửa bài viết thành công"})
            else:
                return Response({"status" : "Chỉnh sửa bài viết không thành công"})
            
