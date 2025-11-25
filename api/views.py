from rest_framework.response import Response
from rest_framework.decorators import api_view
from .utils import get_analysis

@api_view(['POST'])
def analyze(request):
    area = request.data.get("query", "")
    summary, chart, table = get_analysis(area)
    return Response({
        "summary": summary,
        "chart": chart,
        "table": table
    })
