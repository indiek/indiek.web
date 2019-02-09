from django import forms
from .models import dbTopic, dbItem

class ItemForm(forms.ModelForm):
    class Meta:
        model = dbItem
        fields = ('quickname', 'description', 'item_url', 'topics', )

# old attempt
#    def __init__(self, user, *args, **kwargs):
#        super(itemForm, self).__init__(*args, **kwargs)
#        self.fields['topics'].queryset = dbTopic.objects.filter(author=user)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['topics'].queryset = dbTopic.objects.filter(author=user)
