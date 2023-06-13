from django import forms

from progysat.models.models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            "firstname",
            "email",
            "country",
            "lastname",
            "subject",
            "message",
        ]

    agree = forms.BooleanField(
        required=True,
        error_messages={"required": "Vous devez accepter les conditions d'utilisation"},
    )
