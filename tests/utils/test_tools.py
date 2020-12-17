from buildtest.utils.tools import Hasher


def test_Hasher():
    d = {
        "person": {
            "first": "John",
            "last": "Doe",
            "city": "Manchester",
            "country": "USA",
        }
    }
    h = Hasher(d)

    assert "John" == h.get("person.first")
    assert "Doe" == h.get("person/last", sep="/")

    car_types = ["Sedan", "All-whell", "4-whell"]
    h["car"]["type"] = car_types
    assert "car" in h.keys()
    assert "type" in h["car"].keys()
    print(h)

    assert h.get("car.type") == car_types
