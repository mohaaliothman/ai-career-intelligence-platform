import os
from dataclasses import dataclass, field #We use a dataclass to represent database settings within a structured object.

from dotenv import load_dotenv  #Its function is to read the .env file and load the values ​​inside it into Environment Variables.
from sqlalchemy.engine import URL

from src.config.settings import PROJECT_ROOT


ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(dotenv_path=ENV_FILE)


@dataclass(frozen=True) # We use dataclass Because it automatically creates a constructor for us
# Why (frozen=True) This makes the object uneditable after it is created.
class DatabaseSettings:
    driver: str
    host: str
    port: int
    database: str
    username: str
    password: str = field(repr=False) #The password remains inside the object and can be used to connect, but it does not appear when the object is printed.

    @classmethod #Why classmethod Because this function is responsible for creating a new object from DatabaseSettings.
    def from_env(cls) -> "DatabaseSettings":
        required_variables = {
            "DB_HOST": os.getenv("DB_HOST"),
            "DB_NAME": os.getenv("DB_NAME"),
            "DB_USER": os.getenv("DB_USER"),
            "DB_PASSWORD": os.getenv("DB_PASSWORD"),
        } #We did not put DB_PORT here because it has a default value: 5432

        missing_variables = [
            variable_name
            for variable_name, variable_value in required_variables.items()
            if not variable_value
        ]

        if missing_variables:
            missing_variables_text = ", ".join(missing_variables)

            raise ValueError(
                "Missing required database environment variables: "
                f"{missing_variables_text}"
            )

        # Read port
        raw_port = os.getenv("DB_PORT", "5432")

        # Convert the port to a number
        try:
            port = int(raw_port)
        except ValueError as error:
            raise ValueError(
                f"DB_PORT must be a valid integer, but received: {raw_port}"
            ) from error # Why ? Because we want to preserve the original error as the cause of the new error.

        #Create the object
        return cls(
            driver=os.getenv("DB_DRIVER", "postgresql+psycopg"),
            host=required_variables["DB_HOST"],
            port=port,
            database=required_variables["DB_NAME"],
            username=required_variables["DB_USER"],
            password=required_variables["DB_PASSWORD"],
        )

    # Contact address property
    @property
    def url(self) -> URL:
        return URL.create( # Create URL
            drivername=self.driver,
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )


database_settings = DatabaseSettings.from_env() #Create a copy of the settings