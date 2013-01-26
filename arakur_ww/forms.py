#! -*- coding: utf8 -*-
from flask.ext.wtf import Form, TextField, PasswordField, validators, \
        HiddenField, IntegerField, DecimalField


class LoginForm(Form):
    username = TextField('Usuario', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        if self.username.data != 'admin':
            self.username.errors.append('Nombre de usuario invalido')
            return False

        if self.password.data != 'xx':
            self.password.errors.append('Password Incorrecto')
            return False

        return True


class ProgramForm(Form):
    carga_aireada = IntegerField(u'Carga Aireada', [
        validators.Required("Campo obligatorio"),
        validators.NumberRange(1, 9999, "El valor debe estar entre %(min)s y %(max)s"),
        ])
    aireacion = IntegerField(u'Aireación', [
        validators.Required("Campo obligatorio"),
        validators.NumberRange(1, 9999, "El valor debe estar entre %(min)s y %(max)s"),
        ])
    sedimentacion = IntegerField(u'Sedimentación', [
        validators.Required("Campo obligatorio"),
        validators.NumberRange(1, 9999, "El valor debe estar entre %(min)s y %(max)s"),
        ])
    descarga = IntegerField(u'Descarga', [
        validators.Required("Campo obligatorio"),
        validators.NumberRange(1, 9999, "El valor debe estar entre %(min)s y %(max)s"),
        ])


class ParametersForm(Form):
    oxigen_min = DecimalField(u'Oxígeno Mínimo', [
        validators.Required("Campo obligatorio"),
        validators.NumberRange(1, 99.99, "El valor debe estar entre %(min)s y %(max)s"),

        ])
    oxigen_max = DecimalField(u'Oxígeno Máximo', [
        validators.Required("Campo obligatorio"),
        validators.NumberRange(0, 99.99, "El valor debe estar entre %(min)s y %(max)s"),

        ])
    cloudiness_max = IntegerField(u'Turbiedad Máxima', [
        validators.Required("Campo obligatorio"),
        validators.NumberRange(1, 9999, "El valor debe estar entre %(min)s y %(max)s"),

        ])

