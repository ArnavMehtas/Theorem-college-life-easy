from django.shortcuts import render, get_object_or_404
from .models import *

def home(request):
    return render(request, 'students/home.html', {
        "Majors": Major.objects.all()
    })

def major_detail(request, major_id):
    major = get_object_or_404(Major, id=major_id)
    semester = request.GET.get('semester')
    
    # Get distinct semesters as integers
    semesters = Subject.objects.filter(
        major=major
    ).order_by('semester').values_list('semester', flat=True).distinct()

    subjects = []
    if semester and semester.isdigit():
        subjects = Subject.objects.filter(
            major=major, 
            semester=int(semester)
        )

    return render(request, 'students/major_detail.html', {
        'major': major,
        'subjects': subjects,
        'selected_semester': semester,
        'semesters': semesters
    })

def subject_detail(request, subject_id):
    subject = get_object_or_404(
        Subject.objects.prefetch_related('chapters__pdf_notes', 'chapters__youtube_links'), 
        id=subject_id
    )
    chapters = subject.chapters.order_by('chapter_number')
    return render(request, 'students/subject_detail.html', {
        'subject': subject,
        'chapters': chapters
    })


from django.shortcuts import render
def welcome_view(request):
    context = {
        'stats': {
            'members': "1,400+",
            'visitors': "3,500+", 
            'study_groups': "1000+"
        },
        'features': [
            {
                'icon': 'book-open',
                'title': 'Study Resources',
                'desc': 'Curated lectures and materials',
                'url': '/students/welcome/'  # Added URL
            },
            
            {'icon': 'file-pdf', 
             'title': 'PYQ Bank',
             'desc': 'Access previous year question papers',
             'url': '/students/subjects/'
             }
             ,
            {
                'icon': 'brain',
                'title': 'Cgpa Calculator',
                'desc': 'Practice with PYQs in real exam conditions',
                'url': '/students/cgpa-calculator/'  # Added URL
            },
            {'icon': 'calendar-alt', 
             'title': 'Events',
             'desc': 'Upcoming events',
             'url': '/students/events/'  
             },
            {
                'icon': 'users', 
                'title': 'Community',
                'desc': 'Connect with students',
                'url': 'telegram-community/'  # Added URL
            }
            
        ]
    }
    return render(request, 'students/landing.html', context)

def cgpa_calculator(request):
    if request.method == 'POST':
        sgpais = request.POST.getlist('sgpa')  # Get list of SGPAs from form
        sgpais = [float(sgpa) for sgpa in sgpais if sgpa]  # Convert to floats
        
        if sgpais:
            cgpa = sum(sgpais) / len(sgpais)
            return render(request, 'students/cgpa_result.html', {
                'cgpa': round(cgpa, 2),
                'sgpais': sgpais
            })
    
    return render(request, 'students/cgpa_calculator.html')

def telegram_community(request):
    context = {
        'telegram_link': 'https://t.me/+zs3sFjntWvo4MGZl',  # Replace with your actual link
        'member_count': '5,000+',  # Update with real numbers
        'features': [
            'Instant help from seniors',
            'Subject-specific channels',
            'Placement discussion',
            'PYQ sharing',
            '24/7 active community'
        ]
    }
    return render(request, 'students/telegram_community.html', context)


def subject_pyqs(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    pyqs = PYQ.objects.filter(subject=subject).order_by('-year')
    
    return render(request, 'students/subject_pyqs.html', {
        'subject': subject,
        'pyqs': pyqs
    })

from django.db.models import Q

def subject_search(request):
    query = request.GET.get('q', '')
    
    if query:
        subjects = Subject.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        ).distinct()
    else:
        subjects = Subject.objects.all()
    
    return render(request, 'students/subject_search.html', {
        'subjects': subjects,
        'search_query': query
    })

def events_page(request):
    events = Event.objects.order_by('-date')
    return render(request, 'students/events.html', {'events': events})
