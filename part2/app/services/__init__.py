#!/usr/bin/python3
"""
Shared Facade instance (singleton) for the entire app.
All API modules must import this to use the same in-memory repositories.
"""
from app.services.facade import HBnBFacade

facade = HBnBFacade()
