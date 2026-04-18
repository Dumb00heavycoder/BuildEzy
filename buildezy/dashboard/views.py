from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project
from .ai_service import generate_project_details
import json

@login_required
def dashboard_view(request):
    # Get all projects for the logged-in user
    projects = Project.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard/dashboard.html', {'projects': projects})

@login_required
def create_project_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        
        if name and description:
            # 1. Ask Gemini to generate the data
            ai_data = generate_project_details(name, description)
            
            # 2. Extract and format the data
            todos = json.dumps(ai_data.get('todos', []))
            progress = ai_data.get('progress', '')
            stats = json.dumps(ai_data.get('stats', []))
            vision = ai_data.get('vision', '')

            # 3. Save to the database
            project = Project.objects.create(
                user=request.user,
                name=name,
                description=description,
                ai_todos=todos,
                ai_progress=progress,
                ai_stats=stats,
                ai_vision=vision
            )
            
            # Redirect to the specific project detail view
            return redirect('project_detail', project_id=project.id)
            
    return render(request, 'dashboard/create_project.html')

@login_required
def project_detail_view(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    
    # Parse the strings back into Python objects
    todos = []
    stats = []
    try:
        if project.ai_todos:
            todos = json.loads(project.ai_todos)
        if project.ai_stats:
            stats = json.loads(project.ai_stats)
    except json.JSONDecodeError:
        pass
        
    context = {
        'project': project,
        'todos': todos,
        'stats': stats,
    }
    return render(request, 'dashboard/project_detail.html', context)
