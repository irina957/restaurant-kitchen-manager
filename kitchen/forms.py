from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from kitchen.models import Dish, Cook


def validate_experience(value):
    if value is not None and value < 0:
        raise forms.ValidationError("Years of experience cannot be negative.")
    return value


class CookCreationForm(UserCreationForm):
    years_of_experience = forms.IntegerField(
        min_value=0,
        validators=[validate_experience],
        label="Years of experience"
    )


    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "years_of_experience",)


class CookExperienceUpdateForm(forms.ModelForm):
    years_of_experience = forms.IntegerField(
        min_value=0,
        validators=[validate_experience],
        label="Years of experience"
    )

    class Meta:
        model = get_user_model()
        fields = ("years_of_experience",)


class DishForm(forms.ModelForm):
    cooks = forms.ModelMultipleChoiceField(queryset=get_user_model().objects.all(),
                                           widget=forms.CheckboxSelectMultiple,
                                           required=False)
    class Meta:
        model = Dish
        fields = "__all__"


class DishSearchForm(forms.Form):
    name = forms.CharField(max_length=255, required=False, label="",
                            widget=forms.TextInput(attrs={"placeholder": "Search by name"}))
