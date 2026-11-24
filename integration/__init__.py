"""Integration layer connecting Assessment, Treatment Planning, and Therapy."""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ASSESSMENT_ROOT = REPO_ROOT / "Assessment_Diagnosis_Integration"

if str(ASSESSMENT_ROOT) not in sys.path:
    sys.path.insert(0, str(ASSESSMENT_ROOT))
