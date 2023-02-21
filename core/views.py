from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from core.models import Block, Convict
from django.db.models import Q
from rest_framework.decorators import api_view
import json
from django.core.files import File


class Home(ListView):
    model = Block
    template_name = "core/home.html"


class CreateConvict(LoginRequiredMixin, CreateView):
    model = Convict
    fields = ["name", "aliases", "gender", "place_of_birth", "date_of_birth", "education", "financial_background"]
    success_url = reverse_lazy("home")
    template_name = "core/createconvict.html"


class CreateBlock(LoginRequiredMixin, CreateView):
    model = Block
    fields = [
        "perp",
        "charges",
        "charges_code",
        "known_accomplices",
        "fir_date",
        "conviction_date",
        "comments",
        "sentencer",
        "sentence",
    ]
    success_url = reverse_lazy("home")
    template_name = "core/createblock.html"


class SearchView(LoginRequiredMixin, ListView):
    model = Convict
    template_name = "core/search.html"
    context_object_name = "abc"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Call the base implementation first to get a context
        convict_id = self.request.GET.get("convict_id")
        convict_name = self.request.GET.get("convict_name")
        crime_id = self.request.GET.get("crime_id")

        context["convict_id"] = convict_id
        context["convict_name"] = convict_name
        context["crime_id"] = crime_id

        print("convict_id", context["convict_id"]) if context["convict_id"] != "" else print()
        print("convict_name", context["convict_name"]) if context["convict_name"] != "" else print()
        print("crime_id", context["crime_id"]) if context["crime_id"] != "" else print()

        if crime_id != "":
            try:
                q = get_object_or_404(Block, pk=crime_id)
                # q=Block.objects.get(Q(pk=crime_id))
                context["crime"] = q
                print(context["crime"])
                context["search_hint"] = f"Match found for crime id - {crime_id}"
            except:
                pass

        elif convict_id != "":
            try:
                q = Convict.objects.filter(Q(pk=convict_id))
                q = get_object_or_404(Convict, pk=convict_id)
                # q=Block.objects.get(Q(pk=crime_id))
                context["convict"] = q
                print(context["convict"])
                context["search_hint"] = f"Match found for convict id - {convict_id}"
            except:
                pass

        elif convict_name != "":
            q = Convict.objects.filter(Q(name__icontains=convict_name) | Q(aliases__icontains=convict_name))
            context["convict_list"] = q
            context["search_hint"] = f"Match found for convict name - {convict_name}"

        # if not context['search_hint']:
        # context['search_hint']="No results found, redefine search"

        return context


class BlockDetailView(LoginRequiredMixin, DetailView):
    model = Block
    # template_name='core/blockdetailview.html'


class ConvictDetailView(LoginRequiredMixin, DetailView):
    model = Convict
    # template_name='core/convictdetailview.html'


# Create your views here.
def page_not_found_view(request, exception):
    return render(request, "core/404.html", status=404)
