from django.urls import path
from . import views

urlpatterns = [
    path('', views.ModelView.as_view()),
    path('filter/', views.FilterModelsView.as_view(), name='filter'),
    path('search/', views.Search.as_view(), name='search'),
    path('add-rating/', views.AddStarRating.as_view(), name='add_rating'),
    path('<slug:slug>/', views.ModelDetailView.as_view(), name='model_detail'),
    path('review/<int:pk>/', views.AddReview.as_view(), name='add_review'),
    path('racer/<str:slug>/', views.RacerView.as_view(), name='racer_detail'),
]