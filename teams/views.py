from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .models import Team, TeamMembership
from .serializers import (
    TeamSerializer,
    TeamMembershipCreateSerializer,
    TeamMembershipUpdateSerializer,
    TeamMembershipListSerializer,
    TeamMembershipDetailSerializer,
)


class TeamViewSet(ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamMembershipViewSet(ModelViewSet):
    queryset = TeamMembership.objects.select_related("team", "user")

    def get_serializer_class(self):
        if self.action == "create":
            return TeamMembershipCreateSerializer

        if self.action in ["update", "partial_update"]:
            return TeamMembershipUpdateSerializer

        if self.action == "list":
            return TeamMembershipListSerializer

        return TeamMembershipDetailSerializer

    def _update_membership(self, request, partial=False):
        instance = self.get_object()

        serializer = TeamMembershipUpdateSerializer(
            instance,
            data=request.data,
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        output_serializer = TeamMembershipDetailSerializer(instance)
        return Response(output_serializer.data)

    def update(self, request, *args, **kwargs):
        return self._update_membership(request, partial=False)

    def partial_update(self, request, *args, **kwargs):
        return self._update_membership(request, partial=True)