from django.urls import path
from .views import index, by_rubric, BbCreateView, BbDetailView, add_and_save,\
        BbEditView, BbIndexView, BbMonthArchiveView, BbRedirectView

urlpatterns = [
    path('add/', add_and_save, name='add'),
    path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('detail/<int:pk>', BbDetailView.as_view(), name='detail'),
    path('detail/<int:year>/<int:month>/<int:day>/<int:pk>/', BbRedirectView.as_view(), name='old_detail'),
    path('update/<int:pk>', BbEditView.as_view(), name='update'),
    path('<int:year>/<int:month>/', BbMonthArchiveView.as_view()),
    path("", BbIndexView.as_view(), name='index'),
]

