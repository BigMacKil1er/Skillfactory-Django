from django.forms import ModelForm, CheckboxSelectMultiple, ModelMultipleChoiceField
from .models import Category

class SubscribeForm(ModelForm):
    name = ModelMultipleChoiceField(
        label='Категория',
        queryset=Category.objects.all(),
        widget=CheckboxSelectMultiple(attrs={'class': 'py-sm-1'})
    )
    class Meta:
        model = Category
        fields = ['name']