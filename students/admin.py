from django.contrib import admin
from .models import (
    Major, Semester, Student,
    Subject, Chapter, PDFNote, YouTubeLink , Event
)

@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    list_display = ('name', 'description_short')
    search_fields = ('name', 'description')
    
    def description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_short.short_description = 'Description'

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('number',)
    ordering = ('number',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'semester', 'major', 'email')
    list_filter = ('major', 'semester', 'year')
    search_fields = ('name', 'email')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'major', 'semester', 'description_short')
    list_filter = ('major', 'semester')
    search_fields = ('name', 'description')
    
    def description_short(self, obj):
        return obj.description[:75] + '...' if len(obj.description) > 75 else obj.description
    description_short.short_description = 'Description'

class PDFNoteInline(admin.TabularInline):
    model = PDFNote
    extra = 1

class YouTubeLinkInline(admin.TabularInline):
    model = YouTubeLink
    extra = 1

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('name', 'chapter_number', 'subject', 'book_pdf_exists')
    list_filter = ('subject__major', 'subject__semester')
    inlines = [PDFNoteInline, YouTubeLinkInline]
    
    def book_pdf_exists(self, obj):
        return bool(obj.book_pdf)
    book_pdf_exists.boolean = True
    book_pdf_exists.short_description = 'Has PDF Book'

@admin.register(PDFNote)
class PDFNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'chapter_link', 'uploaded_at')
    search_fields = ('title', 'chapter__name')
    
    def chapter_link(self, obj):
        return obj.chapter.name
    chapter_link.short_description = 'Chapter'

@admin.register(YouTubeLink)
class YouTubeLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'chapter_link', 'thumbnail_preview')
    search_fields = ('title', 'chapter__name')
    
    def chapter_link(self, obj):
        return obj.chapter.name
    chapter_link.short_description = 'Chapter'
    
    def thumbnail_preview(self, obj):
        return obj.thumbnail if obj.thumbnail else 'Auto-generated'
    thumbnail_preview.short_description = 'Thumbnail'


from django.contrib import admin
from .models import PYQ  # Make sure to import your model

# Either use the decorator:
@admin.register(PYQ)
class PYQAdmin(admin.ModelAdmin):
    list_display = ('subject', 'year', 'exam_type', 'uploaded_at')
    search_fields = ('subject__name', 'year')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'link')
    search_fields = ('title', 'description')
