# base/views.py
from django.shortcuts import render
from django.db.models import Prefetch
from base.models import Store, StoreCategory


def home(request):
    stores = (
        Store.objects
        .filter(is_published=True)
        .order_by("-created_at")
    )

    store_categories = (
        StoreCategory.objects
        .select_related("category")
        .order_by("category__sort_order", "category__id")
    )

    stores = stores.prefetch_related(
        Prefetch("storecategory_set", queryset=store_categories)
    )

    return render(request, "stores/list.html", {"stores": stores})
