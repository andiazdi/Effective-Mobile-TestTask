# Effective-Mobile Test Task

## Описание проекта

Это API для управления пользователями и ролями с системой прав доступа.  
Проект написан на **FastAPI**, **SQLAlchemy** (PostgreSQL) и **Pydantic**.

---

## Запуск проекта
1. Пропишите переменные окружения в `.env` файле:
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Примените миграции:
   ```bash
   alembic upgrade head
   ```
4. Запустите:
   ```bash
   uvicorn src.main:app --reload
   ```
   
## Структура проекта

- `src/routes/user/` - работа с пользователями.  
- `src/routes/role/` - работа с ролями и правами доступа.  
- `src/dependencies/database.py` - настройка базы данных и сессий SQLAlchemy.  
- `src/routes/auth/` - регистрация и аутентификация пользователей.

---

## Схема управления доступом

**Роли пользователей**  
   Каждый пользователь имеет одну роль (`User.role_id`).

   Для каждой роли хранятся права в таблице `RoleAccess`.  
   Пример структуры прав для роли `admin`:

   | Право                   | Значение |
   |-------------------------|----------|
   | add_user_permission     | True     |
   | read_users_permission   | True     |
   | update_users_permission | True     |
   | delete_users_permission | True     |
   | read_roles_permission   | True     |
   | update_roles_permission | True     |

   Для роли `user` все права по умолчанию `False`.

**Проверка прав**  
   - Из базы данных подгружается роль пользователя и его права.  
   - Доступ к ресурсу разрешается, если право установлено в `True`.  
