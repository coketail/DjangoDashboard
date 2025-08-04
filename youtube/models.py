from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

class AccountInfo(models.Model):
    name = models.CharField(max_length=50)
    subscribers = models.PositiveIntegerField(default=0)
    revenue = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Video(models.Model):
    class Status(models.TextChoices):
        PUBLIC = 'Public', '공개'
        PRIVATE = 'Private', '비공개'
        UNLISTED = 'Unlisted', '일부 공개'

    account = models.ForeignKey(AccountInfo, on_delete=models.CASCADE, related_name='videos')

    title = models.CharField(max_length=100)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(default=timezone.now, verbose_name="업로드 날짜")
    duration = models.DurationField(default=datetime.timedelta(seconds=0), verbose_name="영상 길이")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PRIVATE, verbose_name="공개 상태")
    thumbnail_url = models.URLField(blank=True, null=True, help_text="영상 썸네일 이미지 URL")

    def __str__(self):
        return self.title

    @property
    def formatted_duration(self):
        """영상 길이를 MM:SS 형식의 문자열로 반환합니다."""
        minutes = int(self.duration.total_seconds() // 60)
        seconds = int(self.duration.total_seconds() % 60)
        return f"{minutes:02d}:{seconds:02d}"

    @property
    def predicted_revenue(self):
        """임의의 공식으로 예상 수익을 계산하여 정수로 반환합니다."""
        revenue = (self.views * 0.5) + (self.likes * 10) + ((self.duration.total_seconds() / 60) * 50)
        return int(revenue)