import re
from typing import List
from swift.plugin.orm import ORM, orms


class MCQAccBaseline(ORM):
    def __call__(
        self, completions: List[str], solution: List[str] = None, **kwargs
    ) -> List[float]:
        rewards = []
        ground_truths = solution if solution is not None else kwargs.get("solution", [])

        for pred_text, gt_text in zip(completions, ground_truths):
            gt_match = re.search(
                r"<answer>\s*([A-Z])\s*</answer>", gt_text, re.IGNORECASE
            )
            clean_gt = gt_match.group(1).upper() if gt_match else None

            pred_match = re.search(
                r"<answer>\s*([A-Z])\s*</answer>", pred_text, re.IGNORECASE
            )
            pred_letter = pred_match.group(1).upper() if pred_match else None

            if clean_gt and pred_letter and clean_gt == pred_letter:
                rewards.append(1.0)
            else:
                rewards.append(0.0)

        return rewards


class FormatRewardORM(ORM):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pattern = re.compile(
            r"(?s)"
            r".*?"
            r"<thinking>.*?</thinking>"
            r"\s*"
            r"<answer>.*?</answer>"
            r".*"
        )

    def __call__(self, completions: List[str], **kwargs) -> List[float]:
        rewards = []
        for completion in completions:
            if self.pattern.fullmatch(completion) or self.pattern.match(completion):
                rewards.append(1.0)
            else:
                rewards.append(0.0)
        return rewards


orms["base_acc"] = MCQAccBaseline
orms["format_acc"] = FormatRewardORM
