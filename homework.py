import dataclasses
from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Класс для создания объектов сообщений"""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE = ('Тип тренировки: {training_type};'
               ' Длительность: {duration:.3f} ч.;'
               ' Дистанция: {distance:.3f} км;'
               ' Ср. скорость: {speed:.3f} км/ч;'
               ' Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Получить сообщение о тренировке"""
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_HOUR = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('В классе Training не переопределен'
                                  ' метод get_spent_calories')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight
                / self.M_IN_KM
                * self.duration
                * self.MIN_IN_HOUR)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: float
    SPORTS_WALKING_CALORIES_MULTIPIER = 0.035
    SPORTS_WALKING_CALORIES_MULTIPIER_2 = 0.029
    KM_IN_H_TO_M_IN_SEC = 0.278
    CM_TO_M = 100
    SQR = 2

    def get_spent_calories(self) -> float:
        return ((self.SPORTS_WALKING_CALORIES_MULTIPIER
                 * self.weight
                 + ((self.get_mean_speed()
                     * self.KM_IN_H_TO_M_IN_SEC)
                    ** self.SQR
                    / (self.height / self.CM_TO_M))
                 * self.SPORTS_WALKING_CALORIES_MULTIPIER_2
                 * self.weight)
                * self.duration
                * self.MIN_IN_HOUR)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    length_pool: float
    count_pool: int
    LEN_STEP = 1.38
    SWIMING_MULTIPLICATE = 1.1
    SWIMING_MULTIPLICATE_2 = 2

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                 + self.SWIMING_MULTIPLICATE)
                * self.SWIMING_MULTIPLICATE_2
                * self.weight
                * self.duration)

    def get_mean_speed(self) -> float:
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""

    TYPES_OF_TRAINING: dict[str, type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type not in TYPES_OF_TRAINING:
        raise ValueError(f'Некорректный код: {workout_type}')
    training_class = TYPES_OF_TRAINING[workout_type]
    if len(data) != len(dataclasses.fields(training_class)):
        raise ValueError(f'Некорректная длина данных {len(data)}')
    return training_class(*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
