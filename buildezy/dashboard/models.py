from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    # AI generated fields (we use TextField to store parsed JSON or long text)
    ai_todos = models.TextField(blank=True, null=True)     # JSON string array
    ai_progress = models.TextField(blank=True, null=True)  # Text summarizing progress
    ai_stats = models.TextField(blank=True, null=True)     # JSON string of stats (name, percentage)
    ai_vision = models.TextField(blank=True, null=True)    # Detailed text mapping vision
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} by {self.user.username}"
