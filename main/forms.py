from django import forms

    
class BmiForm(forms.Form):
    height = forms.IntegerField(max_value=300, required=True, label="height")
    weight = forms.IntegerField(max_value=500, required=True, label="weight")
