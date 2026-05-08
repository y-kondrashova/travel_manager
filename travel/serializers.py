from django.db import transaction
from rest_framework import serializers
from .models import TravelProject, ProjectPlace
from .services.art_institute import ArtInstituteService
from .services.exceptions import (
    ArtworkNotFoundError,
    ExternalAPIError,
)


class ProjectPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPlace
        fields = ["id", "external_id", "title", "notes", "visited", "created_at"]
        read_only_fields = ["id", "title", "created_at"]

    def validate(self, attrs):

        external_id = attrs.get("external_id")

        if not external_id:
            return attrs

        try:
            artwork = ArtInstituteService.get_artwork(external_id)

        except ArtworkNotFoundError as e:
            raise serializers.ValidationError(str(e))

        except ExternalAPIError as e:
            raise serializers.ValidationError(str(e))

        attrs["artwork"] = artwork

        return attrs

    def create(self, validated_data):
        artwork = validated_data.pop("artwork")
        validated_data["title"] = artwork["title"]

        return super().create(validated_data)


class TravelProjectSerializer(serializers.ModelSerializer):
    places = ProjectPlaceSerializer(many=True, read_only=True)

    class Meta:
        model = TravelProject
        fields = [
            "id",
            "name",
            "description",
            "start_date",
            "completed",
            "places",
            "created_at",
        ]

        read_only_fields = ["id", "completed", "created_at"]


class TravelProjectCreateSerializer(serializers.ModelSerializer):

    places = ProjectPlaceSerializer(many=True)

    class Meta:
        model = TravelProject
        fields = ["id", "name", "description", "start_date", "places"]

    @staticmethod
    def validate_places(value):

        if len(value) < 1:
            raise serializers.ValidationError(
                "Project must contain at least one place."
            )

        if len(value) > 10:
            raise serializers.ValidationError(
                "Project cannot contain more than 10 places."
            )

        external_ids = [place["external_id"] for place in value]

        if len(set(external_ids)) != len(external_ids):
            raise serializers.ValidationError("Duplicate places are not allowed.")

        return value

    @transaction.atomic
    def create(self, validated_data):

        places_data = validated_data.pop("places")

        project = TravelProject.objects.create(**validated_data)

        for place_data in places_data:
            serializer = ProjectPlaceSerializer(data=place_data)
            serializer.is_valid(raise_exception=True)
            serializer.save(project=project)

        return project
