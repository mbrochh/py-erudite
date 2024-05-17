import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import IngestFromSource


@csrf_exempt
def ingest_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        url = data.get("url")
        title = data.get("title")
        authors = data.get("authors")

        source_type = "webpage"
        if "youtube.com" in url:
            source_type = "youtube"

        IngestFromSource.objects.create(
            source_type=source_type,
            source_url=url,
            title=title,
            authors=authors,
        )
        return JsonResponse({"status": "success"}, status=200)
    return JsonResponse({"status": "failure"}, status=400)
