from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 필드 라벨 및 도움말 텍스트를 한글로 직접 지정합니다.
        self.fields['username'].label = '사용자 이름'
        self.fields['username'].help_text = '필수. 150자 이하. 문자, 숫자, @/./+/-/_ 만 사용 가능합니다.'
        self.fields['password1'].label = '비밀번호'
        self.fields['password2'].label = '비밀번호 확인'
        self.fields['password2'].help_text = '확인을 위해 비밀번호를 다시 한번 입력해주세요.'

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 로그인 필드에 placeholder 추가
        self.fields['username'].widget.attrs.update(
            {'placeholder': '사용자 이름'}
        )
        self.fields['password'].widget.attrs.update(
            {'placeholder': '비밀번호'}
        )