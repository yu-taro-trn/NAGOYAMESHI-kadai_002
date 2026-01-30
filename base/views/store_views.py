from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render
from base.models import Store, StoreCategory
from base.models.store_models import Review
from django.db.models import Avg

def home(request):
    stores = Store.objects.filter(is_published=True).order_by("-created_at")

    store_categories = (
        StoreCategory.objects
        .select_related("category")
        .order_by("category__sort_order", "category__id")
    )

    stores = stores.prefetch_related(
        Prefetch("storecategory_set", queryset=store_categories)
    )

    return render(request, "stores/list.html", {"stores": stores})


def store_list(request):
    return home(request)


def store_detail(request, store_id: int):
    return render(request, "stores/detail.html", {})


def store_detail(request, store_id: int):
    store = get_object_or_404(Store, pk=store_id, is_published=True)

    categories = (
        StoreCategory.objects
        .filter(store=store)
        .select_related("category")
        .order_by("category__sort_order", "category__id")
    )

    reviews = (
        Review.objects
        .filter(store=store, is_published=True)
        .select_related("user")
        .order_by("-created_at")
    )

    avg_rating = reviews.aggregate(avg=Avg("rating"))["avg"]

    return render(
        request,
        "stores/detail.html",
        {
            "store": store,
            "categories": categories,
            "reviews": reviews,
            "avg_rating": avg_rating,
        },
    )