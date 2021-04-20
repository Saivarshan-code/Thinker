from django import forms
from .models import question,comment

class questionform(forms.ModelForm):


    class Meta():
        model = question
        fields = ('title','description','category','image1','image2','image3','file','question')

        widgets = {
            'title':forms.TextInput(attrs={'placeholder':'Title','class':'titleinput'}),
            'question':forms.Textarea(attrs={'class':'question'}),
            'description':forms.TextInput(attrs={'placeholder':"please enter a short description"})
        }

class YourForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(YourForm, self).__init__(*args, **kwargs)
        self.fields['question'].strip = False

    class Meta:
        model = question
        fields = ('title','description','category','image1','image2','image3','file','question')

        widgets = {
            'title':forms.TextInput(attrs={'placeholder':'Title','class':'titleinput'}),
            'question':forms.Textarea(attrs={'placeholder':'actual question','class':'question'}),
            'description':forms.Textarea(attrs={'placeholder':"please enter a short description and not the actual question within 150 words",'rows':4})
        }




class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['comment'].strip = False

    class Meta:
        model = comment
        fields = ('comment','image1','image2','file')

        widgets = {
            'comment':forms.Textarea(attrs={'title':'Answer','help_text':'Comment'})
        }

class SearchForm(forms.Form):
    answer = forms.CharField(widget=forms.Textarea(attrs={"rows":5,"cols":20,'label':'Give your answer'}))
