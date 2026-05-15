"""Genera las etiquetas de componentes para el dibujo del esquemático.

Fork extractivo: la versión upstream usaba `lcapy.expr.Expr` para envolver
expresiones sympy y formatearlas. Aquí trabajamos con sympy directamente,
evitando arrastrar el motor simbólico de lcapy.
"""

import sympy as sym

from .latex import latex_format_label
from .valueformatter import value_formatter
from .valueparser import value_parser


def _sympify_safe(value):
    """Sympifica `value` tolerando entradas que sympy no entiende."""
    try:
        return sym.sympify(value)
    except (sym.SympifyError, SyntaxError, TypeError, AttributeError):
        return None


def _latex_math(value):
    """Devuelve `value` como string LaTeX matemático encerrado en `$`."""
    sexpr = _sympify_safe(value)
    if sexpr is None:
        return '$' + str(value) + '$'
    return '$' + sym.latex(sexpr) + '$'


class LabelMaker:

    def _format_expr(self, expr):
        return _latex_math(expr)

    def _format_value_units(self, value, units, style):
        sexpr = _sympify_safe(value)
        if sexpr is None or not sexpr.is_constant():
            return _latex_math(value)
        return value_formatter(style=style).latex_math(sexpr, units)

    def _format_name(self, cpt_type, cpt_id):

        name = cpt_type
        subscript = cpt_id[1:] if cpt_id.startswith('_') else cpt_id

        if cpt_type == 'REL':
            name = r'\mathcal{R}'
        elif len(name) > 1:
            name = r'\mathrm{%s}' % name

        if subscript != '':
            if len(subscript) > 1:
                subscript = r'\mathrm{%s}' % subscript
            name = name + '_{%s}' % subscript
        return latex_format_label('$' + name + '$')

    def make(self, cpt, label_ports=False, style='eng'):

        # There are two possible labels for a component:
        # 1. Component name, e.g., R1
        # 2. Component value, expression, or symbol

        id_label = self._format_name(cpt.type, cpt.id)
        value_label = None

        if cpt.type == 'P' and not label_ports:
            id_label = None

        elif cpt.type in ('A', 'O', 'W') or id_label.find('#') != -1:
            id_label = None

        if cpt.type in ('A', 'S', 'SW', 'U'):
            value_label = ''

        unify = False
        if len(cpt.args):

            # TODO, extend for mechanical and acoustical components.
            units_map = {'V': 'V', 'I': 'A', 'R': '$\Omega$',
                         'C': 'F', 'L': 'H'}

            expr = value_parser(cpt.args[0])

            if cpt.classname in ('Vstep', 'Istep'):
                expr = '(%s) * Heaviside(t)' % expr
                value_label = self._format_expr(expr)
            elif cpt.classname in ('Vs', 'Is'):
                value_label = self._format_expr(expr)
            elif cpt.classname in ('TF', 'TFscs', 'TFscss', 'TFsscss', 'TFtap'):
                value_label = None
            elif cpt.type in ('F', 'H') and len(cpt.args) > 1:
                # This is hard to give a reasonable label since the
                # control current is specified by a voltage source.
                # The user will have to override manually.
                expr = cpt.args[1]
                value_label = self._format_expr(expr)
            elif cpt.name == 'I':
                # Hack for current source called I
                value_label = self._format_expr(expr)
            elif cpt.classname not in ('TP',):

                if cpt.type in units_map:
                    units = units_map[cpt.type]
                else:
                    units = ''

                value_label = self._format_value_units(expr, units, style)

            # Ensure labels are the same when the value is not specified.
            # This will prevent printing the name and value.
            unify = expr == cpt.type + cpt.id

            # Currently, we only annnotate the component with the
            # value, expression, or symbol.  If this is not specified,
            # it defaults to the component identifier.  Note, there
            # are some objects we do not want to label, such as wires
            # and ports.
        id_label = '' if id_label is None else latex_format_label(id_label)
        value_label = id_label if value_label is None \
            else latex_format_label(value_label)

        if unify:
            value_label = id_label

        return id_label, value_label
