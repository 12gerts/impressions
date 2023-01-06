from django import forms
from .models import RememberModel


class RememberModelForm(forms.ModelForm):
    class Meta:
        model = RememberModel
        fields = ['title', 'location', 'body']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'id': 'remember_title',
                                            'placeholder': 'Каникулы в Бразилии'}),
            'location': forms.TextInput(attrs={'class': 'form-control',
                                               'id': 'remember_location',
                                               'placeholder': 'Поставьте точку на карте'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'id': 'remember_body',
                                          'placeholder': 'Описание'})
        }

    def save_form(self, profile):
        new_remember = RememberModel.objects.update_or_create(
            title=self.cleaned_data['title'],
            location=self.cleaned_data['location'],
            body=self.cleaned_data['body'],
            profile=profile
        )
        return new_remember