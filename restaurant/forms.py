from django import forms
from .models import Reservation, Review


class ReservationForm(forms.ModelForm):
    reserve_start = forms.DateTimeField(
        input_formats=['%m/%d/%Y %I:%M %p'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'}
        )
    )
    reserve_end = forms.DateTimeField(
        input_formats=['%m/%d/%Y %I:%M %p'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker2'}
        )
    )

    class Meta:
        model = Reservation
        fields = ['reserve_start', 'reserve_end']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content']