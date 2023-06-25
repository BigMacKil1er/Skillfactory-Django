from django_filters import FilterSet, CharFilter, DateTimeFilter, ModelChoiceFilter
from django import forms
from .models import Post, Author


class PostFilter(FilterSet):
    title = CharFilter(
        lookup_expr = 'icontains',
        widget = forms.TextInput(attrs={'class':'form-control'})
    )
    dateCreation = DateTimeFilter(
        lookup_expr = 'gt',
        widget = forms.DateInput(attrs={'class':'form-control', 'type': 'date', })
    )
    author = ModelChoiceFilter(
        queryset = Author.objects.all(),
        empty_label = "Все авторы",
        widget = forms.Select(attrs={'class': 'form-control'}),
    )
    class Meta:
        model: Post
        field: ('title', 'author', 'dateCreation')