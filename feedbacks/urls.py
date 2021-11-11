from django.urls import path

from baskets.views import basket_add, basket_remove, basket_edit
from feedbacks.views import FeedbackListView

app_name = 'feedbacks'
urlpatterns = [

    path('feedback/<int:product_id>', FeedbackListView.as_view(), name='feedback'),

]
