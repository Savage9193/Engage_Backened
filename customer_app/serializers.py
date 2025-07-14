from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

    def validate_Email(self, value):
        # Exclude self in update
        customer_id = self.instance.id if self.instance else None
        if Customer.objects.exclude(id=customer_id).filter(Email=value).exists():
            raise serializers.ValidationError("A customer with this email already exists.")
        return value