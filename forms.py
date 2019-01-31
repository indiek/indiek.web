from django import forms
from .models import dbTopic, dbItem

class itemForm(forms.ModelForm):
    class Meta:
        model = dbItem
        fields = ('quickname', 'description', 'item_url', 'topics', )

    def __init__(self, user, *args, **kwargs):
        super(itemForm, self).__init__(*args, **kwargs)
        self.fields['topics'].queryset = dbTopic.objects.filter(author=user)
