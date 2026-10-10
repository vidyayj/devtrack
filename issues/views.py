import json

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Reporter, Issue, CriticalIssue, LowPriorityIssue

REPORTERS_FILE = settings.BASE_DIR / "reporters.json"
ISSUES_FILE = settings.BASE_DIR / "issues.json"


def read_json(path):
    with open(path, "r") as f:
        return json.load(f)


def write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def health(request):
    return HttpResponse("OK")


@csrf_exempt
def reporters(request):
    if request.method == "POST":
        return create_reporter(request)
    if request.method == "GET":
        return get_reporters(request)
    return JsonResponse({"error": "Method not allowed"}, status=405)


def get_reporters(request):
    reporters_list = read_json(REPORTERS_FILE)
    reporter_id = request.GET.get("id")

    if reporter_id is None:
        return JsonResponse(reporters_list, safe=False)

    try:
        reporter_id = int(reporter_id)
    except ValueError:
        return JsonResponse({"error": "id must be a number"}, status=400)

    for reporter in reporters_list:
        if reporter["id"] == reporter_id:
            return JsonResponse(reporter)

    return JsonResponse({"error": "Reporter not found"}, status=404)

def create_reporter(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    try:
        reporter = Reporter(data["id"], data["name"], data["email"], data["team"])
        reporter.validate()
    except KeyError as e:
        return JsonResponse({"error": f"Missing field: {e.args[0]}"}, status=400)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    reporters_list = read_json(REPORTERS_FILE)
    reporters_list.append(reporter.to_dict())
    write_json(REPORTERS_FILE, reporters_list)

    return JsonResponse(reporter.to_dict(), status=201)

@csrf_exempt
def issues(request):
    if request.method == "POST":
        return create_issue(request)
    if request.method == "GET":
        return get_issues(request)
    return JsonResponse({"error": "Method not allowed"}, status=405)
def get_issues(request):
    issues_list = read_json(ISSUES_FILE)
    issue_id = request.GET.get("id")
    status = request.GET.get("status")

    if issue_id is not None:
        try:
            issue_id = int(issue_id)
        except ValueError:
            return JsonResponse({"error": "id must be a number"}, status=400)

        for issue in issues_list:
            if issue["id"] == issue_id:
                return JsonResponse(issue)

        return JsonResponse({"error": "Issue not found"}, status=404)

    if status is not None:
        filtered = []
        for issue in issues_list:
            if issue["status"] == status:
                filtered.append(issue)
        return JsonResponse(filtered, safe=False)

    return JsonResponse(issues_list, safe=False)
def create_issue(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    try:
        values = (
            data["id"],
            data["title"],
            data["description"],
            data["status"],
            data["priority"],
            data["reporter_id"],
        )
    except KeyError as e:
        return JsonResponse({"error": f"Missing field: {e.args[0]}"}, status=400)

    if data["priority"] == "critical":
        issue = CriticalIssue(*values)
    elif data["priority"] == "low":
        issue = LowPriorityIssue(*values)
    else:
        issue = Issue(*values)

    try:
        issue.validate()
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    issues_list = read_json(ISSUES_FILE)
    issues_list.append(issue.to_dict())
    write_json(ISSUES_FILE, issues_list)

    response_data = issue.to_dict()
    response_data["message"] = issue.describe()
    return JsonResponse(response_data, status=201)