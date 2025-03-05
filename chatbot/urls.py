from django.urls import path
from .views import chatbot, ask_gemini

urlpatterns = [
    path("", chatbot, name="chatbot"),
    path("ask_gemini/", ask_gemini, name="ask_gemini"),
]
