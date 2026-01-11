from rest_framework import serializers
from .models import ErrorReport  

class StatusSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=100)
    date = serializers.DateTimeField()



class ErrorSerializer(serializers.ModelSerializer):
    """
    Serializer for ErrorReport model
    """
    class Meta:
        model = ErrorReport
        fields = ['id', 'code', 'description', 'date']