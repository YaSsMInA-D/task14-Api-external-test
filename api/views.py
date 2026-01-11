from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .models import ErrorReport
from .serializers import StatusSerializer, ErrorSerializer


@api_view(['GET'])
def get_server_status(request):
    return Response(StatusSerializer(
        {'status': 'running', 'date': datetime.now()}
    ).data)


@api_view(['GET'])
def get_errors(request):
    errors = ErrorReport.objects.all()
    return Response(ErrorSerializer(errors, many=True).data)


@api_view(['GET'])
def get_error_from_code(request, code):
    try:
        error = ErrorReport.objects.get(code=code)
    except ErrorReport.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(ErrorSerializer(error).data)


@api_view(['POST'])
def create_error(request):
    serializer = ErrorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def error_update_delete(request, id):
    try:
        error = ErrorReport.objects.get(id=id)
    except ErrorReport.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ErrorSerializer(error, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        error.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)