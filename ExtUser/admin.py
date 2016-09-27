from django.contrib import admin
from django.contrib.auth.models import Group
from django import forms
from ExtUser.models import ExtUser, ExtUserProfile
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput
    )

    class Meta:
        model = ExtUser
        fields = ('username', 'email')

    def clean_password2(self):

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = ExtUser
        fields = ('username', 'email', 'location',)

    def clean_password(self):
        return self.initial['password']


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email', 'birthday', 'location', 'gender', 'orientation', 'date_joined', 'is_admin')
    list_filter = ('is_admin', 'gender', 'orientation', 'date_joined')

    readonly_fields = ('date_joined',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info: ', {'fields': ('location', 'gender', 'orientation', 'birthday', 'date_joined')}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'is_staff')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'birthday', 'location', 'gender', 'orientation', 'password1', 'password2')

        }),
    )
    search_fields = ('username', 'email', 'location', 'date_joined')
    ordering = ('username', 'email')
    filter_horizontal = ()

admin.site.register(ExtUser, UserAdmin)
admin.site.unregister(Group)


@admin.register(ExtUserProfile)
class ExtUserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo', 'language')
    search_fields = ('user__username', 'language')
