from django import template
import num2words

register = template.Library()


"""
Convert numbers to words.

Template usage example:
{{ 1234|float_to_words }}

"""


@register.filter(name="float_to_words")
def float_to_words(value: float) -> str:
    try:
        init = num2words
        return init.num2words(
            value,
            lang='pt_BR',
            ordinal=False
        ).capitalize()

    except ValueError:
        return f"{value} não é um número."
