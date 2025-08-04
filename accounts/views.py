from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import CustomUserCreationForm
from django.db.models import Sum
import datetime
from youtube.models import AccountInfo, Video
from youtube.forms import VideoForm
    
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'계정 {username}이(가) 생성되었습니다! 이제 로그인할 수 있습니다.')
            return redirect('accounts:login')
    else:
        # 사용자가 이미 로그인한 경우, 대시보드로 리디렉션
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def dashboard(request):
    # 데이터베이스에서 첫 번째 계정 정보를 가져옵니다. (없으면 None)
    account_info = AccountInfo.objects.first()
    # 데이터베이스에서 최신 비디오 3개를 가져옵니다.
    latest_videos = Video.objects.order_by('-uploaded_at')[:3]

    # 전체 비디오에 대한 통계 계산
    total_views = Video.objects.aggregate(total=Sum('views'))['total'] or 0
    total_duration_seconds = Video.objects.aggregate(total=Sum('duration'))['total'] or datetime.timedelta(0)
    # 초 단위를 시간 단위로 변환
    total_watch_hours = total_duration_seconds.total_seconds() / 3600

    context = {
        'info': account_info,
        'latest_videos': latest_videos,
        'total_views': total_views,
        'total_watch_hours': total_watch_hours,
    }
    return render(request, 'youtube/index.html', context)

@login_required
def contents(request):
    # 데이터베이스에서 모든 비디오를 최신순으로 가져옵니다.
    all_contents = Video.objects.all().order_by('-uploaded_at')
    context = {'contents': all_contents}
    return render(request, 'youtube/contents.html', context)

@login_required
def analysis(request):
    # 데이터베이스에서 모든 비디오를 가져옵니다.
    # 이제 수익 예측 및 시간 포맷팅은 Video 모델의 프로퍼티에서 처리됩니다.
    videos = Video.objects.all()
    context = {'videos': videos}
    return render(request, 'youtube/analysis.html', context)

@login_required
def video_add(request):
    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            # DB에 바로 저장하지 않고, video 객체를 임시로 생성합니다.
            # 'account' 필드를 수동으로 채워줘야 하기 때문입니다.
            new_video = form.save(commit=False)
            
            # 현재 채널 정보(AccountInfo의 첫 번째 객체)를 가져옵니다.
            account = AccountInfo.objects.first()
            if not account:
                messages.error(request, "동영상을 추가할 채널이 존재하지 않습니다. 먼저 채널을 생성해주세요.")
                return redirect('dashboard')

            new_video.account = account
            new_video.save() # 모든 정보가 채워졌으므로, 이제 DB에 최종 저장합니다.
            
            messages.success(request, f"'{new_video.title}' 영상이 성공적으로 추가되었습니다.")
            return redirect('accounts:contents')
    else: # GET 요청일 때
        form = VideoForm()
        
    return render(request, 'youtube/video_form.html', {'form': form, 'page_title': '새 동영상 추가'})

@login_required
def monetization(request):
    # 수익 창출 자격 요건
    SUBSCRIBER_GOAL = 1000
    WATCH_HOUR_GOAL = 4000

    account_info = AccountInfo.objects.first()
    current_subscribers = account_info.subscribers if account_info else 0

    # 최근 365일간의 공개 동영상 시청 시간 계산
    one_year_ago = timezone.now() - datetime.timedelta(days=365)
    recent_videos_duration = Video.objects.filter(
        uploaded_at__gte=one_year_ago,
        status=Video.Status.PUBLIC  # 공개 동영상만 필터링
    ).aggregate(total=Sum('duration'))['total'] or datetime.timedelta(0)

    current_watch_hours = recent_videos_duration.total_seconds() / 3600

    # 진행률 계산
    subscriber_progress = min((current_subscribers / SUBSCRIBER_GOAL) * 100, 100)
    watch_hour_progress = min((current_watch_hours / WATCH_HOUR_GOAL) * 100, 100)

    # 자격 요건 충족 여부
    is_eligible = (current_subscribers >= SUBSCRIBER_GOAL) and (current_watch_hours >= WATCH_HOUR_GOAL)

    context = {
        'current_subscribers': current_subscribers,
        'subscriber_goal': SUBSCRIBER_GOAL,
        'subscriber_progress': subscriber_progress,
        'current_watch_hours': round(current_watch_hours, 1), # 소수점 첫째 자리까지 표시
        'watch_hour_goal': WATCH_HOUR_GOAL,
        'watch_hour_progress': watch_hour_progress,
        'is_eligible': is_eligible,
    }
    return render(request, 'youtube/monetization.html', context)

@login_required
def video_update(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if request.method == 'POST':
        form = VideoForm(request.POST, instance=video)
        if form.is_valid():
            form.save()
            messages.success(request, f"'{video.title}' 영상 정보가 성공적으로 수정되었습니다.")
            return redirect('accounts:contents')
    else:
        form = VideoForm(instance=video)
    
    context = {
        'form': form,
        'page_title': f"'{video.title}' 정보 수정"
    }
    return render(request, 'youtube/video_form.html', context)

@login_required
def video_delete(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if request.method == 'POST':
        video_title = video.title
        video.delete()
        messages.info(request, f"'{video_title}' 영상이 삭제되었습니다.")
        return redirect('accounts:contents')
    # GET 요청 시에는 삭제 확인 페이지를 보여줍니다.
    return render(request, 'youtube/video_confirm_delete.html', {'video': video})
