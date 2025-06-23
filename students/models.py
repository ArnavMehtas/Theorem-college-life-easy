from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
class Major(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Semester(models.Model):
    number = models.IntegerField(unique=True)

    def __str__(self):
        return f"Semester {self.number}"

class Student(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    semester = models.IntegerField()
    email = models.EmailField(max_length=100)
    major = models.ForeignKey(Major, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.major.name}, Semester{self.semester})"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    major = models.ForeignKey(Major, on_delete=models.CASCADE)
    semester = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return f"{self.name} (Sem {self.semester}, {self.major.name})"

from django.db import models

class Chapter(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="chapters")
    name = models.CharField(max_length=200)
    chapter_number = models.IntegerField()
    book_pdf = models.FileField(upload_to='chapter_books/', blank=True, null=True)

    def __str__(self):
        return f"Chapter {self.chapter_number}: {self.name} ({self.subject.name})"

class PDFNote(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="pdf_notes")
    title = models.CharField(max_length=200)
    pdf_file = models.FileField(upload_to='notes_pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.chapter.name}"

class YouTubeLink(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="youtube_links")
    title = models.CharField(max_length=200)
    url = models.URLField()
    thumbnail = models.URLField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        # Extract YouTube video ID for thumbnail
        if 'youtube.com' in self.url or 'youtu.be' in self.url:
            video_id = self.url.split('v=')[1].split('&')[0] if 'v=' in self.url else self.url.split('/')[-1]
            self.thumbnail = f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} - {self.chapter.name}"
    
class PYQ(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    year = models.CharField(max_length=20)
    exam_type = models.CharField(max_length=100)  # e.g., "Midterm", "Final"
    pdf_file = models.FileField(upload_to='pyqs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject.name} - {self.year} {self.exam_type}"

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    link = models.URLField()
    banner = models.ImageField(upload_to='event_banners/', blank=True, null=True)  # optional

    def __str__(self):
        return self.title
