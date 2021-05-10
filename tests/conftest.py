import pytest
from app import create_app
from app import db
from app.models.planet import Planet

@pytest.fixture
def app():
    app = create_app({"TESTING": True})
    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def two_saved_planets(app):
    swirly_planet = Planet(name="Swirly Planet",
                            description="a swirl planet",
                            size="Small")
    loopy_planet = Planet(name="Loopy Planet",
                            description="a loop planet",
                            size="Medium")
    db.session.add_all([swirly_planet, loopy_planet])
    db.session.commit()