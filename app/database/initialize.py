from sqlalchemy.orm import Session


def init_db(db: Session) -> None:
    # * Not needed if creating tables with alembic

    # superuser = Employee.crud.user.read_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
    # if not superuser:
    #     user_in = EmployeeCreateIn(
    #         email=settings.FIRST_SUPERUSER_EMAIL,
    #         full_name=settings.FIRST_SUPERUSER_FULL_NAME,
    #         password=settings.FIRST_SUPERUSER_PASSWORD,
    #         is_superuser=True,
    #         role=Role.board.value,
    #     )
    #     superuser = employee.crud.user.create(db, obj_in=user_in)  # noqa: F841
    ...
