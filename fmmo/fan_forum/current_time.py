from datetime import datetime


def get_current_time(request):
    return {'current_time': datetime.now()}