from pydantic import BaseModel


class Property(BaseModel):
    """
    A model representing a property.

    Attributes:
        type (str): The type of the property.
        sector (str): The sector where the property is located.
        net_usable_area (float): The net usable area of the property.
        net_area (float): The net area of the property.
        n_rooms (int): The number of rooms in the property.
        n_bathroom (int): The number of bathrooms in the property.
        latitude (float): The latitude coordinate of the property.
        longitude (float): The longitude coordinate of the property.
        price (float): The price of the property.
    """
    type: str
    sector: str
    net_usable_area: float
    net_area: float
    n_rooms: int
    n_bathroom: int
    latitude: float
    longitude: float
    price: float
