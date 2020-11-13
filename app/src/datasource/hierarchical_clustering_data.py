# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = RuleDatafromdict(json.loads(json_string))

from enum import Enum
from dataclasses import dataclass
from typing import Any, List, Optional, Union, TypeVar, Type, cast, Callable


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def is_type(t: Type[T], x: Any) -> T:
    assert isinstance(x, t)
    return x


class AttributeText(Enum):
    ocena5tygodnia = "ocena 5 tygodnia"
    ocena6tygodnia = "ocena 6 tygodnia"
    ocena7tygodnia = "ocena 7 tygodnia"
    ocena8tygodnia = "ocena 8 tygodnia"
    ocenamiesiaca2 = "ocena miesiąca 2"
    ocenamiesiaca3 = "ocena miesiąca 3"
    ocenatygodnia1 = "ocena tygodnia 1"
    ocenatygodnia10 = "ocena tygodnia 10"
    ocenatygodnia11 = "ocena tygodnia 11"
    ocenatygodnia12 = "ocena tygodnia 12"
    ocenatygodnia2 = "ocena tygodnia 2"
    ocenatygodnia3 = "ocena tygodnia 3"
    ocenatygodnia4 = "ocena tygodnia 4"
    ocenaw1miesiacu = "ocena w 1 miesiącu"
    ocenawtygodniu9 = "ocena w tygodniu 9"
    sprzedazw1miesiacu = "sprzedaż w 1 miesiącu"
    sprzedazw1tygodniu = "sprzedaż w 1 tygodniu"
    sprzedazw2tygodniu = "sprzedaż w 2 tygodniu"
    sprzedazw3tygodniu = "sprzedaż w 3 tygodniu"
    sprzedazw4tygodniu = "sprzedaż w 4 tygodniu"
    sprzedazw5tygodniu = "sprzedaż w 5 tygodniu"
    sprzedazw6tygodniu = "sprzedaż w 6 tygodniu"
    sprzedazw7tygodniu = "sprzedaż w 7 tygodniu"
    sprzedazw8tygodniu = "sprzedaż w 8 tygodniu"
    sprzedazwmiesiacu2 = "sprzedaż w miesiącu 2"
    sprzedazwmiesiau3 = "sprzedaż w miesiącu 3"
    sprzedazwtygodniu10 = "sprzedaż w tygodniu 10"
    sprzedazwtygodniu11 = "sprzedaż w tygodniu 11"
    sprzedazwtygodniu12 = "sprzedaż w tygodniu 12"
    sprzedazwtygodniu9 = "sprzedaż w tygodniu 9"
    sredniasprzedazw1tygodniu = "średnia sprzedaż w 1 tygodniu"
    sredniasprzedazw2tygodniu = "średnia sprzedaż w 2 tygodniu"
    sredniasprzedazw3tygodniu = "średnia sprzedaż w 3 tygodniu"
    sredniasprzedazw4tygodniu = "średnia sprzedaż w 4 tygodniu"


@dataclass
class Name:
    text: AttributeText
    attributeID: int

    @staticmethod
    def from_dict(obj: Any) -> 'Name':
        assert isinstance(obj, dict)
        text = AttributeText(obj.get("#text"))
        attributeID = int(from_str(obj.get("@attributeID")))
        return Name(text, attributeID)

    def to_dict(self) -> dict:
        result: dict = {}
        result["#text"] = to_enum(AttributeText, self.text)
        result["@attributeID"] = from_str(str(self.attributeID))
        return result


class TypeEnum(Enum):
    continous = "continous"
    symbolic = "symbolic"


class ValueText(Enum):
    lider = "lider"
    nagana = "nagana"
    nagroda = "nagroda"
    odnowa = "od nowa"
    pochwała = "pochwała"
    programnaprawczy = "program naprawczy"
    rozmowadyscyplinująca = "rozmowa dyscyplinująca"
    zwolnienie = "zwolnienie"


@dataclass
class Value:
    text: ValueText
    valueID: int

    @staticmethod
    def from_dict(obj: Any) -> 'Value':
        assert isinstance(obj, dict)
        text = ValueText(obj.get("#text"))
        valueID = int(from_str(obj.get("@valueID")))
        return Value(text, valueID)

    def to_dict(self) -> dict:
        result: dict = {}
        result["#text"] = to_enum(ValueText, self.text)
        result["@valueID"] = from_str(str(self.valueID))
        return result


@dataclass
class SymbolicValue:
    name: Value

    @staticmethod
    def from_dict(obj: Any) -> 'SymbolicValue':
        assert isinstance(obj, dict)
        name = Value.from_dict(obj.get("name"))
        return SymbolicValue(name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = to_class(Value, self.name)
        return result


@dataclass
class ValuesList:
    symbolicvalue: List[SymbolicValue]

    @staticmethod
    def from_dict(obj: Any) -> 'ValuesList':
        assert isinstance(obj, dict)
        symbolicvalue = from_list(SymbolicValue.from_dict, obj.get("symbolic_value"))
        return ValuesList(symbolicvalue)

    def to_dict(self) -> dict:
        result: dict = {}
        result["symbolic_value"] = from_list(lambda x: to_class(SymbolicValue, x), self.symbolicvalue)
        return result


@dataclass
class Attribute:
    name: Name
    type: TypeEnum
    desc: Optional[str] = None
    valueslist: Optional[ValuesList] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Attribute':
        assert isinstance(obj, dict)
        name = Name.from_dict(obj.get("name"))
        type = TypeEnum(obj.get("type"))
        desc = from_union([from_str, from_none], obj.get("desc"))
        valueslist = from_union([ValuesList.from_dict, from_none], obj.get("values_list"))
        return Attribute(name, type, desc, valueslist)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = to_class(Name, self.name)
        result["type"] = to_enum(TypeEnum, self.type)
        result["desc"] = from_union([from_str, from_none], self.desc)
        result["values_list"] = from_union([lambda x: to_class(ValuesList, x), from_none], self.valueslist)
        return result


@dataclass
class Attributes:
    attribute: List[Attribute]

    @staticmethod
    def from_dict(obj: Any) -> 'Attributes':
        assert isinstance(obj, dict)
        attribute = from_list(Attribute.from_dict, obj.get("attribute"))
        return Attributes(attribute)

    def to_dict(self) -> dict:
        result: dict = {}
        result["attribute"] = from_list(lambda x: to_class(Attribute, x), self.attribute)
        return result


class Operator(Enum):
    empty = "=="


@dataclass
class FactsAttributeValue:
    attribute: Name
    continousValue: int
    operator: Operator
    attributeOrder: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'FactsAttributeValue':
        assert isinstance(obj, dict)
        attribute = Name.from_dict(obj.get("attribute"))
        continousValue = int(from_str(obj.get("continousValue")))
        operator = Operator(obj.get("operator"))
        attributeOrder = from_union([from_none, lambda x: int(from_str(x))], obj.get("attributeOrder"))
        return FactsAttributeValue(attribute, continousValue, operator, attributeOrder)

    def to_dict(self) -> dict:
        result: dict = {}
        result["attribute"] = to_class(Name, self.attribute)
        result["continousValue"] = from_str(str(self.continousValue))
        result["operator"] = to_enum(Operator, self.operator)
        result["attributeOrder"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.attributeOrder)
        return result


@dataclass
class Facts:
    attributevalue: List[FactsAttributeValue]

    @staticmethod
    def from_dict(obj: Any) -> 'Facts':
        assert isinstance(obj, dict)
        attributevalue = from_list(FactsAttributeValue.from_dict, obj.get("attribute_value"))
        return Facts(attributevalue)

    def to_dict(self) -> dict:
        result: dict = {}
        result["attribute_value"] = from_list(lambda x: to_class(FactsAttributeValue, x), self.attributevalue)
        return result


@dataclass
class ConclusionAttributeValue:
    attribute: Name
    attributeOrder: int
    operator: Operator
    continousValue: Optional[int] = None
    value: Optional[Value] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ConclusionAttributeValue':
        assert isinstance(obj, dict)
        attribute = Name.from_dict(obj.get("attribute"))
        attributeOrder = int(from_str(obj.get("attributeOrder")))
        operator = Operator(obj.get("operator"))
        continousValue = from_union([from_none, lambda x: int(from_str(x))], obj.get("continousValue"))
        value = from_union([Value.from_dict, from_none], obj.get("value"))
        return ConclusionAttributeValue(attribute, attributeOrder, operator, continousValue, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["attribute"] = to_class(Name, self.attribute)
        result["attributeOrder"] = from_str(str(self.attributeOrder))
        result["operator"] = to_enum(Operator, self.operator)
        result["continousValue"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.continousValue)
        result["value"] = from_union([lambda x: to_class(Value, x), from_none], self.value)
        return result


@dataclass
class Conclusion:
    attributevalue: ConclusionAttributeValue

    @staticmethod
    def from_dict(obj: Any) -> 'Conclusion':
        assert isinstance(obj, dict)
        attributevalue = ConclusionAttributeValue.from_dict(obj.get("attribute_value"))
        return Conclusion(attributevalue)

    def to_dict(self) -> dict:
        result: dict = {}
        result["attribute_value"] = to_class(ConclusionAttributeValue, self.attributevalue)
        return result


@dataclass
class Conditions:
    attributevalue: Union[List[ConclusionAttributeValue], FactsAttributeValue]

    @staticmethod
    def from_dict(obj: Any) -> 'Conditions':
        assert isinstance(obj, dict)
        attributevalue = from_union([FactsAttributeValue.from_dict, lambda x: from_list(ConclusionAttributeValue.from_dict, x)], obj.get("attribute_value"))
        return Conditions(attributevalue)

    def to_dict(self) -> dict:
        result: dict = {}
        result["attribute_value"] = from_union([lambda x: to_class(FactsAttributeValue, x), lambda x: from_list(lambda x: to_class(ConclusionAttributeValue, x), x)], self.attributevalue)
        return result


@dataclass
class Rule:
    number: int
    ruleID: int
    conclusion: Conclusion
    conditions: Conditions

    @staticmethod
    def from_dict(obj: Any) -> 'Rule':
        assert isinstance(obj, dict)
        number = int(from_str(obj.get("@number")))
        ruleID = int(from_str(obj.get("@ruleID")))
        conclusion = Conclusion.from_dict(obj.get("conclusion"))
        conditions = Conditions.from_dict(obj.get("conditions"))
        return Rule(number, ruleID, conclusion, conditions)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@number"] = from_str(str(self.number))
        result["@ruleID"] = from_str(str(self.ruleID))
        result["conclusion"] = to_class(Conclusion, self.conclusion)
        result["conditions"] = to_class(Conditions, self.conditions)
        return result


@dataclass
class Rules:
    rule: List[Rule]

    @staticmethod
    def from_dict(obj: Any) -> 'Rules':
        assert isinstance(obj, dict)
        rule = from_list(Rule.from_dict, obj.get("rule"))
        return Rules(rule)

    def to_dict(self) -> dict:
        result: dict = {}
        result["rule"] = from_list(lambda x: to_class(Rule, x), self.rule)
        return result


@dataclass
class KnowledgeBase:
    description: str
    kbID: int
    kbName: str
    userID: int
    attributes: Attributes
    facts: Facts
    rules: Rules

    @staticmethod
    def from_dict(obj: Any) -> 'KnowledgeBase':
        assert isinstance(obj, dict)
        description = from_str(obj.get("@description"))
        kbID = int(from_str(obj.get("@kbID")))
        kbName = from_str(obj.get("@kbName"))
        userID = int(from_str(obj.get("@userID")))
        attributes = Attributes.from_dict(obj.get("attributes"))
        facts = Facts.from_dict(obj.get("facts"))
        rules = Rules.from_dict(obj.get("rules"))
        return KnowledgeBase(description, kbID, kbName, userID, attributes, facts, rules)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@description"] = from_str(self.description)
        result["@kbID"] = from_str(str(self.kbID))
        result["@kbName"] = from_str(self.kbName)
        result["@userID"] = from_str(str(self.userID))
        result["attributes"] = to_class(Attributes, self.attributes)
        result["facts"] = to_class(Facts, self.facts)
        result["rules"] = to_class(Rules, self.rules)
        return result


@dataclass
class RuleData:
    knowledgebase: KnowledgeBase

    @staticmethod
    def from_dict(obj: Any) -> 'RuleData':
        assert isinstance(obj, dict)
        knowledgebase = KnowledgeBase.from_dict(obj.get("knowledge_base"))
        return RuleData(knowledgebase)

    def to_dict(self) -> dict:
        result: dict = {}
        result["knowledge_base"] = to_class(KnowledgeBase, self.knowledgebase)
        return result


def RuleDatafromdict(s: Any) -> RuleData:
    return RuleData.from_dict(s)


def RuleDatatodict(x: RuleData) -> Any:
    return to_class(RuleData, x)
