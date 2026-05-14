from .models import UserProfile


def get_user_role(user):
    try:
        return user.userprofile.role
    except UserProfile.DoesNotExist:
        return None


def is_organizer(user):
    return get_user_role(user) == "organizer"


def is_manager(user):
    return get_user_role(user) == "manager"


def is_organizer_or_manager(user):
    return get_user_role(user) in ["organizer", "manager"]