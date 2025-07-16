from rest_framework import serializers
from .models import Template

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = '__all__'
        read_only_fields = ('template_id',)

    def validate_template_id(self, value):
        if Template.objects.filter(template_id=value).exists():
            raise serializers.ValidationError("template_id must be unique.")
        return value
