from django.db.models import Q
from django.views.generic import ListView
from products.models import Product


# Create your views here.

class SearchProductView(ListView):
    template_name = 'search/view.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        query = request.GET.get('q', None)
        print(query)
        if query is not None:
            lookup = Q(title__icontains=query) | Q(description__icontains=query)
        return Product.objects.filter(lookup).distinct()
