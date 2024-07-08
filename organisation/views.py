from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.views import APIView

from .models import Organisation
from .serializers import OrganisationSerializer



class OrganisationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        organisations = request.user.organisations.all()
        serializer = OrganisationSerializer(organisations, many=True)
        return Response({
            'status': 'success',
            'message': 'Organisations retrieved successfully',
            'data': {'organisations': serializer.data}
        }, status=status.HTTP_200_OK)


class OrganisationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get (self, request, orgId):
        organisation = Organisation.objects.filter(orgId=orgId, users=request.user).first()
        if organisation:
            serializer = OrganisationSerializer(organisation)
            return Response({
                'status': 'success',
                'message': 'Organisation retrieved successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'status': 'Forbidden',
            'message': 'Access denied',
            'statusCode': 403
        }, status=status.HTTP_403_FORBIDDEN)


class OrganisationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrganisationSerializer(data=request.data)
        if serializer.is_valid():
            organisation = serializer.save()
            organisation.users.add(request.user)
            return Response({
                'status': 'success',
                'message': 'Organisation created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'Bad Request',
            'message': 'Client error',
            'statusCode': 400,
            'errors': [{'field': key, 'message': value[0]} for key, value in serializer.errors.items()]
        }, status=status.HTTP_400_BAD_REQUEST)


class AddUserToOrganisationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, orgId):
        organisation = Organisation.objects.filter(orgId=orgId, users=request.user).first()
        if not organisation:
            return Response({
                'status': 'Unauthorized',
                'message': 'Access denied',
                'statusCode': 401,
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        userId = request.data.get('userId')
        user = User.objects.filter(userId=userId).first()
        if user:
            organisation.users.add(user)
            return Response({
                'status': 'success',
                'message': 'User added to organisation successfully',
            }, status=status.HTTP_200_OK)
        return Response({
            'status': 'Bad Request',
            'message': 'User not found',
            'statusCode': 400,
        }, status=status.HTTP_400_BAD_REQUEST)

