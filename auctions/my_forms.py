from django import forms


class AddBid(forms.Form):
    bid = forms.IntegerField(min_value=0)


class AddCommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={"rows": 4, "cols": 50, "required": True}), label="")


class AddListing(forms.Form):
    listing = forms.CharField(max_length=64)
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": 6, "cols": 60, "required": True}), label="")
    active = forms.BooleanField()


class AddAuction(forms.Form):
    # type is implicit
    name = forms.CharField()
    active = forms.BooleanField(initial=True)
