import types
from collections import namedtuple


def _create_value_cls(name):
    cls = namedtuple("_EnumValue_" + name, "name value")
    cls.__repr__ = lambda self: "<%s.%s: %r>" % (name, self.name, self.value)
    cls.__str__ = lambda self: "%s.%s" % (name, self.name)
    return cls


def _is_descriptor(obj):
    return (
        hasattr(obj, "__get__") or hasattr(obj, "__set__") or hasattr(obj, "__delete__")
    )


class EnumMeta(type):
    def __new__(cls, name, bases, attrs):
        value_mapping = {}
        member_mapping = {}
        member_names = []

        value_cls = _create_value_cls(name)
        for key, value in list(attrs.items()):
            is_descriptor = _is_descriptor(value)
            if key[0] == "_" and not is_descriptor:
                continue

            # Special case classmethod to just pass through
            if isinstance(value, classmethod):
                continue

            if is_descriptor:
                setattr(value_cls, key, value)
                del attrs[key]
                continue

            try:
                new_value = value_mapping[value]
            except KeyError:
                new_value = value_cls(name=key, value=value)
                value_mapping[value] = new_value
                member_names.append(key)

            member_mapping[key] = new_value
            attrs[key] = new_value

        attrs["_enum_value_map_"] = value_mapping
        attrs["_enum_member_map_"] = member_mapping
        attrs["_enum_member_names_"] = member_names
        actual_cls = super().__new__(cls, name, bases, attrs)
        value_cls._actual_enum_cls_ = actual_cls
        return actual_cls

    def __iter__(cls):
        return (cls._enum_member_map_[name] for name in cls._enum_member_names_)

    def __reversed__(cls):
        return (
            cls._enum_member_map_[name] for name in reversed(cls._enum_member_names_)
        )

    def __len__(cls):
        return len(cls._enum_member_names_)

    def __repr__(cls):
        return "<enum %r>" % cls.__name__

    @property
    def __members__(cls):
        return types.MappingProxyType(cls._enum_member_map_)

    def __call__(cls, value):
        try:
            return cls._enum_value_map_[value]
        except (KeyError, TypeError):
            raise ValueError("%r is not a valid %s" % (value, cls.__name__))

    def __getitem__(cls, key):
        return cls._enum_member_map_[key]

    def __setattr__(cls, name, value):
        raise TypeError("Enums are immutable.")

    def __delattr__(cls, attr):
        raise TypeError("Enums are immutable")

    def __instancecheck__(self, instance):
        # isinstance(x, Y)
        # -> __instancecheck__(Y, x)
        try:
            return instance._actual_enum_cls_ is self
        except AttributeError:
            return False


class Enum(metaclass=EnumMeta):
    @classmethod
    def try_value(cls, value):
        try:
            return cls._enum_value_map_[value]
        except (KeyError, TypeError):
            return value


class CreationSource(Enum):
    OTHER = "OTHER"
    APPOINTMENTS = "APPOINTMENTS"
    COUPON = "COUPON"
    DELETION_RECOVERY = "DELETION_RECOVERY"
    DIRECTORY = "DIRECTORY"
    EGIFTING = "EGIFTING"
    EMAIL_COLLECTION = "EMAIL_COLLECTION"
    FEEDBACK = "FEEDBACK"
    IMPORT = "IMPORT"
    INVOICES = "INVOICES"
    LOYALTY = "LOYALTY"
    MARKETING = "MARKETING"
    MERGE = "MERGE"
    ONLINE_STORE = "ONLINE_STORE"
    INSTANT_PROFILE = "INSTANT_PROFILE"
    TERMINAL = "TERMINAL"
    THIRD_PARTY = "THIRD_PARTY"
    THIRD_PARTY_IMPORT = "THIRD_PARTY_IMPORT"
    UNMERGE_RECOVERY = "UNMERGE_RECOVERY"

    def __str__(self):
        return self.value


class CardBrand(Enum):
    OTHER_BRAND = "OTHER_BRAND"
    VISA = "VISA"
    MASTERCARD = "MASTERCARD"
    AMERICAN_EXPRESS = "AMERICAN_EXPRESS"
    DISCOVER = "DISCOVER"
    DISCOVER_DINERS = "DISCOVER_DINERS"
    JCB = "JCB"
    CHINA_UNIONPAY = "CHINA_UNIONPAY"
    SQUARE_GIFT_CARD = "SQUARE_GIFT_CARD"
    SQUARE_CAPITAL_CARD = "SQUARE_CAPITAL_CARD"
    INTERAC = "INTERAC"
    EFTPOS = "EFTPOS"
    FELICA = "FELICA"

    def __str__(self):
        return self.value


class CardPrepaidType(Enum):
    UNKNOWN_PREPAID_TYPE = "UNKNOWN_PREPAID_TYPE"
    NOT_PREPAID = "NOT_PREPAID"
    PREPAID = "PREPAID"

    def __str__(self):
        return self.value


class CustomerSort(Enum):
    DEFAULT = "DEFAULT"
    CREATED_AT = "CREATED_AT"


def try_enum(cls, val):
    """A function that tries to turn the value into enum ``cls``.
    If it fails it returns the value instead.
    """

    try:
        return cls._enum_value_map_[val]
    except (KeyError, TypeError, AttributeError):
        return val
