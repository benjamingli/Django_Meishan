# coding=utf8
from django import forms


WEATHER_CHOICES=(
  (0, '晴'),
  (1, '晴转多云'),
  (2, '阴'),
  (3, '阴有小雨'),
  (4, '雨')
)

class WeatherForm(forms.Form):
    date = forms.DateField(
        label='日期',
        widget=forms.TextInput(attrs={
            'onfocus': "MyCalendar.SetDate(this)",
        })
    )
    holiday = forms.BooleanField(required=False, label='节假日')
    maxTemp = forms.CharField(label='最高气温')
    minTemp = forms.CharField(label='最低气温')
    typeDay = forms.ChoiceField(choices=WEATHER_CHOICES, label='天气类别')

class ResultForm(forms.Form):
    date = forms.DateField(
        label='日期',
        widget=forms.TextInput(attrs={
            'onfocus': "MyCalendar.SetDate(this)",
        })
    )
