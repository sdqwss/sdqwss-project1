from django import forms
from django.contrib.auth.models import User
from .models import Room


class GroupRoomForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        label="Участники"
    )

    class Meta:
        model = Room
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Название чата', 'required': True})
        }

    def __init__(self, *args, **kwargs):

        self.current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)

        if self.current_user:
            self.fields['members'].queryset = User.objects.exclude(pk=self.current_user.pk)
        else:
            self.fields['members'].queryset = User.objects.none()

    def save(self, commit=True):
        room = super().save(commit=False)
        if commit:
            room.save()

            room.members.add(self.current_user, *self.cleaned_data['members'])
            room.save()
        return room

members = forms.ModelMultipleChoiceField(
    queryset=User.objects.none(),
    widget=forms.CheckboxSelectMultiple,
    label="Участники",
    required=False
)