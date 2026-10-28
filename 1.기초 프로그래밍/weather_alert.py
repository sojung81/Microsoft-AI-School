"""서울의 온도·습도를 수집하고 조건에 따라 macOS 알림을 보내는 실습입니다."""

import argparse
import csv
import json
import math
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

# ---------- 여기의 숫자만 바꾸면 경고 기준과 수집 주기가 바뀝니다. ----------
TEMPERATURE_LIMIT = 30       # 이 온도 이상이면 고온 주의 (°C)
HUMIDITY_LIMIT = 70          # 이 습도 이상이면 습도 주의 (%)
INTERVAL_SECONDS = 60        # 1분 = 60초
REQUEST_TIMEOUT = 15        # API 응답을 기다리는 최대 시간 (초)

LATITUDE = 37.5665          # 서울의 위도
LONGITUDE = 126.9780        # 서울의 경도
SEOUL_TIME = ZoneInfo("Asia/Seoul")

# 도시 중심 좌표입니다. 새 지역도 같은 형식으로 추가할 수 있습니다.
LOCATIONS = {
    "서울": (37.5665, 126.9780), "부산": (35.1796, 129.0756),
    "인천": (37.4563, 126.7052), "대구": (35.8714, 128.6014),
    "대전": (36.3504, 127.3845), "광주": (35.1595, 126.8526),
    "울산": (35.5384, 129.3114), "세종": (36.4800, 127.2890),
    "수원": (37.2636, 127.0286), "강릉": (37.7519, 128.8761),
    "제주": (33.4996, 126.5312),
}

# 실행한 터미널의 위치와 관계없이 이 파이썬 파일 옆에 저장합니다.
PROJECT_DIR = Path(__file__).resolve().parent
LATEST_FILE = PROJECT_DIR / "weather_latest.json"
HISTORY_FILE = PROJECT_DIR / "weather_history.csv"
CSV_FIELDS = ["collected_at", "data_time", "location",
              "temperature_c", "relative_humidity_percent", "weather_description",
              "apparent_temperature_c", "precipitation_mm", "rain_mm", "snowfall_cm",
              "wind_speed_kmh", "pm2_5", "pm10", "air_quality_time", "us_aqi"]


def parse_weather(response, location="서울"):
    """API 응답에서 필요한 값을 꺼내고 누락·잘못된 값을 검사합니다."""
    if not isinstance(response, dict):
        raise ValueError("API 응답이 JSON 객체가 아닙니다.")
    current = response.get("current")
    if not isinstance(current, dict):
        raise ValueError("API 응답에 current 데이터가 없습니다.")

    temperature = current.get("temperature_2m")
    humidity = current.get("relative_humidity_2m")
    data_time = current.get("time")
    for name, value in [("온도", temperature), ("습도", humidity)]:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{name} 데이터가 없거나 숫자가 아닙니다.")
        if not math.isfinite(value):
            raise ValueError(f"{name} 데이터가 유효한 숫자가 아닙니다.")
    if not 0 <= humidity <= 100:
        raise ValueError("습도는 0~100%여야 합니다.")
    if not isinstance(data_time, str) or not data_time:
        raise ValueError("데이터 기준 시각이 없습니다.")

    # API에 서울 시간대를 요청했으므로 시각에 +09:00 정보를 붙입니다.
    measured_at = datetime.fromisoformat(data_time)
    if measured_at.tzinfo is None:
        measured_at = measured_at.replace(tzinfo=SEOUL_TIME)

    result = {
        "location": location,
        "source": "Open-Meteo",
        "collected_at": datetime.now(SEOUL_TIME).isoformat(timespec="seconds"),
        "data_time": measured_at.astimezone(SEOUL_TIME).isoformat(timespec="seconds"),
        "temperature_c": temperature,
        "relative_humidity_percent": humidity,
    }
    # 부가 항목이 누락되더라도 온도·습도 수집은 계속합니다.
    fields = {"weather_code": "weather_code", "apparent_temperature": "apparent_temperature_c",
              "precipitation": "precipitation_mm", "rain": "rain_mm",
              "snowfall": "snowfall_cm", "wind_speed_10m": "wind_speed_kmh"}
    for api_name, saved_name in fields.items():
        result[saved_name] = optional_number(current.get(api_name))
    result["weather_description"] = describe_weather(result["weather_code"])
    return result


def optional_number(value):
    """없는 수치를 0으로 만들지 않고 None(확인 불가)으로 둡니다."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return value if math.isfinite(value) else None


def describe_weather(code):
    """Open-Meteo WMO 코드를 비·눈·맑음 등 한국어로 표시합니다."""
    descriptions = {
        0: "맑음", 1: "대체로 맑음", 2: "구름 조금", 3: "흐림",
        45: "안개", 48: "착빙 안개", 51: "약한 이슬비", 53: "이슬비", 55: "강한 이슬비",
        56: "어는 이슬비", 57: "강한 어는 이슬비", 61: "약한 비", 63: "비", 65: "강한 비",
        66: "어는 비", 67: "강한 어는 비", 71: "약한 눈", 73: "눈", 75: "강한 눈",
        77: "싸락눈", 80: "약한 소나기", 81: "소나기", 82: "강한 소나기",
        85: "약한 눈 소나기", 86: "강한 눈 소나기", 95: "뇌우", 96: "우박 동반 뇌우",
        97: "강한 뇌우", 99: "강한 우박·뇌우",
    }
    return descriptions.get(code, "확인 불가")


def fetch_air_quality(location="서울"):
    """무료 대기질 API에서 PM2.5·PM10과 미국 AQI를 읽습니다."""
    latitude, longitude = LOCATIONS[location]
    parameters = {"latitude": latitude, "longitude": longitude,
                  "current": "pm2_5,pm10,us_aqi", "timezone": "Asia/Seoul"}
    url = "https://air-quality-api.open-meteo.com/v1/air-quality?" + urlencode(parameters)
    request = Request(url, headers={"User-Agent": "SeoulWeatherAlert/1.0"}, method="GET")
    with urlopen(request, timeout=REQUEST_TIMEOUT) as response:
        payload = json.load(response)
    current = payload.get("current") if isinstance(payload, dict) else None
    if not isinstance(current, dict):
        raise ValueError("대기질 current 데이터가 없습니다.")
    result = {}
    for name in ["pm2_5", "pm10", "us_aqi"]:
        value = optional_number(current.get(name))
        result[name] = value if value is not None and value >= 0 else None
    if result["pm2_5"] is None and result["pm10"] is None:
        raise ValueError("미세먼지 수치가 없습니다.")
    moment = datetime.fromisoformat(current["time"])
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=SEOUL_TIME)
    result["air_quality_time"] = moment.isoformat()
    return result


def fetch_weather(location="서울"):
    """HTTP GET 요청을 보내고 JSON 응답을 읽습니다. API Key는 필요 없습니다."""
    if location not in LOCATIONS:
        raise ValueError("지원하지 않는 지역입니다.")
    latitude, longitude = LOCATIONS[location]
    parameters = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,weather_code,apparent_temperature,precipitation,rain,snowfall,wind_speed_10m",
        "hourly": "temperature_2m,relative_humidity_2m",  # 그래프용 기온·습도
        "past_days": 2,              # 어제·그제의 시간별 자료도 요청
        "forecast_days": 1,
        "temperature_unit": "celsius",
        "timezone": "Asia/Seoul",
    }
    url = "https://api.open-meteo.com/v1/forecast?" + urlencode(parameters)
    request = Request(url, headers={"User-Agent": "SeoulWeatherAlert/1.0"}, method="GET")
    with urlopen(request, timeout=REQUEST_TIMEOUT) as response:
        payload = json.load(response)
        weather = parse_weather(payload, location)
        weather["hourly_history"] = parse_hourly_history(payload)
    try:
        weather.update(fetch_air_quality(location))
        weather["air_quality_error"] = ""
    except (URLError, TimeoutError, OSError, ValueError, KeyError, TypeError) as error:
        # 미세먼지 API만 실패하면 날씨 수집은 유지하고 미세먼지를 확인 불가로 표시합니다.
        weather.update(pm2_5=None, pm10=None, us_aqi=None, air_quality_time=None,
                       air_quality_error=str(error))
        print(f"[대기질 오류] 날씨 수집은 계속합니다: {error}")
    return weather


def parse_hourly_history(response):
    """기상 모델의 과거 시간별 기온입니다. 직접 수집한 CSV 기록과는 구분합니다."""
    hourly = response.get("hourly", {})
    if not isinstance(hourly, dict):
        return []
    times = hourly.get("time", [])
    temperatures = hourly.get("temperature_2m", [])
    if not isinstance(times, list) or not isinstance(temperatures, list):
        return []
    humidities = hourly.get("relative_humidity_2m", [])
    if not isinstance(humidities, list):
        humidities = []
    now = datetime.now(SEOUL_TIME)
    history = []
    for index, (value_time, temperature) in enumerate(zip(times, temperatures)):
        if isinstance(temperature, bool) or not isinstance(temperature, (int, float)):
            continue
        if not math.isfinite(temperature):
            continue
        try:
            moment = datetime.fromisoformat(value_time)
            if moment.tzinfo is None:
                moment = moment.replace(tzinfo=SEOUL_TIME)
        except (TypeError, ValueError):
            continue
        if moment <= now:  # 아직 오지 않은 예측 시간은 과거 그래프에서 제외합니다.
            humidity = optional_number(humidities[index]) if index < len(humidities) else None
            if humidity is not None and not 0 <= humidity <= 100:
                humidity = None
            history.append({"data_time": moment.isoformat(), "temperature_c": temperature,
                            "relative_humidity_percent": humidity})
    return history


def load_alert_state(location=None):
    """지난 알림 상태를 읽어 프로그램을 다시 켜도 중복 알림을 줄입니다."""
    state = {"high_temperature": False, "high_humidity": False}
    try:
        previous = json.loads(LATEST_FILE.read_text(encoding="utf-8"))
        if not isinstance(previous, dict):
            raise ValueError("최신 데이터가 JSON 객체가 아닙니다.")
        city = location or previous.get("location", "서울")
        by_city = previous.get("alert_states_by_location", {})
        if not isinstance(by_city, dict):
            by_city = {}
        saved = by_city.get(city)
        if saved is None:
            saved = previous.get("alert_state", {}) if previous.get("location", "서울") == city else {}
        if not isinstance(saved, dict):
            raise ValueError("알림 상태가 올바르지 않습니다.")
        for name in state:
            state[name] = saved.get(name) is True
    except FileNotFoundError:
        pass  # 처음 실행해서 파일이 없는 경우에는 기본 상태로 시작합니다.
    except (OSError, ValueError) as error:
        print(f"[안내] 이전 알림 상태를 읽지 못해 기본값으로 시작합니다: {error}")
    return state


def send_notification(message):
    """AppleScript로 이 맥의 알림 센터에 알림을 요청합니다."""
    if sys.platform != "darwin":
        print("[알림 오류] macOS에서만 알림을 보낼 수 있습니다.")
        return False

    # 메시지를 명령어에 붙이지 않고 인자로 전달해 따옴표도 안전하게 처리합니다.
    script = ('on run argv\n'
              'display notification (item 2 of argv) with title (item 1 of argv)\n'
              'end run')
    try:
        subprocess.run(
            ["/usr/bin/osascript", "-e", script, "서울 온습도 알리미", message],
            check=True, capture_output=True, text=True, timeout=10,
        )
        print("[알림 요청 완료] 배너 표시는 macOS 알림 설정에 따라 달라집니다.")
        return True
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
        detail = getattr(error, "stderr", None) or str(error)
        print(f"[알림 오류] {detail.strip()}")
        return False  # 다음 수집 때 다시 시도할 수 있도록 성공으로 기록하지 않습니다.


def check_alerts(weather, previous_state, allow_notifications=True):
    """정상 → 경고로 바뀔 때만 알림을 보내고, 정상이 되면 상태를 해제합니다."""
    temperature = weather["temperature_c"]
    humidity = weather["relative_humidity_percent"]
    conditions = [
        ("high_temperature", temperature >= TEMPERATURE_LIMIT,
         f"고온 주의: {weather['location']} 기온 {temperature:g}°C (기준 {TEMPERATURE_LIMIT:g}°C 이상)"),
        ("high_humidity", humidity >= HUMIDITY_LIMIT,
         f"습도 주의: {weather['location']} 상대습도 {humidity:g}% (기준 {HUMIDITY_LIMIT:g}% 이상)"),
    ]
    new_state = previous_state.copy()
    for name, is_warning, message in conditions:
        if not is_warning:
            new_state[name] = False
            continue
        print(message)
        if previous_state[name]:
            print("[중복 방지] 같은 경고가 유지되어 알림을 생략합니다.")
        elif allow_notifications:
            new_state[name] = send_notification(message)
        else:
            print("[알림 생략] --no-notify 모드입니다.")
    return new_state


def save_weather(weather):
    """CSV 항목이 늘어나면 기존 기록을 보존해 열을 추가한 뒤 새 기록을 붙입니다."""
    if HISTORY_FILE.exists() and HISTORY_FILE.stat().st_size:
        with HISTORY_FILE.open(encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            old_fields = reader.fieldnames or []
            old_rows = list(reader) if old_fields != CSV_FIELDS else None
        if old_rows is not None:
            # 이전 버전의 온도·습도 기록은 유지하고 없었던 항목은 빈칸으로 둡니다.
            fields = CSV_FIELDS + [field for field in old_fields if field not in CSV_FIELDS]
            temporary_csv = HISTORY_FILE.with_suffix(".tmp")
            with temporary_csv.open("w", encoding="utf-8", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fields)
                writer.writeheader()
                writer.writerows(old_rows)
            temporary_csv.replace(HISTORY_FILE)
            active_fields = fields
        else:
            active_fields = CSV_FIELDS
    else:
        active_fields = CSV_FIELDS

    # 도시를 바꿔도 이전 도시의 알림 상태를 잃지 않게 보관합니다.
    by_city = {}
    try:
        previous = json.loads(LATEST_FILE.read_text(encoding="utf-8"))
        if isinstance(previous, dict):
            saved = previous.get("alert_states_by_location", {})
            if isinstance(saved, dict):
                by_city.update(saved)
            if isinstance(previous.get("alert_state"), dict):
                by_city[previous.get("location", "서울")] = previous["alert_state"]
    except (OSError, ValueError):
        pass
    if isinstance(weather.get("alert_state"), dict):
        by_city[weather["location"]] = weather["alert_state"]
    weather["alert_states_by_location"] = by_city
    temporary = LATEST_FILE.with_suffix(".tmp")
    temporary.write_text(json.dumps(weather, ensure_ascii=False, indent=2) + "\n",
                         encoding="utf-8")
    temporary.replace(LATEST_FILE)
    needs_header = not HISTORY_FILE.exists() or HISTORY_FILE.stat().st_size == 0
    with HISTORY_FILE.open("a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=active_fields, extrasaction="ignore")
        if needs_header:
            writer.writeheader()
        writer.writerow(weather)


def collect_once(previous_state, allow_notifications=True):
    """한 번 수집합니다. 실패하더라도 이전 상태와 파일을 유지하고 돌아옵니다."""
    try:
        weather = fetch_weather()
    except (URLError, TimeoutError, OSError, ValueError) as error:
        print(f"[수집 오류] 인터넷 연결과 API 응답을 확인해주세요: {error}")
        return previous_state, False

    print(f"\n[{weather['collected_at']}] 서울: "
          f"{weather['temperature_c']:g}°C / 습도 {weather['relative_humidity_percent']:g}%")
    print(f"데이터 기준 시각: {weather['data_time']}")
    new_state = check_alerts(weather, previous_state, allow_notifications)
    weather["alert_state"] = new_state
    try:
        save_weather(weather)
    except OSError as error:
        print(f"[저장 오류] 프로젝트 폴더의 쓰기 권한과 남은 공간을 확인해주세요: {error}")
        return new_state, False
    print("[저장 완료] weather_latest.json 갱신 / weather_history.csv 한 줄 추가")
    return new_state, True


def main(argv=None):
    parser = argparse.ArgumentParser(description="서울 온도·습도 수집 및 macOS 알림")
    parser.add_argument("--preview", action="store_true", help="눈·비 효과 미리보기 창도 함께 열기")
    parser.add_argument("--console", action="store_true", help="창 대신 터미널에서 1분마다 실행")
    parser.add_argument("--once", action="store_true", help="지금 한 번만 수집하고 종료")
    parser.add_argument("--no-notify", action="store_true", help="실제 알림 없이 출력·저장만 실행")
    parser.add_argument("--test-notification", action="store_true", help="날씨와 관계없이 테스트 알림 1회 요청")
    args = parser.parse_args(argv)

    try:
        # 옵션 없이 ▶ 실행하면 대시보드 창을 엽니다. 기존 1회 테스트도 유지합니다.
        if not args.console and not args.once and not args.test_notification:
            from weather_dashboard import launch
            launch(allow_notifications=not args.no_notify, preview=args.preview)
            return 0

        if args.test_notification:
            if args.no_notify:
                print("테스트 알림을 보내려면 --no-notify를 빼주세요.")
                return 1
            return 0 if send_notification("테스트 알림입니다. 온습도 알리미가 준비되었습니다.") else 1

        state = load_alert_state("서울")
        print(f"사용 Python: {sys.executable}")
        print(f"저장 폴더: {PROJECT_DIR}")
        while True:
            started = time.monotonic()
            state, success = collect_once(state, not args.no_notify)
            if args.once:
                return 0 if success else 1
            # 요청에 걸린 시간을 제외해 약 1분 간격으로 수집을 시작합니다.
            remaining = max(0, INTERVAL_SECONDS - (time.monotonic() - started))
            print(f"다음 수집까지 약 {remaining:.0f}초 대기합니다. 종료: Ctrl+C")
            time.sleep(remaining)
    except KeyboardInterrupt:
        print("\n[종료] 사용자가 중단했습니다. 저장된 데이터는 남아 있습니다.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
