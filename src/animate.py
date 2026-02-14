import atexit
import re
import shutil
import sys
import time

import colorama
import httpx
from wcwidth import wcswidth

colorama.init()

# API_URL = "https://querycourse.ntust.edu.tw/QueryCourse/api//courses"
API_URL = "http://localhost:8000/QueryCourse/api//courses"
PAYLOAD = {
    "Semester": "1142",
    "CourseNo": "",
    "CourseName": "",
    "CourseTeacher": " ",
    "Dimension": "",
    "CourseNotes": "",
    "CampusNotes": "",
    "ForeignLanguage": 0,
    "OnlyGeneral": 0,
    "OnleyNTUST": 0,
    "OnlyMaster": 0,
    "OnlyUnderGraduate": 0,
    "OnlyNode": 0,
    "Language": "zh",
}
HEADERS = {"Content-Type": "application/json; charset=utf-8"}

INTERVAL_SECONDS = 3
TYPE_DELAY = 0.001

COL1_WIDTH = 54
COL2_WIDTH = 16

prev_state: dict[str, dict[str, object]] = {}

ANSI_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


def pad_vis(s: str, width: int) -> str:
    """根據顯示寬度補齊到指定長度"""
    cur = 0
    out = []
    for ch in s:
        w = wcswidth(ch)
        w = max(w, 0)
        if cur + w > width:
            break
        out.append(ch)
        cur += w
    out_s = "".join(out)
    pad = width - wcswidth(out_s)
    return out_s + " " * pad


def fetch_courses(client: httpx.Client) -> dict:
    r = client.post(API_URL, json=PAYLOAD, headers=HEADERS, timeout=30.0)
    r.raise_for_status()
    return r.json()


def parse_int_or_none(val: object) -> int | None:
    if isinstance(val, int):
        return val
    if isinstance(val, str) and val.isdigit():
        return int(val)
    return None


def build_colored_line(
    course_no: str,
    course_name: str,
    choose_val: int | None,
    restrict2: str,
    classroom: str,
    prev_choose_val: int | None,
) -> str:
    choose_color = colorama.Fore.YELLOW
    if prev_choose_val is not None and choose_val is not None:
        if choose_val > prev_choose_val:
            choose_color = colorama.Fore.RED
        elif choose_val < prev_choose_val:
            choose_color = colorama.Fore.GREEN

    part1_vis = f"{course_no} | {course_name}"
    choose_str = "-" if choose_val is None else str(choose_val)
    part2_vis = (
        "+" if choose_color == colorama.Fore.RED else "-"
    ) + f" {choose_str} / {restrict2}"
    part3_vis = f"| {classroom}"

    part1_pad = pad_vis(part1_vis, COL1_WIDTH)
    part2_pad = pad_vis(part2_vis, COL2_WIDTH)

    part1_col = f"{colorama.Fore.CYAN}{part1_pad}{colorama.Style.RESET_ALL}"

    idx = part2_pad.find(choose_str)
    if idx >= 0:
        prefix = part2_pad[:idx]
        suffix = part2_pad[idx + len(choose_str) :]
        part2_col = (
            f"{colorama.Fore.YELLOW}{prefix}"
            f"{choose_color}{choose_str}{colorama.Fore.YELLOW}"
            f"{suffix}{colorama.Style.RESET_ALL}"
        )
    else:
        part2_col = f"{colorama.Fore.YELLOW}{part2_pad}{colorama.Style.RESET_ALL}"

    part3_col = f"{colorama.Fore.GREEN}{part3_vis}{colorama.Style.RESET_ALL}"
    return f"{part1_col}{part2_col}{part3_col}"


def type_out(line: str) -> None:
    i = 0
    while i < len(line):
        m = ANSI_RE.match(line, i)
        if m:
            print(m.group(0), end="", flush=True)
            i = m.end()
        else:
            print(line[i], end="", flush=True)
            time.sleep(TYPE_DELAY)
            i += 1
    if not line.endswith("\n"):
        print()

def enable_sticky_title(title: str) -> None:
    rows = shutil.get_terminal_size().lines or 24
    sys.stdout.write("\x1b[2J")
    sys.stdout.write(f"\x1b[2;{rows}r")
    sys.stdout.write("\x1b[1;1H")
    sys.stdout.write(f"{colorama.Fore.MAGENTA}{title}{colorama.Style.RESET_ALL}\n")
    sys.stdout.write("\x1b[2;1H")
    sys.stdout.flush()


def reset_scroll_region() -> None:
    sys.stdout.write("\x1b[r")
    sys.stdout.flush()


atexit.register(reset_scroll_region)


def main() -> None:
    first_run = True
    with httpx.Client(http2=True) as client:
        while True:
            try:
                data = fetch_courses(client)
                data_sorted = sorted(data, key=lambda c: c.get("CourseNo") or "")

                to_print: list[str] = []

                for c in data_sorted:
                    course_no = c.get("CourseNo") or "-"
                    name = c.get("CourseName") or "-"
                    choose_raw = c.get("ChooseStudent")
                    choose_val = parse_int_or_none(choose_raw)
                    restrict2 = c.get("Restrict2") or "-"
                    room = c.get("ClassRoomNo") or "-"

                    prev = prev_state.get(course_no)

                    # 只檢查人數變化
                    changed = prev is not None and choose_raw != prev.get("choose_raw")

                    if not first_run and changed:
                        prev_choose_val = parse_int_or_none(prev.get("choose_raw"))
                        colored_line = build_colored_line(
                            course_no,
                            name,
                            choose_val,
                            restrict2,
                            room,
                            prev_choose_val,
                        )
                        to_print.append(colored_line)

                    prev_state[course_no] = {
                        "name": name,
                        "choose_raw": choose_raw,
                        "restrict2": restrict2,
                        "room": room,
                    }

                if first_run:
                    enable_sticky_title("加退選即時通")
                    first_run = False
                else:
                    for line in to_print:
                        type_out(line + "\n")

                time.sleep(INTERVAL_SECONDS)

            except KeyboardInterrupt:
                break
            except Exception as e:
                time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
