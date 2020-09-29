from django.shortcuts import render
from django.http import HttpResponse
import logging
import re
from .models import Type, Equip


def add_to_base(new_equip_list, base):
    """
    Добавляем серийные номера в базу.
    Если список совпадений пуст, то, получается, ничего не происходит.
    """
    # Устанавливаем уровень логирования
    logging.basicConfig(level=logging.INFO)

    # Для каждого из совпадений
    for equip in new_equip_list:
        # Добавляем в базу
        add_to = Equip.objects.get_or_create(type_code=base, serial_number=equip)
        try:
            # Если такой в базе уже есть
            if add_to[1] is False:
                raise AlreadyExists()
            # Если есть - выводим сообщение на консоль
        except AlreadyExists as exc:
            logging.info(f'{exc}')


def check_equip(type, equip_list):
    """
    Проверяем загруженные данные
    """

    # тестовая строка: '0JJDD3_3gf\321SS3-3qq\n133FFX_111\n3F1KK3@K12\9DIOPFD0DF\nDDOIUYT0KK\n'
    masks = {
        'XXAAAAAXAA': re.compile(r"([\dA-Z]{2}[A-Z]{5}[\dA-Z][A-Z]{2})"),
        'NXXAAXZXaa': re.compile(r"([\d][\dA-Z]{2}[A-Z]{2}[\dA-Z][-_@][\dA-Z][a-z]{2})"),
        'NXXAAXZXXX': re.compile(r"([\d][\dA-Z]{2}[A-Z]{2}[\dA-Z][-_@][\dA-Z]{3})")
    }

    # Получаем тип оборудования, по выбранному в форме
    base = Type.objects.get(name=type)
    # Получаем маску этого типа
    mask = masks[base.mask]
    # Проверяем на совпадения
    new_equip = re.findall(mask, equip_list)
    # Загружаем совпадения в базу
    add_to_base(new_equip_list=new_equip, base=base)

    # Если совпадений не было, возвращаем NO, если были, возвращаем какие были
    if not new_equip:
        return 'NO'
    else:
        return new_equip


def missing_TypeEquip(request):
    """
    Проверка заголовка typeEquip
    """
    # Если значение у заголовка пустое - вызываем исключение
    try:
        if request.GET['typeEquip'] == '':
            raise MissingTypeEquip()
        else:
            return False
    except MissingTypeEquip:
        return True


class AlreadyExists(Exception):
    """
    Исключение, если такой номер уже есть
    """
    def __str__(self):
        return 'Такой серийный номер уже есть в базе'


class MissingTypeEquip(Exception):
    """
    Исключение не выбранного типа оборудования
    """
    pass


def main(request):
    """
    Основная страница. Показываем все типы оборудования для выбора
    """

    types = Type.objects.all()

    context = {
        'types': types
    }

    return render(request, 'main/index.html', context)


def ajax_form(request):
    """
    Обрабатываем загруженные данные через ajax
    """
    # Если приходит запрос
    if request.GET and 'typeEquip' in request.GET:

        # Если пустая typeEquip, вызываем алерт, чтобы выбрали тип
        if missing_TypeEquip(request=request):
            return HttpResponse(f"missingTypeEquip")
        # Проверяем на наличие валидных номеров
        data = check_equip(type=request.GET['typeEquip'], equip_list=request.GET['textContent'])
        # Если их нет - возвращаем алерт, что ничего не загружено
        if data == 'NO':
            return HttpResponse('NO')
        # Если есть - возвращаем алерт, что успешно загружены такие-то номера
        elif data:
            return HttpResponse('\n'.join(data))
    else:
        return


