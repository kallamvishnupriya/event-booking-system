from .models import UserProfile


def is_organizer(user):
    try:
        return user.userprofile.role == "organizer"
    except:
        return False


def is_manager(user):
    try:
        return user.userprofile.role == "manager"
    except:
        return False


def is_organizer_or_manager(user):
    try:
        return user.userprofile.role in ["organizer", "manager"]
    except:
        return False