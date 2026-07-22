from datetime import date, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator


def to_camel(value: str) -> str:
    head, *tail = value.split("_")
    return head + "".join(part.capitalize() for part in tail)


class APIModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, from_attributes=True)


class Gender(StrEnum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class MeasurementType(StrEnum):
    OFFICIAL = "OFFICIAL"
    SELF = "SELF"


class ItemKey(StrEnum):
    CARDIO = "CARDIO"
    GRIP = "GRIP"
    MUSCULAR_END = "MUSCULAR_END"
    FLEXIBILITY = "FLEXIBILITY"
    AGILITY = "AGILITY"
    POWER = "POWER"
    COORDINATION = "COORDINATION"
    BMI = "BMI"


class FitnessElement(StrEnum):
    CARDIO = "CARDIO"
    GRIP = "GRIP"
    MUSCULAR_END = "MUSCULAR_END"
    FLEXIBILITY = "FLEXIBILITY"
    AGILITY = "AGILITY"
    POWER = "POWER"
    COORDINATION = "COORDINATION"


class Grade(StrEnum):
    SEED = "SEED"
    SPROUT = "SPROUT"
    FLOWER = "FLOWER"
    FRUIT = "FRUIT"


class SignupRequest(APIModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)


class LoginRequest(APIModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=64)


class ParentBrief(APIModel):
    id: str
    email: EmailStr


class ParentOut(ParentBrief):
    created_at: datetime


class AuthData(APIModel):
    parent: ParentBrief
    access_token: str
    token_type: str = "bearer"


class ChildCreate(APIModel):
    nickname: str = Field(min_length=1, max_length=50)
    gender: Gender
    birth_year_month: date

    @field_validator("birth_year_month", mode="before")
    @classmethod
    def parse_year_month(cls, value: date | str) -> date:
        if isinstance(value, str) and len(value) == 7:
            value = f"{value}-01"
        if isinstance(value, str):
            value = date.fromisoformat(value)
        if value.day != 1:
            raise ValueError("birthYearMonth는 YYYY-MM 형식이어야 합니다.")
        return value


class ChildUpdate(APIModel):
    nickname: str | None = Field(default=None, min_length=1, max_length=50)
    gender: Gender | None = None
    birth_year_month: date | None = None

    @field_validator("birth_year_month", mode="before")
    @classmethod
    def parse_year_month_if_present(cls, value: date | str | None) -> date | None:
        if isinstance(value, str) and len(value) == 7:
            value = f"{value}-01"
        if isinstance(value, str):
            value = date.fromisoformat(value)
        if value is not None and value.day != 1:
            raise ValueError("birthYearMonth는 YYYY-MM 형식이어야 합니다.")
        return value


class ChildOut(APIModel):
    id: str
    nickname: str
    gender: Gender
    birth_year_month: str
    age_months: int
    in_target_range: bool
    created_at: datetime | None = None


class MeasurementItemCreate(APIModel):
    item_key: ItemKey
    value: float = Field(ge=0, le=9999)


class MeasurementCreate(APIModel):
    type: MeasurementType
    measured_at: date
    center_id: str | None = None
    items: list[MeasurementItemCreate] = Field(min_length=1, max_length=8)

    @model_validator(mode="after")
    def unique_items(self) -> "MeasurementCreate":
        keys = [item.item_key for item in self.items]
        if len(keys) != len(set(keys)):
            raise ValueError("측정 항목은 중복될 수 없습니다.")
        if self.type is MeasurementType.SELF:
            self.center_id = None
        return self


class CenterBrief(APIModel):
    id: str
    name: str


class MeasurementItemOut(APIModel):
    item_key: ItemKey
    label: str
    value: float
    item_grade: Grade | None
    is_weak: bool


class ProfileOut(APIModel):
    strengths: list[ItemKey]
    weaknesses: list[ItemKey]
    undecidable_grades: list[Grade]


class MeasurementOut(APIModel):
    id: str
    child_id: str
    type: MeasurementType
    measured_at: date
    age_months_at_measure: int
    grade: Grade
    center: CenterBrief | None
    items: list[MeasurementItemOut]
    profile: ProfileOut
    created_at: datetime


class MeasurementListItem(APIModel):
    id: str
    type: MeasurementType
    measured_at: date
    grade: Grade


class CenterOut(APIModel):
    id: str
    name: str
    address: str
    sido: str | None
    sido_sigungu: str | None
    latitude: float | None
    longitude: float | None
    distance_km: float | None = None
    reservation_url: str | None = None
    stale: bool = False


class ActivityOut(APIModel):
    id: str
    title: str
    fitness_element: FitnessElement | None
    fitness_elements: list[FitnessElement] = Field(default_factory=list)
    age_group: str | None
    url: str
    description: str | None = None
    thumbnail_url: str | None = None
    fitness_level: str | None = None
    equipment: str | None = None
    training_place: str | None = None
    muscle_part: str | None = None
    duration_seconds: int | None = None


class SeriesPoint(APIModel):
    measured_at: date
    value: float
    type: MeasurementType


class GrowthSeries(APIModel):
    item_key: ItemKey
    label: str
    unit: str
    points: list[SeriesPoint]


class GradeHistory(APIModel):
    measured_at: date
    grade: Grade


class RegionalInsight(APIModel):
    region: str
    region_measure_count: int
    national_avg: float
    relative_level: str
    percentile: int
    message: str
    cta: dict[str, str]


class RegionMapItem(APIModel):
    sido_sigungu: str
    measure_count: int
    participation_rate: float


class SyncRequest(APIModel):
    targets: list[str] = Field(min_length=1)

    @field_validator("targets")
    @classmethod
    def valid_targets(cls, values: list[str]) -> list[str]:
        allowed = {"CENTERS", "ACTIVITIES"}
        if any(value not in allowed for value in values):
            raise ValueError("targets는 CENTERS 또는 ACTIVITIES여야 합니다.")
        return values
