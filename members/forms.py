from django import forms
from django.contrib.auth.forms import (PasswordChangeForm, UserChangeForm,
                                       UserCreationForm)
from django.utils.safestring import mark_safe

from .models import City, State, User, UserProfile


class SignUpForm(UserCreationForm):              
	username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))  
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))                              																						
	first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))                                                                    
	last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))  
	# last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))  
	# last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))  

	
	class Meta:                                                                                         
		model = User                                                                                      
		fields = ('username', 'email', 'first_name', 'last_name', 'state', 'city', 'password1', 'password2')  

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('Email already used')
		return email

	def __init__(self, *args, **kwargs):                                    
		super(SignUpForm, self).__init__(*args, **kwargs)                    
		self.fields['username'].widget.attrs['class'] = 'form-control'            
		self.fields['password1'].widget.attrs['class'] = 'form-control'      
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'      
		self.fields['password2'].widget.attrs['class'] = 'form-control'  
		self.fields['password2'].widget.attrs['placeholder'] = 'Re-Enter Password'       
		self.fields['city'].queryset = City.objects.none()
		self.fields['city'].widget.attrs['class'] = 'form-control' 
		if 'state' in self.data:
			try:
				state_id = int(self.data.get('state'))
				self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('name')
			except (ValueError, TypeError):
				pass  
		elif self.instance.pk:
			self.fields['city'].queryset = self.instance.state.city_set.order_by('name')
		self.fields['state'].widget.attrs['class'] = 'form-control' 



class PasswordChangingForm(PasswordChangeForm):                                                                                                                                                                    
	old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'old password'}))                          																						
	new_password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))                                                                 
	new_password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))          

	class Meta:                                                                                                                                      
		model = User                                                                                     
		fields = ('old_password', 'new_password1', 'new_password2')  



class EditProfileForm(UserChangeForm):                                  										
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))                              																						
	username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))   
	first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))                                                                     
	last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))                                                                    

	class Meta:                                                                                         
		model = User                                                                                    
		fields = ('username', 'email', 'first_name', 'last_name', 'state', 'city', 'password')   

	def __init__(self, *args, **kwargs):                                    
		super(EditProfileForm, self).__init__(*args, **kwargs)   
		self.fields['city'].queryset = City.objects.none()  
		if 'state' in self.data:
			try:
				state_id = int(self.data.get('state'))
				self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('name')
			except (ValueError, TypeError):
				pass  
		elif self.instance.pk:
			self.fields['city'].queryset = self.instance.state.city_set.order_by('name')   


class ProfilePageForm(forms.ModelForm):		
	class Meta:																							
		model = UserProfile 
		fields = ('first_name', 'last_name', 'bio', 'picture', 'website_url', 'birth_date', 'location', 'facebook_url', 'twitter_url', 'instagram_url')
		widgets = {                                                                                                                                                                                                        
			'first_name': forms.TextInput(attrs={'placeholder': 'optional', 'class': 'form-control'}),                                                                                                                                                                                                         
			'last_name': forms.TextInput(attrs={'class': 'form-control'}),       
			'bio': forms.Textarea(attrs={'class': 'form-control'}),  
			'picture': forms.ImageField(required=False),  
			'birth_date': forms.Textarea(attrs={'class': 'form-control'}),                                                                                                                                  
			'location': forms.Textarea(attrs={'class': 'form-control'}),                                                                                                                                                                                                                                                                  
			'website_url': forms.TextInput(attrs={'class': 'form-control'}),                                                                    
			'facebook_url': forms.TextInput(attrs={'class': 'form-control'}),                                                                    
			'twitter_url': forms.TextInput(attrs={'class': 'form-control'}),                                                                    
			'instagram_url': forms.TextInput(attrs={'class': 'form-control'}),                                                                    
			# 'pinterest_url': forms.TextInput(attrs={'class': 'form-control'}),                                                                    
		}
