from django.http import HttpResponseForbidden
from django.shortcuts import render

from .models import Project


def projects_list_view(request) -> render:
    """
    View to render the project list in the sidebar using HTMX.
    Handles manual pagination and is optimized for partial updates.
    """
    # Only allow HTMX requests
    if not request.headers.get("HX-Request"):
        return HttpResponseForbidden("Forbidden: This endpoint is reserved for HTMX partial requests.")

    # Manual Pagination Logic via Query Params
    try:
        page = int(request.GET.get("page", 1))
    except ValueError:
        page = 1

    print(f"Fetching projects for page {page}...")  # Debugging statement

    page_size = 10
    start = (page - 1) * page_size
    end = page * page_size

    # Query: Filter by owner and order by creation date (newest)
    queryset = Project.objects.filter(owner=request.user).order_by("-is_pinned", "-created_at")

    # Fetch N+1 items to determine if a "Show More" button is needed
    projects_slice = queryset[start : end + 1]
    projects = list(projects_slice[:page_size])
    has_next = len(projects_slice) > page_size

    context = {
        "projects": projects,
        "next_page": page + 1 if has_next else None,
    }

    return render(request, "projects/projects_list.html", context)


def workspace_view(request) -> render:
    """
    Temporary view to render the Workspace and test the base layout.
    """
    return render(request, "projects/workspace.html")
