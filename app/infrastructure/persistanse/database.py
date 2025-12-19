import psycopg2
from LuminUserService.app.infrastructure.dependency_container import DependencyContainer


def connection_factory():
    def create_connection():
        return psycopg2.connect(
            host="localhost",
            database="LuminUserDatabase",
            user="postgres",
            password="(123)%111"
        )
    return create_connection


def get_dependency_container():
    return DependencyContainer(connection_factory())