from app.services.chat_service import _detect_live_request

def test_live_mandi_request_is_detected():
    assert _detect_live_request("What is today's mandi price of tomatoes?")

def test_live_weather_request_is_detected():
    assert _detect_live_request("What is the current weather today?")
