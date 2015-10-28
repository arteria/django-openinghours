from django.shortcuts import render_to_response


def current_openings(request):
    return render_to_response('openinghours/index.html', {}) 