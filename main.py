"""Рубежный контроль № 1. Вариант запросов В, предметная область № 20."""

import sys
from dataclasses import dataclass
from operator import itemgetter

sys.stdout.reconfigure(encoding="utf-8")


@dataclass(frozen=True)
class Detail:
    """Деталь с основной связью один-ко-многим с поставщиком."""

    id: int
    name: str
    price: int
    supplier_id: int


@dataclass(frozen=True)
class Supplier:
    """Поставщик деталей."""

    id: int
    name: str


@dataclass(frozen=True)
class DetailSupplier:
    """Связующая запись для отношения многие-ко-многим."""

    detail_id: int
    supplier_id: int


suppliers = [
    Supplier(1, "Альфа-Снаб"),
    Supplier(2, "Бета-Пром"),
    Supplier(3, "Гамма-Деталь"),
    Supplier(4, "Дельта-Металл"),
]

details = [
    Detail(1, "Анкер", 120, 1),
    Detail(2, "Втулка", 75, 2),
    Detail(3, "Адаптер", 180, 1),
    Detail(4, "Шестерня", 250, 3),
    Detail(5, "Арматура", 60, 4),
]

details_suppliers = [
    DetailSupplier(1, 1),
    DetailSupplier(1, 2),
    DetailSupplier(2, 2),
    DetailSupplier(2, 3),
    DetailSupplier(3, 1),
    DetailSupplier(3, 3),
    DetailSupplier(4, 3),
    DetailSupplier(4, 4),
    DetailSupplier(5, 1),
    DetailSupplier(5, 4),
]


def main():
    """Формирует и выводит результаты трех запросов варианта В."""

    # Объединение по связи один-ко-многим: поставщик -> его детали.
    one_to_many = [
        (detail.name, detail.price, supplier.name)
        for supplier in suppliers
        for detail in details
        if detail.supplier_id == supplier.id
    ]

    print("Задание В1. Детали на букву А и их поставщики")
    result_1 = sorted(
        [row for row in one_to_many if row[0].casefold().startswith("а")],
        key=itemgetter(0),
    )
    for detail_name, price, supplier_name in result_1:
        print(f"  {detail_name} - {supplier_name} ({price} руб.)")

    print("\nЗадание В2. Минимальная цена деталей у каждого поставщика")
    minimum_prices = []
    for supplier in suppliers:
        prices = [
            price
            for _, price, supplier_name in one_to_many
            if supplier_name == supplier.name
        ]
        if prices:
            minimum_prices.append((supplier.name, min(prices)))
    result_2 = sorted(minimum_prices, key=itemgetter(1))
    for supplier_name, minimum_price in result_2:
        print(f"  {supplier_name} - {minimum_price} руб.")

    # Объединение по связи многие-ко-многим через класс DetailSupplier.
    many_to_many = [
        (supplier.name, detail.name, detail.price)
        for supplier in suppliers
        for detail in details
        for relation in details_suppliers
        if relation.supplier_id == supplier.id
        and relation.detail_id == detail.id
    ]
    result_3 = sorted(many_to_many, key=itemgetter(0))

    print("\nЗадание В3. Связанные детали и поставщики")
    for supplier_name, detail_name, price in result_3:
        print(f"  {supplier_name} - {detail_name} ({price} руб.)")


if __name__ == "__main__":
    main()
