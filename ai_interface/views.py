from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import http.client
import json

@csrf_exempt
def ai_endpoint(request):
    if request.method == 'POST':
        input_text = request.POST.get('input_text')
        
        conn = http.client.HTTPSConnection("api.baicaigpt.com")
        payload = json.dumps({
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": input_text}
            ]
        })
        headers = {
            'Authorization': 'Bearer bacai-eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtb2JpbGUiOiIxODI2MjI4Mjg0MyIsImV4cCI6MTcyMjQ0ODI5MTAxNCwiaWF0IjoxNzE5MzI2MjI3fQ.-YvKq5bhjedAR6eCIgHt-y7PaDDkKSD6_hpohYX6oE0',
            'Content-Type': 'application/json'
        }
        conn.request("POST", "/v1/chat/completions", payload, headers)
        res = conn.getresponse()
        data = res.read()
        response_data = json.loads(data.decode("utf-8"))
        ai_response = response_data['choices'][0]['message']['content']
        return JsonResponse({'text': ai_response})
    return JsonResponse({'error': 'Invalid request method.'}, status=405)
