from __future__ import annotations

from typing import Iterable

from django.contrib.auth.models import AnonymousUser


MODERATOR_GROUP_NAMES: tuple[str, ...] = (
    "Модераторы",
    "Moderators",
    "moderators",
    "moderator",
)


def get_user_group_names(user) -> list[str]:
    """
    Возвращает список имён групп пользователя (как строки).

    Нужен для сериализации и для определения ролей без привязки к конкретному UI.
    """
    if not user or isinstance(user, AnonymousUser) or not getattr(user, "is_authenticated", False):
        return []
    try:
        return list(user.groups.values_list("name", flat=True))
    except Exception:
        # На случай кастомного User/мока без related manager.
        return []


def is_moderator(user) -> bool:
    """
    Модератор: staff/superuser ИЛИ в одной из групп MODERATOR_GROUP_NAMES.
    """
    if not user or isinstance(user, AnonymousUser) or not getattr(user, "is_authenticated", False):
        return False
    if getattr(user, "is_superuser", False) or getattr(user, "is_staff", False):
        return True

    group_names: Iterable[str] = get_user_group_names(user)
    return any(name in MODERATOR_GROUP_NAMES for name in group_names)


def get_role(user) -> str:
    """
    Возвращает роль для фронтенда.

    Контракт:
    - admin: superuser
    - moderator: staff или группа модераторов
    - consumer: все остальные
    """
    if not user or isinstance(user, AnonymousUser) or not getattr(user, "is_authenticated", False):
        return "consumer"
    if getattr(user, "is_superuser", False):
        return "admin"
    if is_moderator(user):
        return "moderator"
    return "consumer"

