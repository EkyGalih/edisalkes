

def main_processor(request):
    user = request.user
    return {
        'user' : user
    }