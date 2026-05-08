from rest_framework_nested import routers
from django.urls import path, include

from .views import TravelProjectViewSet, ProjectPlaceViewSet

router = routers.SimpleRouter()
router.register(r'projects', TravelProjectViewSet, basename='projects')

projects_router = routers.NestedSimpleRouter(
    router,
    r'projects',
    lookup='project'
)

projects_router.register(
    r'places',
    ProjectPlaceViewSet,
    basename='project-places'
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(projects_router.urls)),
]