from braces.views import FormMessagesMixin
from envelope.views import ContactView

from django.utils.translation import ugettext_lazy as _

from ojoalplato.contactform.forms import ContactForm


class ContactFormView(FormMessagesMixin, ContactView):
    form_valid_message = _(u"Gracias por su mensaje.")
    form_invalid_message = _(u"Se ha encontrado un error en el formulario de contacto.")
    form_class = ContactForm
