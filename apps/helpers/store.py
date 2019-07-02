"""
File contains all store related helper
functions
"""
from apps.stores.models import Store
from apps.products.models import Product

def user_stores(request):
    """
    Get stores related to a particular user
    """
    user = request.user
    queryset = Store.objects.filter(
        owner=user
    )
    # if len(queryset) < 1:
    #     all_stores = Store.objects.all()
    #     for i in all_stores:
    #         try:
    #             staff = Staff.objects.filter(
    #             store=i.pk
    #             ).first()
    #             user.username == staff.username
    #             store = staff.store
    #             queryset = Store.objects.filter(
    #                 pk=store.pk
    #             )
    #         except:
    #             continue
    return queryset

def store_products(storename):
    store = Store.objects.get(name=storename)
    queryset = Product.objects.filter(
        store=store
    )
    return queryset

