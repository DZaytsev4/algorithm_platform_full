from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils import timezone

from algorithms.models import Algorithm

User = get_user_model()

ADMIN_USERNAME = 'admin'
MODERATOR_USERNAME = 'moderator'
USER1_USERNAME = 'user1'
USER2_USERNAME = 'user2'

ADMIN_PASSWORD = 'adminpass123'
MODERATOR_PASSWORD = 'modpass123'
USER1_PASSWORD = 'user1pass123'
USER2_PASSWORD = 'user2pass123'

MODERATOR_GROUP_NAME = 'Модераторы'

ALGORITHM_DATA = [
    {
        'name': 'Binary Search',
        'description': 'Реализация двоичного поиска на Python.',
        'code': 'def binary_search(arr, target):\n    left, right = 0, len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            return mid\n        if arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1\n',
        'author_name': USER1_USERNAME,
        'status': Algorithm.STATUS_APPROVED,
        'is_paid': False,
        'price': 0,
        'language': 'Python',
        'compiler': 'python',
        'moderated_by': MODERATOR_USERNAME,
        'moderated_at': True,
        'tegs': 'python,search,algorithms',
    },
    {
        'name': 'Prime Check',
        'description': 'Проверка на простое число на C++.',
        'code': '#include <cmath>\n#include <iostream>\nusing namespace std;\nbool is_prime(int n) {\n    if (n < 2) return false;\n    for (int i = 2; i <= sqrt(n); i++) {\n        if (n % i == 0) return false;\n    }\n    return true;\n}\nint main() {\n    int n; cin >> n;\n    cout << (is_prime(n) ? "YES" : "NO") << endl;\n    return 0;\n}\n',
        'author_name': USER2_USERNAME,
        'status': Algorithm.STATUS_APPROVED,
        'is_paid': False,
        'price': 0,
        'language': 'C++',
        'compiler': 'g++',
        'moderated_by': MODERATOR_USERNAME,
        'moderated_at': True,
        'tegs': 'cpp,prime,math',
    },
    {
        'name': 'String Reverse',
        'description': 'Реверс строки в Java.',
        'code': 'public class Main {\n    public static String reverse(String s) {\n        return new StringBuilder(s).reverse().toString();\n    }\n    public static void main(String[] args) {\n        System.out.println(reverse("hello"));\n    }\n}\n',
        'author_name': USER1_USERNAME,
        'status': Algorithm.STATUS_PENDING,
        'is_paid': False,
        'price': 0,
        'language': 'Java',
        'compiler': 'javac',
        'moderated_by': None,
        'moderated_at': None,
        'tegs': 'java,string,utility',
    },
    {
        'name': 'Paid Sorting',
        'description': 'Платный алгоритм сортировки на C++.',
        'code': '#include <algorithm>\n#include <iostream>\n#include <vector>\nusing namespace std;\nint main() {\n    vector<int> data = {3, 1, 4, 1, 5, 9};\n    sort(data.begin(), data.end());\n    for (int value : data) cout << value << " ";\n    return 0;\n}\n',
        'author_name': USER2_USERNAME,
        'status': Algorithm.STATUS_APPROVED,
        'is_paid': True,
        'price': 150,
        'language': 'C++',
        'compiler': 'g++',
        'moderated_by': MODERATOR_USERNAME,
        'moderated_at': True,
        'tegs': 'cpp,sorting,paid',
    },
    {
        'name': 'Paid Graph Algorithm',
        'description': 'Платный графовый алгоритм на Python.',
        'code': 'def dfs(graph, start, visited=None):\n    if visited is None:\n        visited = set()\n    visited.add(start)\n    for neighbor in graph.get(start, []):\n        if neighbor not in visited:\n            dfs(graph, neighbor, visited)\n    return visited\n\nif __name__ == "__main__":\n    graph = {"A": ["B", "C"], "B": ["A"], "C": ["A"]}\n    print(dfs(graph, "A"))\n',
        'author_name': USER1_USERNAME,
        'status': Algorithm.STATUS_APPROVED,
        'is_paid': True,
        'price': 250,
        'language': 'Python',
        'compiler': 'python',
        'moderated_by': MODERATOR_USERNAME,
        'moderated_at': True,
        'tegs': 'python,graph,paid',
    },
]


class Command(BaseCommand):
    help = 'Seed initial users and algorithms into the database.'

    def handle(self, *args, **options):
        self.stdout.write('Start seeding initial data...')

        moderator_group, _ = Group.objects.get_or_create(name=MODERATOR_GROUP_NAME)

        admin, created = User.objects.get_or_create(
            username=ADMIN_USERNAME,
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        admin.set_password(ADMIN_PASSWORD)
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()
        self.stdout.write(f'  Admin user: {admin.username} (password: {ADMIN_PASSWORD})')

        moderator, _ = User.objects.get_or_create(
            username=MODERATOR_USERNAME,
            defaults={
                'email': 'moderator@example.com',
                'is_staff': False,
                'is_superuser': False,
            }
        )
        moderator.set_password(MODERATOR_PASSWORD)
        moderator.save()
        moderator.groups.add(moderator_group)
        self.stdout.write(f'  Moderator user: {moderator.username} (password: {MODERATOR_PASSWORD})')

        user1, _ = User.objects.get_or_create(
            username=USER1_USERNAME,
            defaults={
                'email': 'user1@example.com',
                'is_staff': False,
                'is_superuser': False,
            }
        )
        user1.set_password(USER1_PASSWORD)
        user1.save()
        self.stdout.write(f'  Regular user 1: {user1.username} (password: {USER1_PASSWORD})')

        user2, _ = User.objects.get_or_create(
            username=USER2_USERNAME,
            defaults={
                'email': 'user2@example.com',
                'is_staff': False,
                'is_superuser': False,
            }
        )
        user2.set_password(USER2_PASSWORD)
        user2.save()
        self.stdout.write(f'  Regular user 2: {user2.username} (password: {USER2_PASSWORD})')

        users = {
            ADMIN_USERNAME: admin,
            MODERATOR_USERNAME: moderator,
            USER1_USERNAME: user1,
            USER2_USERNAME: user2,
        }

        for algo_data in ALGORITHM_DATA:
            moderated_by_user = None
            if algo_data['moderated_by']:
                moderated_by_user = users.get(algo_data['moderated_by'])

            algorithm, created = Algorithm.objects.update_or_create(
                name=algo_data['name'],
                defaults={
                    'description': algo_data['description'],
                    'code': algo_data['code'],
                    'author_name': algo_data['author_name'],
                    'status': algo_data['status'],
                    'tegs': algo_data['tegs'],
                    'is_paid': algo_data['is_paid'],
                    'price': algo_data['price'],
                    'language': algo_data['language'],
                    'compiler': algo_data['compiler'],
                    'moderated_by': moderated_by_user,
                    'moderated_at': timezone.now() if algo_data['moderated_at'] else None,
                }
            )
            created_text = 'created' if created else 'updated'
            self.stdout.write(f'  Algorithm {created_text}: {algorithm.name}')

        self.stdout.write(self.style.SUCCESS('Initial data seeding completed.'))
