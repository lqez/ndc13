from django import forms
from ndc.models import Profile


class EmailLoginForm(forms.Form):
    email = forms.EmailField(max_length=255, label='', widget=forms.TextInput(attrs={
        'placeholder': 'Email address',
        'class': 'span4',
    }))

    def clean(self):
        cleaned_data = super(EmailLoginForm, self).clean()
        return cleaned_data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user')
