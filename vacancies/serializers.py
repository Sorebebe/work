from rest_framework import serializers


class VacancySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    company = serializers.CharField(max_length=200)
    sphere = serializers.CharField(max_length=20)
    sphere_display = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)