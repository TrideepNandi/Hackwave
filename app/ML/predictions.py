import joblib
import numpy as np

def load_recommendation_model(vectorizer_path='tfidf_vectorizer.pkl',
                              matrix_path='tfidf_matrix.pkl',
                              model_path='yoga_recommendation_model.pkl'):
    # Load TF-IDF vectorizer
    tfidf_vectorizer = joblib.load(vectorizer_path)

    # Load TF-IDF matrix
    tfidf_matrix = joblib.load(matrix_path)

    # Load trained model
    model = joblib.load(model_path)

    return tfidf_vectorizer, tfidf_matrix, model

def recommend_yoga_practices(user_diseases, vectorizer, matrix, model):
    user_input = vectorizer.transform([user_diseases])
    predictions_proba = model.predict_proba(user_input)
    top_indices = np.argsort(predictions_proba[0])[-5:][::-1]  # Get top 5 predictions
    recommendations = [model.classes_[idx] for idx in top_indices]
    return recommendations

# Example usage
def get_yoga_recommendations(user_diseases):
    vectorizer, matrix, model = load_recommendation_model()
    recommendations = recommend_yoga_practices(user_diseases, vectorizer, matrix, model)
    return recommendations

user_diseases = "high blood pressure"
recommendations = get_yoga_recommendations(user_diseases)
print("Recommended yoga practices:", recommendations)
