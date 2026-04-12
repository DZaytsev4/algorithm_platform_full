from rest_framework import serializers
from .models import Algorithm

class AlgorithmSerializer(serializers.ModelSerializer):
    # В запросе может приходить из фронта (копия логина), источник истины при create — request.user
    author_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    tags_list = serializers.SerializerMethodField()
    can_edit = serializers.SerializerMethodField()
    can_moderate = serializers.SerializerMethodField()

    class Meta:
        model = Algorithm
        fields = [
            'id', 'name', 'tegs', 'description', 'code', 'author_name',
            'status', 'status_display', 'moderated_by', 'moderated_at',
            'rejection_reason', 'created_at', 'updated_at', 'tags_list',
            'can_edit', 'can_moderate'
        ]
        read_only_fields = [
            'id', 'moderated_by', 'moderated_at',
            'created_at', 'updated_at', 'status_display', 'tags_list',
            'can_edit', 'can_moderate'
        ]

    def get_tags_list(self, obj):
        return obj.get_tags_list()

    def get_can_edit(self, obj):
        request = self.context.get('request')
        if request:
            return obj.can_edit(request.user)
        return False

    def get_can_moderate(self, obj):
        request = self.context.get('request')
        if request:
            return obj.can_moderate(request.user)
        return False

    def create(self, validated_data):
        """
        Автор всегда из JWT (request.user), не из тела запроса — защита от подмены.
        Тело может дублировать username для совместимости/логов.
        """
        request = self.context.get('request')
        validated_data.pop('author_name', None)
        if request and request.user and request.user.is_authenticated:
            validated_data['author_name'] = request.user.username
        else:
            validated_data['author_name'] = 'anonymous'
        validated_data.setdefault('status', Algorithm.STATUS_PENDING)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        При обновлении — если алгоритм был одобрен/отклонён — сбрасываем модерацию.
        Автора через API менять нельзя.
        """
        validated_data.pop('author_name', None)
        if instance.status in [Algorithm.STATUS_APPROVED, Algorithm.STATUS_REJECTED]:
            instance.reset_moderation()
        return super().update(instance, validated_data)
