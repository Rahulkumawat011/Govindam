from django import forms
from django.core.validators import RegexValidator
from .models import ContactRequest, Product

class ContactRequestForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '10-Digit Mobile Number',
        })
    )
    
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Business Email Address (Optional)',
        })
    )
    
    product = forms.ChoiceField(
        choices=[],  # Populated dynamically in __init__
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )
    
    quantity = forms.IntegerField(
        min_value=1,
        initial=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Required Quantity (e.g. 500)',
        })
    )

    message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Explain your requirements / specifications in detail (Optional)...',
            'rows': 4,
        })
    )

    class Meta:
        model = ContactRequest
        fields = ['name', 'company_name', 'phone', 'email', 'product', 'quantity', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name',
            }),
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company / Board Name (Optional)',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Standard product categories list
        default_categories = [
            'Tower Cross Arm', 'Cross Arm', 'Stay Set', 'Clamps',
            'Brackets', 'Channels', 'Angles', 'MS Structures',
            'Steel Fabrication', 'Custom Fabrication'
        ]
        
        choices = [('', 'Select Product Category')]
        seen = set()
        
        try:
            active_products = Product.objects.filter(status='published').order_by('order')
            for p in active_products:
                if p.title not in seen:
                    choices.append((p.title, p.title))
                    seen.add(p.title)
        except Exception:
            pass

        for cat in default_categories:
            if cat not in seen:
                choices.append((cat, cat))
                seen.add(cat)
                
        self.fields['product'].choices = choices

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        # Clean out spaces, dashes, + symbol
        cleaned = phone.replace(' ', '').replace('-', '').replace('+', '')
        if cleaned.startswith('91') and len(cleaned) == 12:
            cleaned = cleaned[2:]
        elif cleaned.startswith('0') and len(cleaned) == 11:
            cleaned = cleaned[1:]
            
        if not cleaned.isdigit() or len(cleaned) != 10 or cleaned[0] not in '6789':
            raise forms.ValidationError("Please enter a valid 10-digit Indian mobile number.")
        return cleaned

    def clean_message(self):
        msg = self.cleaned_data.get('message', '').strip()
        if not msg:
            product = self.cleaned_data.get('product') or 'Hardware Product'
            qty = self.cleaned_data.get('quantity') or 100
            msg = f"Quick inquiry request for {product} (Required Quantity: {qty})."
        return msg

