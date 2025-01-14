from django.contrib import admin
from .models import (
    HR_Candidate, 
    HR_Position, 
    HR_Status,
    TimezoneDifference,
)


@admin.register(TimezoneDifference)
class TimezoneDifferenceAdmin(admin.ModelAdmin): 
    list_display = ['difference'] 


@admin.register(HR_Candidate)
class HR_CandidateAdmin(admin.ModelAdmin): 
    list_display = ['name', 'status', 'requested_datetime']


@admin.register(HR_Position)
class HR_PositionAdmin(admin.ModelAdmin): 
    list_display = ['name']


@admin.register(HR_Status)
class HR_StatusAdmin(admin.ModelAdmin): 
    list_display = ['name'] 
