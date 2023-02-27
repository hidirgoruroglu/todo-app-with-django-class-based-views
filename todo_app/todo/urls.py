from django.urls import path
from .views import TaskListView,TaskDetailView,TaskCreateView,TaskUpdateView,TaskDeleteView,CustomLoginView,RegisterView
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path("",TaskListView.as_view(),name="task_list_view"),
    path("login/", CustomLoginView.as_view(), name="custom_login_view"),
    path("logout/", LogoutView.as_view(next_page="custom_login_view"), name="custom_logout_view"),
    path("register/", RegisterView.as_view(), name="register_view"),
    path("task/<int:pk>/",TaskDetailView.as_view(),name="task_detail_view"),
    path("task/create/",TaskCreateView.as_view(),name="task_create_view"),
    path("task/update/<int:pk>/",TaskUpdateView.as_view(),name="task_update_view"),
    path("task/delete/<int:pk>/",TaskDeleteView.as_view(),name="task_delete_view"),
]
