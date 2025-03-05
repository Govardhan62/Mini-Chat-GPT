import google.generativeai as genai
from django.shortcuts import render
from django.http import JsonResponse

# Set up Gemini API Key
genai.configure(api_key="AIzaSyBPvSVmsCfXkxzHqN6dBEGAw5GZ3Ag2ZIk")

# List available models
models = genai.list_models()
for model in models:
    print(model.name)  # Print model names

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Store session-based chat history
def get_chat_history(request):
    if "chat_history" not in request.session:
        request.session["chat_history"] = []
    return request.session["chat_history"]

def chatbot(request):
    return render(request, "chatbot.html")

def ask_gemini(request):
    if request.method == "POST":
        user_message = request.POST.get("message", "").strip()

        if not user_message:
            return JsonResponse({"message": "Please enter a message!"})

        # Retrieve chat history
        chat_history = get_chat_history(request)
        chat_history.append(f"You: {user_message}")

        # Generate response
        response = model.generate_content(user_message)

        # Extract the text response
        bot_message = response.text.strip() if response and response.text else "I couldn't understand that."

        # Append bot response to history
        chat_history.append(f"Bot: {bot_message}")
        request.session["chat_history"] = chat_history  # Save session

        return JsonResponse({"message": bot_message})
