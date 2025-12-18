class DomainException(Exception):
    pass


class UserIsAlreadyExistException(DomainException):
    pass


class UserIsNotExistException(DomainException):
    pass


class UsernameValidationException(DomainException):
    pass


class BioValidationException(DomainException):
    pass


class PhoneValidationException(DomainException):
    pass


class EmailValidationException(DomainException):
    pass


class DateOfBornValidationException(DomainException):
    pass


class AvatarURLValidationException(DomainException):
    ...
