from django.contrib.auth.models import Group


def user_groups(request):
    is_admin = is_manager = is_customer = False
    if request.user.is_authenticated:
        groups = request.user.groups.values_list('name', flat=True)
        print(f"Groups: {groups}")  # Для налагодження
        is_admin = 'administrator' in groups
        is_manager = 'manager' in groups
        is_customer = 'user' in groups
    print(f"is_admin: {is_admin}")
    print(f"is_manager: {is_manager}")
    print(f"is_customer: {is_customer}")
    # Для налагодження
    return {
        'is_admin': is_admin,
        'is_manager': is_manager,
        'is_customer': is_customer,
    }
