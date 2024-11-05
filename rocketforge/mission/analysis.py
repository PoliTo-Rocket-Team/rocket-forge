import rocketforge.mission.config as config
from rocketpy import Environment
from datetime import datetime


def set_environment():
    # Environment Definition
    date = datetime(config.year, config.month, config.day, config.hour)
    env = Environment(latitude=config.latitude, longitude=config.longitude, elevation=config.elevation)
    env.set_date(date=date, timezone="UTC")
    env.set_atmospheric_model(type="Forecast", file="GFS")
    config.env = env
