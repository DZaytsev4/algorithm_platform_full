import { User } from '../types';

export const hasModerationAccess = (user: User | null): boolean => {
  if (!user) return false;

  // Основной источник истины — поле role, которое отдаёт бэкенд.
  if (user.role === 'moderator' || user.role === 'admin') return true;

  // Фоллбеки на случай старого бэкенда / другого формата ответа.
  const userAny = user as any;
  if (userAny.is_staff || userAny.is_superuser) return true;

  const groups: unknown = userAny.groups;
  if (Array.isArray(groups)) {
    const groupNames = groups
      .map((g: any) => (typeof g === 'string' ? g : g?.name))
      .filter(Boolean)
      .map((s: string) => s.toLowerCase());

    const moderatorGroups = new Set([
      'moderator',
      'moderators',
      'модератор',
      'модераторы',
      'admin',
      'administrators',
      'администратор',
      'администраторы',
    ]);

    return groupNames.some((name: string) => moderatorGroups.has(name));
  }

  return false;
};

export const getUserRoleDisplay = (user: User): string => {
  const userAny = user as any;
  
  if (user.role) return user.role;
  if (userAny.is_superuser) return 'admin';
  if (userAny.is_staff) return 'staff';
  if (userAny.groups && userAny.groups.length > 0) {
    return userAny.groups.map((g: any) => typeof g === 'string' ? g : g.name).join(', ');
  }
  
  return 'consumer';
};