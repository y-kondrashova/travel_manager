from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import TravelProject, ProjectPlace
from .serializers import (
    TravelProjectSerializer,
    TravelProjectCreateSerializer,
    ProjectPlaceSerializer,
)


class TravelProjectViewSet(viewsets.ModelViewSet):

    queryset = TravelProject.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return TravelProjectCreateSerializer

        return TravelProjectSerializer

    def destroy(self, request, *args, **kwargs):

        project = self.get_object()

        if project.places.filter(visited=True).exists():
            return Response(
                {"detail": "Cannot delete project with visited places."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().destroy(request, *args, **kwargs)


class ProjectPlaceViewSet(viewsets.ModelViewSet):

    serializer_class = ProjectPlaceSerializer

    def get_queryset(self):
        return ProjectPlace.objects.filter(
            project_id=self.kwargs["project_pk"]
        )

    def perform_create(self, serializer):
        project = get_object_or_404(
            TravelProject,
            pk=self.kwargs["project_pk"]
        )

        serializer.save(project=project)
