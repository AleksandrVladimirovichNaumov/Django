from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from feedbacks.models import Feedback


class FeedbackListView(ListView):

    model = Feedback
    template_name = 'feedbacks/feedbacks.html'

    # def get_queryset(self):
    #     return Feedback.objects.filter(user=self.request.user).select_related('user')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FeedbackListView, self).get_context_data()
        context['feedbacks'] = Feedback.objects.filter(user_id=self.request.user_id_id, product_id=self.request.product_id_id).select_related('user')