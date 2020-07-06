from django.db.models import CharField

# simplify charfield because i always have to think what to put for these parameters
# whereas it's almost always the same/similar to below
DEFAULT_MODELS_CHAR_FIELD = CharField(
    max_length=300, blank=False, default="", null=False
)
