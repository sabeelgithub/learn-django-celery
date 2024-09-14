from rest_framework import serializers
from .models import Tip

class TipWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tip
        fields = [
            'tip_name'
            ]