from django import forms


class BootstrapFormMixin:
    """Adds Bootstrap classes to every field's widget automatically."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                existing = widget.attrs.get('class', '')
                widget.attrs['class'] = (existing + ' form-check-input').strip()
            elif isinstance(widget, forms.Select):
                existing = widget.attrs.get('class', '')
                widget.attrs['class'] = (existing + ' form-select').strip()
            else:
                existing = widget.attrs.get('class', '')
                widget.attrs['class'] = (existing + ' form-control').strip()
