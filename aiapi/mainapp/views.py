from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ChatSession
import uuid
import json
import requests

# Create your views here.
from groq import Groq


@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        session_id = data.get("session_id")
        user_message = data.get("message")

        if not session_id:
            session_id = str(uuid.uuid4())
            chat_session = ChatSession.objects.create(session_id=session_id)
        else:
            chat_session = ChatSession.objects.filter(session_id=session_id).first()
            if not chat_session:
                return JsonResponse({"error": "Invalid session ID"}, status=400)

        # Add user message to the session
        chat_session.messages.append({"role": "user", "content": user_message})
        chat_session.save()

        # Call Groq AI API
        client = Groq(
            api_key="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",
        )

        try:
            chat_completion = client.chat.completions.create(
                messages=chat_session.messages,
                model="llama-3.3-70b-versatile",
            )
            bot_message = (
                chat_completion.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
            )

            # Add bot message to the session
            chat_session.messages.append({"role": "bot", "content": bot_message})
            chat_session.save()

            return JsonResponse({"session_id": session_id, "message": bot_message})
        except Exception as e:
            return JsonResponse(
                {"error": f"Failed to fetch response from Groq AI: {str(e)}"},
                status=500,
            )

    return JsonResponse({"error": "Invalid request method"}, status=405)
