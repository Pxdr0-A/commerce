from django import forms

class AddBid(forms.Form):
    bid = forms.IntegerField(min_value=0)

class AddCommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={"rows": 4, "cols": 50, "required": True}), label="")