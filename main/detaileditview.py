from django.views.generic.base import TemplateResponseMixin, ContextMixin, View
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import UpdateView, ModelFormMixin, ProcessFormView


class DetailEditView(SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView):
    template_name_suffix = '_form'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data(object=object))



