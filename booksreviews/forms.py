from django import forms
from .models import Post
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.models import User

# モデル名_form.htmlで自動的にformを認識してくれる 
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields =('title','content','category',)
    
    #htmlのタグにクラスを追加する
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = 'form-control'


class LoginForm(AuthenticationForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = 'form-control'

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email','password1','password2')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = 'form-control'

class SearchForm(forms.Form):
    freeword = forms.CharField(min_length = 1,max_length=30, label ='',required=False)

    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)


        