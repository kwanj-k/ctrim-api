"""
File contains all store related helper
functions
"""
from apps.stores.models import Store

def user_stores(request):
    """
    Get stores related to a particular user
    """
    user = request.user
    queryset = Store.objects.filter(
        owner=user
    )
    if len(queryset) < 1:
        all_stores = Store.objects.all()
        for i in all_stores:
            staff = Staff.objects.filter(
                store=i.pk
            ).first()
            try:
                user.username == staff.username
                store = staff.store
                queryset = Store.objects.filter(
                    pk=store.pk
                )
            except:
                continue
    return queryset
