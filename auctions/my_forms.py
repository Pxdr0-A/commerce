from django import forms


class AddBid(forms.Form):
    bid = forms.IntegerField(min_value=0)


class AddCommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={"rows": 2, "cols": 20, "required": True}), label="")


class AddListing(forms.Form):
    listing = forms.CharField(max_length=64)
    description = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 2, "cols": 20, "required": True}),
        label="description"
    )
    url = forms.URLField()
    active = forms.BooleanField(initial=True)


class AddAuction(forms.Form):
    # type is implicit
    name = forms.CharField(max_length=64)
    active = forms.BooleanField(initial=True)


class AddType(forms.Form):
    name = forms.CharField(max_length=64)
    description = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 2, "cols": 20, "required": True}),
        label="description"
    )
