from rest_framework.views import APIView
from rest_framework.response import Response
from app.ML.predictions import get_yoga_recommendations

class YogaRecommendationsView(APIView):
    def get(self, request, user_diseases, format=None):
        recommendations = get_yoga_recommendations(user_diseases)
        return Response({'recommendations': recommendations})
