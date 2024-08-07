from django.urls import path, include
from apps.API import views

urlpatterns = [
    # Swagger
    path('', include('apps.API.swagger.urls')),

    # Main
    path('about/api', views.MainAPIView.as_view()),
    path('datetime/now/', views.DatetimeAPIView.as_view()),

    # Auth
    path('auth/signup/', views.SignupApiView.as_view()),
    path('auth/signin/', views.SiginApiView.as_view()),
    
    # Users
    path('users/', views.UsersListApiView.as_view()),
    
    # Blog, comment, like
    path('blogs/', views.BlogListCreateAPIView.as_view()),
    path('blogs/<int:id>/', views.BlogDetailAPIView.as_view()),
    path('blogs/<int:blog_id>/like/', views.LikeToggleAPIView.as_view()),
    path('blogs/<int:blog_id>/comments/', views.CommentListCreateAPIView.as_view()),
    path('comments/<int:id>/', views.CommentDetailAPIView.as_view()),
]