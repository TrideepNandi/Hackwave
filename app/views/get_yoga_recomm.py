import csv
from rest_framework.views import APIView
from rest_framework.response import Response
from app.ML.predictions import get_yoga_recommendations
from app.models import Elder
import os


class YogaRecommendationsView(APIView):
    def post(self, request, format=None):
        # Get the user's medical history
        elder_id = int(request.data.get('id'))
        elder = Elder.objects.get(id=elder_id)
        elder_diseases = elder.medical_history
        print(elder_diseases)
        current_dir = os.path.dirname(__file__)

        # Navigate up one directory to reach the app directory
        app_dir = os.path.dirname(current_dir)

        # Navigate to the ML directory to access the CSV file
        csv_path = os.path.join(app_dir, 'ML', 'final_asan1_1.csv')

        # Load the asana data from the CSV file
        asana_data = {}
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                asana_data[row['AName']] = row

        # Get the recommended asanas
        recommended_asanas = get_yoga_recommendations(elder_diseases)

        # Get the full data for each recommended asana
        recommendations = [asana_data[asana] for asana in recommended_asanas if asana in asana_data]

        return Response({'recommendations': recommendations})
