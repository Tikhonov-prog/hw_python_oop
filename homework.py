from dataclasses import dataclass, asdict
from typing import Union


@dataclass
class InfoMessage:
    """Класс для создания объектов сообщений"""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message = ('Тип тренировки: {};'
               ' Длительность: {:.3f} ч.;'
               ' Дистанция: {:.3f} км;'
               ' Ср. скорость: {:.3f} км/ч;'
               ' Потрачено ккал: {:.3f}.')

    def get_message(self) -> str:
        """Получить сообщение о тренировке"""
        return self.message.format(*asdict(self).values())


@dataclass
class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_HOUR = 60
    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(type(self).__name__,
                                   self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories()
                                   )
        return info_message


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

    SPORTS_WALKING_CALORIES_MULTIPIER = 0.035
    SPORTS_WALKING_CALORIES_MULTIPIER_2 = 0.029
    KM_IN_H_TO_M_IN_SEC = 0.278
    CM_TO_M = 100
    SQR = 2
    height: float

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

    LEN_STEP = 1.38
    SWIMING_MULTIPLICATE = 1.1
    SWIMING_MULTIPLICATE_2 = 2
    length_pool: float
    count_pool: int

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


def read_package(workout_type: str, data: Union[int, float]) -> Training:
    """Прочитать данные полученные от датчиков."""

    TYPES_OF_TRAINING: dict[str, tuple[type[Training], int]] = {
        'SWM': (Swimming, 5),
        'RUN': (Running, 3),
        'WLK': (SportsWalking, 4)
    }

    if workout_type not in TYPES_OF_TRAINING:
        raise ValueError('Некорректное имя')
    training_class, num_in_packages = TYPES_OF_TRAINING[workout_type]
    if len(data) != num_in_packages:
        raise ValueError('Некорректное число данных')
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
        training = read_package(workout_type, data)
        main(training)
