"""Run from the unpacked folder. Default demo needs no API key."""
import argparse
import os
from getpass import getpass
from pathlib import Path

from assessment_component import AssessmentService
from assessment_component.evaluate import evaluate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live",action="store_true",help="Type fictional replies and use the NVIDIA assessment model")
    parser.add_argument("--storage",type=Path,default=Path("demo_sessions"))
    args = parser.parse_args()
    if args.live and not os.getenv("NVIDIA_API_KEY"):
        os.environ["NVIDIA_API_KEY"] = getpass("NVIDIA key (hidden): ").strip()
    service = AssessmentService(args.storage, mock=not args.live)
    turn = service.start_session(fictional_name="Alex", age=30)
    scripted = iter(["I've felt low for three weeks.", "I missed a shift because I couldn't concentrate."])
    while True:
        print("Interviewer:", turn["text"])
        if turn["state"] == "complete":
            break
        reply = input("Fictional reply: ") if args.live else next(scripted)
        if not args.live:
            print("Fictional reply:", reply)
        turn = service.submit_reply(turn["session_id"], question_id=turn["question_id"], text=reply)
    folder = args.storage/turn["session_id"]
    print("Session folder:", folder.resolve())
    print("Output contract passed:", evaluate(folder)["passed"])


if __name__ == "__main__":
    main()
