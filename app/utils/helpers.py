from flask import flash

def flash_custom_errors(form):
    """Exibe erros de formulário com ícones e formatação consistente."""
    for field, errors in form.errors.items():
        for error in errors:
            flash(
                f'<ion-icon name="alert-circle-outline"></ion-icon> '
                f'<strong>{getattr(form, field).label.text}:</strong> {error}',
                'error'
            )