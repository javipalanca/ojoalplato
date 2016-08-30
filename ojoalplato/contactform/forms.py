# forms.py
from envelope.forms import ContactForm as EnvelopeContactForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class ContactForm(EnvelopeContactForm):
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Enviar', css_class='btn-lg fb-lile-btn social-buttons'))
