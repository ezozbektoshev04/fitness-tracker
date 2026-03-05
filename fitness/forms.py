from django import forms
from .models import WorkoutPlan, WorkoutLog


class WorkoutPlanForm(forms.ModelForm):
    class Meta:
        model = WorkoutPlan
        fields = ['title', 'description', 'exercises']
        widgets = {
            'exercises': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class WorkoutLogForm(forms.ModelForm):
    class Meta:
        model = WorkoutLog
        fields = ['workout_plan', 'date_completed', 'duration_minutes', 'notes']
        widgets = {
            'date_completed': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['workout_plan'].queryset = WorkoutPlan.objects.filter(user=user)
