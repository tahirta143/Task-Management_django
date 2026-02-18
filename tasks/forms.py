from django import forms
from .models import Task
from core.models import User

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'assigned_to']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
        if user and not (user.is_manager() or user.is_admin()):
            # Staff can only update status
            for field_name in ['title', 'description', 'priority', 'assigned_to']:
                if field_name in self.fields:
                    self.fields[field_name].disabled = True
            
        # Filter assigned_to to only show active users or staff/managers if needed
        # self.fields['assigned_to'].queryset = User.objects.filter(is_active=True)
