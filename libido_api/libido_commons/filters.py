from rest_framework import generics
from django_filters import rest_framework as filters
from libido_rooms.models import Room


class MinMaxRoomFilter(filters.FilterSet):
    min_user_count = filters.NumberFilter(field_name="user_count", lookup_expr="gte")
    max_user_count = filters.NumberFilter(field_name="user_count", lookup_expr="lte")

    min_play_list_count = filters.NumberFilter(
        field_name="play_lists_count", lookup_expr="gte"
    )
    max_play_list_count = filters.NumberFilter(
        field_name="play_lists_count", lookup_expr="lte"
    )

    class Meta:
        model = Room
        fields = "__all__"


#         fields = [
#             "id",
#             "title",
#             "created_at"
#             "min_user_count",
#             "max_user_count",
#             "min_play_list_count",
#             "max_play_list_count",
#         ]
