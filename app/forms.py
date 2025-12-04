from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Apt, Amounts, Info, Coords, Images

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'John'})
    )
    last_name = forms.CharField(
        max_length=150, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Doe'})
    )
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'placeholder': 'john@example.com'})
    )
    contact_number = forms.CharField(
        max_length=20, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': '+1 (555) 123-4567'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'contact_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'johndoe123'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm password'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomSignupForm(CustomUserCreationForm):
    # Add a dropdown menu for user type
    user_type = forms.ChoiceField(choices=UserProfile.USER_TYPES, label="I am a")
    # contact_number is inherited from CustomUserCreationForm; only define role-specific fields here
    company_name = forms.CharField(required=False, max_length=255)
    properties_count = forms.IntegerField(required=False, min_value=0)
    budget = forms.IntegerField(required=False, min_value=0)
    move_in_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta(CustomUserCreationForm.Meta):
        model = User
        fields = ('first_name','last_name','email','username','password1','password2','user_type','contact_number','company_name','properties_count','budget','move_in_date')

    def save(self, commit=True):
        # Save the user first
        user = super().save(commit=False)
        if commit:
            user.save()
            # Then create their profile with additional fields
            user_type = self.cleaned_data.get('user_type')
            contact = self.cleaned_data.get('contact_number')
            company = self.cleaned_data.get('company_name')
            count = self.cleaned_data.get('properties_count')
            budget = self.cleaned_data.get('budget')
            move_in = self.cleaned_data.get('move_in_date')
            UserProfile.objects.create(
                user=user,
                user_type=user_type,
                contact_number=contact,
                company_name=company,
                properties_count=count,
                budget=budget,
                move_in_date=move_in
            )
        return user


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = ('contact_number', 'company_name', 'properties_count', 'budget', 'move_in_date')
        widgets = {
            'contact_number': forms.TextInput(attrs={'placeholder': '+1 (555) 123-4567'}),
            'company_name': forms.TextInput(attrs={'placeholder': 'Your Company'}),
            'properties_count': forms.NumberInput(attrs={}),
            'budget': forms.NumberInput(attrs={'placeholder': '0'}),
            'move_in_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
        self.user_instance = user

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user_instance:
            self.user_instance.first_name = self.cleaned_data.get('first_name')
            self.user_instance.last_name = self.cleaned_data.get('last_name')
            self.user_instance.email = self.cleaned_data.get('email')
            if commit:
                self.user_instance.save()
        if commit:
            profile.save()
        return profile


class AptForm(forms.ModelForm):
    class Meta:
        model = Apt
        fields = ('name', 'address')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Property name (e.g., Luxury 3BHK)', 'class': 'form-input'}),
            'address': forms.TextInput(attrs={'placeholder': 'Full address', 'class': 'form-input'}),
        }


class AmountsForm(forms.ModelForm):
    class Meta:
        model = Amounts
        fields = ('minimum', 'maximum')
        widgets = {
            'minimum': forms.NumberInput(attrs={'placeholder': '0', 'class': 'form-input'}),
            'maximum': forms.NumberInput(attrs={'placeholder': '0', 'class': 'form-input'}),
        }


class InfoForm(forms.ModelForm):
    class Meta:
        model = Info
        fields = ('phone_number', 'url')
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': '+1 (555) 123-4567', 'class': 'form-input'}),
            'url': forms.URLInput(attrs={'placeholder': 'https://example.com', 'class': 'form-input'}),
        }


class CoordsForm(forms.ModelForm):
    class Meta:
        model = Coords
        fields = ('lat', 'long')
        widgets = {
            'lat': forms.NumberInput(attrs={'placeholder': 'Latitude', 'class': 'form-input', 'step': 'any'}),
            'long': forms.NumberInput(attrs={'placeholder': 'Longitude', 'class': 'form-input', 'step': 'any'}),
        }


class ImagesForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ('src',)
        widgets = {
            'src': forms.URLInput(attrs={'placeholder': 'Image URL (e.g., https://example.com/image.jpg)', 'class': 'form-input'}),
        }