from django import forms


class TallerBaseForm(forms.ModelForm):
    """
    Formulario base para los modelos del taller.
    Aquí se centralizarán estilos y validaciones compartidas.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            current_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (
                f"{current_class} form-control".strip()
            )
