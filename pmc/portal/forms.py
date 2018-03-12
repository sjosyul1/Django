from django import forms


#LoginForm takes inputs Username, Password
class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label='Username ')
    password = forms.CharField(max_length=50, widget=forms.PasswordInput,  label='Password ')

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if not username and not password :
            raise forms.ValidationError('Username and Password are Mandatory!')

#HomeForm takes inputs ProductModel
class HomeForm(forms.Form):
    modelno = forms.CharField(max_length=50, label='Search Product for Certification',
                              widget=forms.TextInput(attrs={'placeholder': 'Product Model'}))

    def clean(self):
        cleaned_data = super(HomeForm, self).clean()
        modelno = cleaned_data.get('modelno')

#RegisterForm handles all registration fields
class RegisterForm(forms.Form):
    name = forms.CharField(max_length=50,  label='Name ')
    address = forms.CharField(max_length=250, widget=forms.Textarea, label='Address ')
    emailid = forms.CharField(max_length=50, widget=forms.EmailInput,  label='Email ID ')
    phonenumber = forms.CharField(min_length=10, max_length=10, widget=forms.NumberInput(attrs={'placeholder': '4804804800'}),  label='Phone No ')
    contactperson = forms.CharField(max_length=50,  label='Contact Person ')
    username = forms.CharField(max_length=50, label='Username ')
    password = forms.CharField(max_length=50, widget=forms.PasswordInput,  label='Password ')
    usertypes = (('1', 'Manufacturer',), ('2', 'TestLab',))
    usertype = forms.ChoiceField(widget=forms.RadioSelect, choices=usertypes)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        name = cleaned_data.get('name')
        address = cleaned_data.get('address')
        emailid = cleaned_data.get('emailid')
        phonenumber = cleaned_data.get('phonenumber')
        contactperson = cleaned_data.get('contactperson')
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        usertype = cleaned_data.get('usertype')
        if not username and not password and not name and not address and not emailid and not phonenumber and not contactperson and not usertype:
            raise forms.ValidationError('All Fields are Mandatory!')


#AddForm handles product fields
class AddProdForm(forms.Form):
    prodmodel = forms.CharField(max_length=50, label='Product Model ')
#    manuname = forms.CharField(max_length=50) commented to check cookie
    modtech = forms.CharField(max_length=50,label='Module Technology ')
    manudate = forms.CharField(label='Manufactured Date',
                        widget=forms.TextInput(attrs={'placeholder': '2017-12-04'}))
 #   manudate = forms.CharField(max_length=10, attrs={'placeholder':'2017-12-04'})
    mIsc = forms.FloatField(required=True, label='Isc', max_value=100, min_value=0,
                                widget=forms.NumberInput(attrs={'id': 'form_mIsc', 'step': "0.01"}))
    mVoc = forms.FloatField(required=True, label='Voc', max_value=100, min_value=0,
                            widget=forms.NumberInput(attrs={'id': 'form_mVoc', 'step': "0.01"}))
    mImp = forms.FloatField(required=True, label='Imp', max_value=100, min_value=0,
                            widget=forms.NumberInput(attrs={'id': 'form_mImp', 'step': "0.01"}))
    mVmp = forms.FloatField(required=True, label='Vmp', max_value=100, min_value=0,
                            widget=forms.NumberInput(attrs={'id': 'form_mVmp', 'step': "0.01"}))
    mFF = forms.FloatField(required=True, label='FF',max_value=100, min_value=0,
                            widget=forms.NumberInput(attrs={'id': 'form_mFF', 'step': "0.01"}))
    mPmp = forms.FloatField(required=True, label='Pmp', max_value=1000, min_value=0,
                            widget=forms.NumberInput(attrs={'id': 'form_mPmp', 'step': "0.01"}))

    def clean(self):
        cleaned_data = super(AddProdForm, self).clean()
        prodmodel = cleaned_data.get('prodmodel')
#        manuname = cleaned_data.get('manuname')
        modtech = cleaned_data.get('modtech')
        manudate = cleaned_data.get('manudate')
        mIsc = cleaned_data.get('mIsc')
        mVoc = cleaned_data.get('mVoc')
        mImp = cleaned_data.get('mImp')
        mVmp = cleaned_data.get('mVmp')
        mFF = cleaned_data.get('mFF')
        mPmp = cleaned_data.get('mPmp')

        if not prodmodel and not modtech and not manudate and not mIsc and not mVoc and not mImp and not mVmp and not mFF and not mPmp:
            raise forms.ValidationError('All Fields are Mandatory!')

# Form to assign product to Testlab
class SelTestLabForm(forms.Form):
    prodmodel = forms.CharField(max_length=50, label='Product Model ')
    testlab = forms.CharField(max_length=50, label='Test Lab ')

    def clean(self):
        cleaned_data = super(SelTestLabForm, self).clean()
        prodmodel = cleaned_data.get('prodmodel')
        testlab = cleaned_data.get('testlab')

        if not prodmodel and not testlab :
            raise forms.ValidationError('All Fields are Mandatory!')

# Form to provide certification access
class CertAccessForm(forms.Form):
 #   manuname = forms.CharField(max_length=50)
    prodmodel = forms.CharField(max_length=50, label='Product Model ')
    allowuseraccess = (('1', 'Enable',), ('0', 'Disable',))
    allowuser = forms.ChoiceField(widget=forms.RadioSelect, choices=allowuseraccess)

    def clean(self):
        cleaned_data = super(CertAccessForm, self).clean()
  #      manuname = cleaned_data.get('manuname') Taken from cookie
        prodmodel = cleaned_data.get('prodmodel')
        allowuser = cleaned_data.get('allowuser')

        if not prodmodel and not allowuser :
            raise forms.ValidationError('All Fields are Mandatory!')

#Form to view Detailed Certification
class ViewDetCertForm(forms.Form):
    prodmdl = forms.CharField(max_length=50, label='Product Model ')

    def clean(self):
        cleaned_data = super(ViewDetCertForm, self).clean()
        prodmdl = cleaned_data.get('prodmdl')

        if not prodmdl:
            raise forms.ValidationError('All Fields are Mandatory!')

#Form to add Samples
class AddSamplesForm(forms.Form):
    projno = forms.CharField(max_length=50, label="Project No",  widget=forms.TextInput(attrs={'placeholder': '1001'}))
    samplescount = forms.CharField(max_length=50, label="No. of Smaples")

    def clean(self):
        cleaned_data = super(AddSamplesForm, self).clean()
        projno = cleaned_data.get('projno')
        samplescount = cleaned_data.get('samplescount')

        if not projno and not samplescount :
            raise forms.ValidationError('All Fields are Mandatory!')

#Form to add Baseline Test Results
class AddTBresultsForm(forms.Form):
    projno = forms.CharField(max_length=50, label='Project No', widget=forms.TextInput(attrs={'placeholder': '1001'}))
    sampleid = forms.CharField(max_length=50, label='Sample ID')
 #   seq = forms.CharField(max_length=50)
 #   testname = forms.CharField(max_length=50)
    testdate = forms.CharField(label='Test Date',
                        widget=forms.TextInput(attrs={'placeholder': '2017-12-04'}))
    tIsc = forms.FloatField(label='Isc', required=True, max_value=100, min_value=0,
                                widget=forms.NumberInput(attrs={'id': 'form_tIsc', 'step': "0.01"}))
    tVoc = forms.FloatField(label='Voc', required=True, max_value=100, min_value=0,
                            widget=forms.NumberInput(attrs={'id': 'form_tVoc', 'step': "0.01"}))
    tImp = forms.FloatField(label='Imp',required=True, max_value=100, min_value=0,
                            widget=forms.NumberInput(attrs={'id': 'form_tImp', 'step': "0.01"}))
    tVmp = forms.FloatField(label='Vmp',required=True, max_value=100, min_value=0,
                            widget=forms.NumberInput(attrs={'id': 'form_tVmp', 'step': "0.01"}))
    tFF = forms.FloatField(label='FF',required=True, max_value=100, min_value=0,
                            widget=forms.NumberInput(attrs={'id': 'form_tFF', 'step': "0.01"}))
    tPmp = forms.FloatField(label='Pmp',required=True, max_value=1000, min_value=0,
                            widget=forms.NumberInput(attrs={'id': 'form_tPmp', 'step': "0.01"}))

    def clean(self):
        cleaned_data = super(AddTBresultsForm, self).clean()
        projno = cleaned_data.get('projno')
        sampleid = cleaned_data.get('sampleid')
     #   seq = cleaned_data.get('seq')
     #   testname = cleaned_data.get('testname')
        testdate = cleaned_data.get('testdate')
        tIsc = cleaned_data.get('tIsc')
        tVoc = cleaned_data.get('tVoc')
        tImp = cleaned_data.get('tImp')
        tVmp = cleaned_data.get('tVmp')
        tFF = cleaned_data.get('tFF')
        tPmp = cleaned_data.get('tPmp')

        if not sampleid and not projno and not testdate and not tIsc and not tVoc and not tImp and not tVmp and not tFF and not tPmp:
            raise forms.ValidationError('All Fields are Mandatory!')


#Form to add Stress Test Results
class AddTresultsForm(forms.Form):
    projno = forms.CharField(max_length=50, label='Project No', widget=forms.TextInput(attrs={'placeholder': '1001'}))
    sampleid = forms.CharField(max_length=50, label= "Sample ID", widget=forms.TextInput(attrs={'placeholder': '1'}))
   # seq = forms.CharField(max_length=50, label='Sequence', widget=forms.TextInput(attrs={'placeholder': 'A'}))
    SEQ_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    ]
    seq = forms.CharField(label='Sequence', widget=forms.Select(choices=SEQ_CHOICES))
    TN_CHOICES = [
        ('TC200', 'TC200'),
        ('UV', 'UV'),
        ('HF', 'HF'),
        ('TC50', 'TC50'),
        ('DH', 'DH'),
    ]
    testname = forms.CharField(label='Test Name', widget=forms.Select(choices=TN_CHOICES))
#    testname = forms.CharField(max_length=50, label="Test Name", widget=forms.TextInput(attrs={'placeholder': 'TC200'}))
    testdate = forms.CharField(label='Test Date',
                        widget=forms.TextInput(attrs={'placeholder': '2017-12-04'}))
    tIsc = forms.FloatField(label='Isc',required=True, max_value=100, min_value=0,
                                widget=forms.NumberInput(attrs={'id': 'form_tIsc', 'step': "0.01"}))
    tVoc = forms.FloatField(label='Voc',required=True, max_value=100, min_value=0,
                            widget=forms.NumberInput(attrs={'id': 'form_tVoc', 'step': "0.01"}))
    tImp = forms.FloatField(label='Imp',required=True, max_value=100, min_value=0,
                            widget=forms.NumberInput(attrs={'id': 'form_tImp', 'step': "0.01"}))
    tVmp = forms.FloatField(label='Vmp',required=True, max_value=100, min_value=0,
                            widget=forms.NumberInput(attrs={'id': 'form_tVmp', 'step': "0.01"}))
    tFF = forms.FloatField(label='FF',required=True, max_value=100, min_value=0,
                            widget=forms.NumberInput(attrs={'id': 'form_tFF', 'step': "0.01"}))
    tPmp = forms.FloatField(label='Pmp',required=True, max_value=1000, min_value=0,
                            widget=forms.NumberInput(attrs={'id': 'form_tPmp', 'step': "0.01"}))

    def clean(self):
        cleaned_data = super(AddTresultsForm, self).clean()
        projno = cleaned_data.get('projno')
        sampleid = cleaned_data.get('sampleid')
        seq = cleaned_data.get('seq')
        testname = cleaned_data.get('testname')
        testdate = cleaned_data.get('testdate')
        tIsc = cleaned_data.get('tIsc')
        tVoc = cleaned_data.get('tVoc')
        tImp = cleaned_data.get('tImp')
        tVmp = cleaned_data.get('tVmp')
        tFF = cleaned_data.get('tFF')
        tPmp = cleaned_data.get('tPmp')

        if not sampleid and not projno and not seq and not testname and not testdate and not tIsc and not tVoc and not tImp and not tVmp and not tFF and not tPmp:
            raise forms.ValidationError('All Fields are Mandatory!')


#Form to take projno and return Tets results
class ViewTresultsForm(forms.Form):
    projno = forms.CharField(max_length=50, label=" Project No", widget=forms.TextInput(attrs={'placeholder': '1001'}))

    def clean(self):
        cleaned_data = super(ViewTresultsForm, self).clean()
        projno = cleaned_data.get('projno')

        if not projno:
            raise forms.ValidationError('All Fields are Mandatory!')



#Form to view Detailed Certification -- Testlab
class ViewTCertForm(forms.Form):
    projno = forms.CharField(max_length=50, label='Project No ', widget=forms.TextInput(attrs={'placeholder': '1001'}))

    def clean(self):
        cleaned_data = super(ViewTCertForm, self).clean()
        projno = cleaned_data.get('projno')

        if not projno:
            raise forms.ValidationError('All Fields are Mandatory!')