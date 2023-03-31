from django import forms
from .models import Algorithm

class AlgorithmForm(forms.ModelForm):
    GENRE_CHOICES = [
        ('test1','테스트1'),
        ('test2','테스트2'),
        ('test3','테스트3')
    ]
    genre = forms.ChoiceField(choices=GENRE_CHOICES)
    score = forms.FloatField(widget=forms.NumberInput(
        #기본태그에 속성 추가
        attrs={
            'min' :0,
            'max':5,
            'step':0.5
        }
    ))
    release_date = forms.DateField(widget=forms.DateInput(
        attrs={
            'type':'date',
        }
    ))
    class Meta:
        model = Algorithm
        fields = '__all__'