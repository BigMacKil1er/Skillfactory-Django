

from django import forms
from .models import Advertisement, MediaContent, UserResponse


class CreateAdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ('title', 'text', 'category')

    # Добавьте поле для медиаконтента
    media_file = forms.FileField(label='Медиаконтент', required=False)

class AdvertisementFormEdit(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ('title', 'text')
    media_file = forms.FileField(label='Медиаконтент', required=False)
    # mediacontent = forms.ModelChoiceField(
    #     queryset=MediaContent.objects.filter(media_type='image'),
    #     widget=forms.Select(attrs={'class': 'form-control'}),
    # )

class MediaContentForm(forms.ModelForm):
    class Meta:
        model = MediaContent
        fields = ('media_type', 'media_file', 'advertisement')

class UserResponseForm(forms.ModelForm):
    class Meta:
        model = UserResponse
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget = forms.Textarea(attrs={'rows': 3})