import json
import os

from django.http import HttpResponseForbidden, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from dkcontrol import settings


@csrf_exempt
def deploy(request):
    if request.headers.get('Authorization') == settings.c.get('SETTINGS', 'DEPLOYMENT_TOKEN'):
        json_data = json.loads(request.body)
        print(f"Downloading new update ({json_data['tag']})")

        stream = os.popen('git pull')
        output = stream.read()
        print(output)

        stream = os.popen('python manage.py migrate')
        output = stream.read()
        print(output)

        with open("./main/__init__.py", "r") as r:  # Restart server by editing file
            lines = r.readlines()
        with open("./main/__init__.py", "w") as w:
            w.writelines([])
            w.writelines(lines)

        return HttpResponse("OK")
    else:
        return HttpResponseForbidden()
