"""
When working with forms: 
1) Ensure that GET requests (and other ‘safe’ methods, as defined by RFC 7231#section-4.2.1) are side effect free.)
2) In any template that uses a POST form, use the csrf_token tag inside the <form> element if the form is for an internal URL, e.g.:
    <form method="post">{% csrf_token %}</form>

Read more: https://docs.djangoproject.com/en/3.2/ref/csrf/
"""
from django import forms
from .models import Blockchain, Block, Miner


class BlockchainForm(forms.ModelForm):
    """ Form used to create a blockchain """
    class Meta:
        model = Blockchain
        fields = ['creator_name','title']
        labels = {'creator_name': 'Dit navn', 'title': 'Hvad skal vi kalde blokkæden?', }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': "2A's chatbeskeder"}),
        }


class JoinForm(forms.ModelForm):
    """ Form used to join a blockchain """
    blockchain_id = forms.CharField(max_length=8, label="Blokkæde-ID",
                                help_text="Indtast ID'et på den blokkæde, du vil deltage i")

    class Meta:
        model = Miner
        fields = ['name']
        labels = {
            'name': 'Dit navn',
        }
        help_texts = {
            'name': 'Navnet, du vælger her, vil være synligt for de andre deltagere i blokkæden',
        }

    def clean_blockchain_id(self):
        """ Additional validation of the form's blockchain_id field """
        blockchain_id = self.cleaned_data['blockchain_id'].lower()
        if not Blockchain.objects.filter(id=blockchain_id).exists():
            raise forms.ValidationError(
                'Der findes ingen blokkæde med dette ID.')
        return blockchain_id

    def clean(self):
        """
        Additional validation of form data:
        Validate that there are no other users on the blockchain with the chosen username
        """
        cleaned_data = super().clean()
        cleaned_name = cleaned_data.get("name")
        cleaned_blockchain_id = cleaned_data.get('blockchain_id')
        if cleaned_name and cleaned_blockchain_id:
            blockchain = Blockchain.objects.get(id=cleaned_blockchain_id)
            if Miner.objects.filter(name=cleaned_name, blockchain=blockchain).exists():
                raise forms.ValidationError(
                    'Der er allerede en minearbejder med dette navn i blokkæden. Vælg et andet navn.')
        return cleaned_data



class BlockForm(forms.ModelForm):
    """ Form used to create a block """
    class Meta:
        model = Block
        fields = ['nonce']

    def clean_nonce(self):
        """ Nonce has to be an integer """
        nonce = self.cleaned_data['nonce']
        if nonce:
            if not str(nonce).isnumeric():
                raise forms.ValidationError(
                    'Nonce skal være et heltal')
        return nonce
