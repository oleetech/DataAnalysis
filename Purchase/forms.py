# app_name/forms.py
from django import forms

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='CSV File', required=True)
    start_date = forms.CharField(label='Start Date', widget=forms.TextInput(attrs={'type': 'text'}), required=True)
    end_date = forms.CharField(label='End Date', widget=forms.TextInput(attrs={'type': 'text'}), required=True)
    def __init__(self, *args, **kwargs):
        super(CSVUploadForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control form-control-sm',
                'id': f"{field_name}",
            })    
