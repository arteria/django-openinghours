from django.shortcuts import render_to_response



def currentOpenings(request):
    return render_to_response('openinghours/index.html', {}) 