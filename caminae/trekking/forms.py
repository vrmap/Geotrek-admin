from django.utils.translation import ugettext as _
from django.conf import settings

import floppyforms as forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Layout, Submit, HTML

from caminae.core.forms import TopologyMixinForm
from caminae.core.widgets import PointWidget, LineTopologyWidget, PointTopologyWidget
from caminae.mapentity.widgets import SelectMultipleWithPop

from .models import Trek, POI, WebLink


class TrekForm(TopologyMixinForm):
    parking_location = forms.gis.GeometryField(widget=PointWidget)

    modelfields = (
            'name',
            'departure',
            'arrival',
            'published',
            'difficulty',
            'route',
            'destination',
            'description_teaser',
            'description',
            'ambiance',
            'disabled_infrastructure',
            'duration',
            'is_park_centered',
            'is_transborder',
            'advised_parking',
            'parking_location',
            'public_transport',
            'advice',
            'themes',
            'main_themes',
            'networks',
            'usages',
            'web_links',
            )

    def __init__(self, *args, **kwargs):
        super(TrekForm, self).__init__(*args, **kwargs)
        self.fields['topology'].widget = LineTopologyWidget()
        self.fields['web_links'].widget = SelectMultipleWithPop(
												choices=self.fields['web_links'].choices, 
												add_url=WebLink.get_add_url())

    class Meta(TopologyMixinForm.Meta):
        model = Trek


class POIForm(TopologyMixinForm):
    modelfields = (
            'name',
            'description',
            'type',
            )

    def __init__(self, *args, **kwargs):
        super(POIForm, self).__init__(*args, **kwargs)
        self.fields['topology'].widget = PointTopologyWidget()

    class Meta(TopologyMixinForm.Meta):
        model = POI


class WebLinkCreateFormPopup(forms.ModelForm):
    helper = FormHelper()

    def __init__(self, *args, **kwargs):
        super(WebLinkCreateFormPopup, self).__init__(*args, **kwargs)
        self.helper.form_action = self.instance.get_add_url()
        # Main form layout
        self.helper.form_class = 'form-horizontal'
        arg_list = ['name_{0}'.format(l[0]) for l in settings.LANGUAGES]
        arg_list += ['url', 'thumbnail', FormActions(
            HTML('<a href="#" class="btn" onclick="javascript:window.close();">%s</a>' % _("Cancel")),
            Submit('save_changes', _('Create'), css_class="btn-primary"),
            css_class="form-actions",
        )]
        self.helper.layout = Layout(*arg_list)
    class Meta:
        model = WebLink
        exclude = ('name',)