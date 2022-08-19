from crispy_forms.layout import LayoutObject, TEMPLATE_PACK
from django.template.loader import render_to_string


"""
This is used to render an entire formset as though it was a single field.
Only for front end stuff rendering the Address Form inside the Registration Form
"""


class DynamicFormset(LayoutObject):
    template = "records/dynamic-formset.html"

    def __init__(self, formset_name_in_context, template=None):
        self.formset_name_in_context = formset_name_in_context
        self.fields = []

        if template:
            self.template = template

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
        formset = context[self.formset_name_in_context]
        return render_to_string(self.template, context={"formset": formset})
