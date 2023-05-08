from django.db import models
from django.contrib.auth.models import User



import numpy as np
from datetime import date

# Create your models here.
# object_1.class_name.add(object_2) -> many to many

gender_choise = (
    ("MALE", "Male"),
    ("FEMALE", "Female")
)
type_blog = (
    ("trả lời", "hỏi"),
    ("bình luận", "đăng bài viết")
)
class Reporter(models.Model):
    
    reporter_id   = models.ForeignKey(User, on_delete= models.CASCADE)
    gender        = models.CharField(max_length = 20, choices = gender_choise, default = 'MALE')
    phone_number  = models.CharField(max_length= 12, unique= True)
    address       = models.CharField(max_length=100, default= "")
    company       = models.CharField(max_length=100, default= "")
    
    friends_list  = models.TextField(default= "", blank= True, null= True)
    blogs_list    = models.TextField(default= "", blank= True, null= True)
    question_list = models.TextField(default= "", blank= True, null= True)
    organization  = models.TextField(default= "", blank= True, null= True)
    
    def __str__(self):
        return self.reporter_id.last_name + " " + self.reporter_id.first_name
    
    
    def change_password(self, password):
        self.reporter_id.set_password(password)
        self.reporter_id.save()
        
        
    def follow(self, id_reporter):
        friends_list = str(self.friends_list).split('_')
        if id_reporter not in friends_list:
            friends_list.append(id_reporter)
            friends_list = '_'.join(friends_list)
            self.friends_list = friends_list
            self.save()
            
    
    def un_follow(self, id_reporter):
        friends_list = str(self.friends_list).split('_')
        if id_reporter in friends_list:
            np_friends = np.array(friends_list) 
            np_friends = np.delete(np_friends, np.where(np_friends == id_reporter))
            friends_list = '_'.join(list(np_friends))
            self.friends_list = friends_list
            self.save()
            

class Article(models.Model):
    
    title          = models.CharField(max_length= 100, blank= False, null= False)
    reporter       = models.ForeignKey(Reporter, on_delete=models.CASCADE)
    pub_date       = models.DateField()
    
    content        = models.TextField(default= "")
    number_view    = models.CharField(max_length= 100, default= "0")
    number_comment = models.CharField(max_length= 100, default= "0")
    up_vote        = models.CharField(max_length= 100, default= "0")
    down_vote      = models.CharField(max_length= 100, default= "0")
    
    tag            = models.TextField(default= "")  
    types_blog     = models.CharField(max_length = 20, choices = type_blog, default = 'trả lời')
    
    
    def __str__(self):
        return self.title + f" -- Tác giả[{self.reporter.reporter_id.username}]"
    
    
    def show_tag(self):
        str_tag = self.tag.split("#")[1:]
        for i in range(len(str_tag)):
            str_tag[i] = "#" + str_tag[i]
        return str_tag
        
    
    
    
    class Meta:
        ordering = ['-pub_date']
    
    
class Commented(models.Model):
    
    reporter = models.ForeignKey(Reporter, on_delete= models.CASCADE)
    article  = models.ForeignKey(Article, on_delete = models.CASCADE)
    
    content  = models.TextField(blank= False, null= False)
    
    pub_date = models.DateField(auto_now_add=True)
    # pub_date = models.DateField(default= date.today)
    
    def __str__(self):
        print(self.article.types_blog)
        return self.reporter.__str__() + " Đã " + self.article.types_blog + " " + self.article.__str__()
    
    
    
class Groups_User(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    group_name = models.CharField(max_length= 20)
    
    def __str__(self):
        return self.group_name