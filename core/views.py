from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
import requests
from blockchain.views import mine_block
from core.models import Block, Convict
from django import forms
from django.db.models import Q
from rest_framework.decorators import api_view
import json
from django.core.files import File
from datetime import date


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


class Home(ListView):
    model = Block
    template_name = "core/home.html"


class CreateConvict(LoginRequiredMixin, CreateView):
    model = Convict
    fields = [
        "name",
        "aliases",
        "gender",
        "date_of_birth",
        "place_of_birth",
        "place_of_birth_type",
        "education",
        "financial_background",
        "family_record",
    ]

    def get_form(self, form_class=None):  # for dropdown
        form = super().get_form(form_class=form_class)
        form.fields["gender"] = forms.ChoiceField(choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")])
        form.fields["place_of_birth_type"] = forms.ChoiceField(choices=[("Urban", "Urban"), ("Rural", "Rural")])
        form.fields["education"] = forms.ChoiceField(
            choices=[
                ("", ""),
                ("Illiterate", "Illiterate"),
                ("school dropout", "school dropout"),
                ("school", "school"),
                ("graduate", "graduate"),
                ("post graduate", "post graduate"),
            ]
        )
        form.fields["financial_background"] = forms.ChoiceField(
            choices=[
                ("", ""),
                ("Below poverty", "Below poverty"),
                ("lower class", "lower class"),
                ("middle", "middle"),
                ("upper", "upper"),
            ]
        )
        form.fields["family_record"] = forms.ChoiceField(choices=[("", ""), ("Yes", "Yes"), ("No", "No")])
        return form

    success_url = reverse_lazy("home")
    template_name = "core/createconvict.html"


class CreateBlock(LoginRequiredMixin, CreateView):
    model = Block
    fields = [
        "perp",
        "charges",
        "charges_code",
        "crime_type",
        "known_accomplices",
        "fir_date",
        "conviction_date",
        "comments",
        "sentencer",
        "sentence",
    ]

    def get_form(self, form_class=None):  # for dropdown
        form = super().get_form(form_class=form_class)
        form.fields["crime_type"] = forms.ChoiceField(choices=[("Violent", "Violent"), ("Non-Violent", "Non-Violent")])
        return form

    success_url = reverse_lazy("home")
    template_name = "core/createblock.html"

    def form_valid(self, form):
        criminal_value = form.cleaned_data["perp"]
        list_crime = {
            "criminal_id": int(criminal_value.id),
            "name": str(criminal_value.name),
            "gender": str(criminal_value.gender),
            "dob": str(criminal_value.date_of_birth),
            "fin_status": str(criminal_value.financial_background),
            "education": str(criminal_value.education),
            "population": str(criminal_value.place_of_birth_type),
            "family_record": str(criminal_value.family_record),
            "crime": {
                "charges": str(form.cleaned_data["charges"]),
                "charges_code": str(form.cleaned_data["charges_code"]),
                "crime_type": str(form.cleaned_data["crime_type"]),
                "known_accomplices": str(form.cleaned_data["known_accomplices"]),
                "fir_date": str(form.cleaned_data["fir_date"]),
                "conviction_date": str(form.cleaned_data["conviction_date"]),
                "comments": str(form.cleaned_data["comments"]),
                "sentencer": str(form.cleaned_data["sentencer"]),
                "sentence": str(form.cleaned_data["sentence"]),
            },
        }
        headers = {"content-type": "application/json"}

        response = requests.post("http://127.0.0.1:8000/mine_block", data=json.dumps(list_crime), headers=headers)
        print(response.text)
        return super().form_valid(form)


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

        # print("convict_id", context["convict_id"]) if context["convict_id"] != "" else print()
        # print("convict_name", context["convict_name"]) if context["convict_name"] != "" else print()
        # print("crime_id", context["crime_id"]) if context["crime_id"] != "" else print()

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
