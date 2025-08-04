from django import forms
from .models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        # 사용자가 직접 입력할 필드들을 지정합니다.
        fields = ['title', 'thumbnail_url', 'status', 'views', 'likes', 'duration']
        # 폼 필드의 라벨을 한글로 변경합니다.
        labels = {
            'title': '영상 제목',
            'thumbnail_url': '썸네일 이미지 URL',
            'status': '공개 상태',
            'views': '조회수',
            'likes': '좋아요 수',
            'duration': '영상 길이',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'thumbnail_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'views': forms.NumberInput(attrs={'class': 'form-control'}),
            'likes': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '예: 00:05:30'}),
        }
        help_texts = {
            'duration': 'HH:MM:SS 형식으로 입력하세요. (예: 5분 30초는 00:05:30)'
        }