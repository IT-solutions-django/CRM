from django.shortcuts import render
from django.views import View 
from .models import (
    HR_Candidate,
    HR_Position,
    HR_Status, 
    TimezoneDifference,
)


class HRView(View): 
    template_name = 'hr/hr.html'
    def get(self, request): 
        candidates = HR_Candidate.objects.all()

        context = {
            'segment': 'hr', 

            
            'candidates': candidates,
        }

        return render(request, self.template_name, context)