from django.urls import path

from .views import projects_list_view, workspace_view

app_name = "projects"

urlpatterns = [
    path("", workspace_view, name="workspace"),
    path("partials/sidebar-list/", projects_list_view, name="projects_list"),
]
