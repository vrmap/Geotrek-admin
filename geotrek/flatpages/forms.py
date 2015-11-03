import floppyforms as forms
from django.utils.translation import ugettext_lazy as _
from geotrek.common.forms import CommonForm
from geotrek.flatpages.models import FlatPage
from modeltranslation.settings import AVAILABLE_LANGUAGES


class FlatPageForm(CommonForm):
    content = forms.CharField(widget=forms.TextInput, label=_(u"Content"))

    def __init__(self, *args, **kwargs):
        super(FlatPageForm, self).__init__(*args, **kwargs)
        self.fields['source'].help_text = None

    class Meta:
        model = FlatPage
        fields = ('title', 'published', 'source', 'external_url', 'target', 'content')

    def clean(self):
        cleaned_data = super(FlatPageForm, self).clean()
        for lang in AVAILABLE_LANGUAGES:
            external_url = cleaned_data.get('external_url_' + lang, None)
            if external_url is not None and len(external_url) > 0:
                if 'content_' + lang in self.errors:
                    self.errors.pop('content_' + lang)
        return cleaned_data