from django.shortcuts import render

# Create your views here.

#cart
def cart_summary(request):
  return render(request,"cart_summary.html",{})

#checkout
def checkout(request):
  return render(request,"checkout.html",{})

#search
def search_view(request):
    query = request.GET.get("q")  # get ?q= value from URL
    results = []  # replace with real search logic (e.g. Product.objects.filter(...))

    if query:
        # Example if you had a Product model
        # results = Product.objects.filter(name__icontains=query)
        results = [f"Result for '{query}'"]  

    return render(request, "search_results.html", {"query": query, "results": results})
