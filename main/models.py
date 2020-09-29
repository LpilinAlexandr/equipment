from django.db import models


class Type(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    code = models.TextField(verbose_name='Код')
    mask = models.CharField(max_length=100, verbose_name='Маска')

    def __str__(self):
        return f'{self.name}'


class Equip(models.Model):
    code = models.TextField(verbose_name='Код')
    type_code = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name='Код типа')
    serial_number = models.CharField(max_length=100, unique=True, verbose_name='Серийный номер')

    def __str__(self):
        return f'{self.type_code} -- {self.serial_number}'