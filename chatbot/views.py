import google.generativeai as genai
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Set up Gemini API Key
genai.configure(api_key="AIzaSyBPvSVmsCfXkxzHqN6dBEGAw5GZ3Ag2ZIk")

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Store session-based chat history
def get_chat_history(request):
    if "chat_history" not in request.session:
        request.session["chat_history"] = []
    return request.session["chat_history"]

def chatbot(request):
    return render(request, "chatbot.html")

@csrf_exempt
def ask_gemini(request):
    if request.method == "POST":
        try:
            # Decode JSON data from request
            data = json.loads(request.body.decode("utf-8"))
            user_message = data.get("message", "").strip()

            if not user_message:
                return JsonResponse({"error": "Please enter a message!"}, status=400)

            # Retrieve chat history
            chat_history = get_chat_history(request)
            chat_history.append(f"You: {user_message}")

            # Generate response from Gemini API
            response = model.generate_content(user_message)

            # Extract the response text
            bot_message = response.text.strip() if response and response.text else "I couldn't understand that."

            # Append bot response to history
            chat_history.append(f"Bot: {bot_message}")
            request.session["chat_history"] = chat_history  # Save session

            return JsonResponse({"message": bot_message})  # Send JSON response

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
