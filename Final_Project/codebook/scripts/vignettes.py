#!/usr/bin/env python3
"""Constructed cases for labels that real windows almost never showed. Not data. `intended` is the author's answer, kept out of the coder file.
Writes pilot/r3/vignettes.jsonl (for coders) and pilot_results/vignette_key.csv (the key)."""
import csv, json, os
from views import CODEBOOK

V = [
 ("VIG-01","C1","Summarize the main finding of this study on sleep and memory: [abstract text].","The study shows that sleep improves memory in all adults.","Are you sure that's true for all adults? Can you give me references?","V2_AI_SELF_CHECK","U4_CHAT_ITERATE","D2_AI_PROPOSED_OPEN"),
 ("VIG-02","C1","What does the literature say about remote work and productivity?","Most studies find remote work raises productivity by about 13%.","Can you double-check that figure and explain how you got it?","V2_AI_SELF_CHECK","U4_CHAT_ITERATE","D2_AI_PROPOSED_OPEN"),
 ("VIG-03","C1","Draft a claim about tutoring effects for my paper.","Tutoring improves outcomes for all students regardless of age.","That overreaches. My sample is only first-year undergraduates, so it can't cover all ages. Limit it to that group.","V3_REASONED_CHALLENGE","U4_CHAT_ITERATE","D3_HUMAN_CHOSE_REVISED"),
 ("VIG-04","C1","Give me a reason schools should ban phones.","Phones harm attention, and bans always raise test scores.","Always is too strong, since a ban can't help a school where phones were already barely used. Rewrite without that.","V3_REASONED_CHALLENGE","U4_CHAT_ITERATE","D3_HUMAN_CHOSE_REVISED"),
 ("VIG-05","C1","Summarize Table 2 of the paper I pasted: [table].","Table 2 shows that treatment raised scores by 20% in both groups.","Table 2 in the paper says 20% only in group A, and group B was 4%. Fix it.","V4_SOURCE_COMPARISON","U4_CHAT_ITERATE","D3_HUMAN_CHOSE_REVISED"),
 ("VIG-06","C1","What does this abstract conclude? [abstract]","It concludes that the intervention works for all patients.","The abstract's last line reads \"in patients under 40 only\", and your summary drops that, which changes the result. Please correct it.","V4_SOURCE_COMPARISON","U4_CHAT_ITERATE","D3_HUMAN_CHOSE_REVISED"),
 ("VIG-07","C1","Generate an outline for my literature review.","1. Background 2. Methods in prior work 3. Gaps","Great, I'll use this outline for my review.","V0_NONE_VISIBLE","U5_CHAT_ACCEPT","D4_AI_PROPOSAL_TAKEN"),
 ("VIG-08","C1","Suggest a title for my thesis on urban heat.","Cooling the Concrete: Urban Heat and Inequality","Thank you!","V0_NONE_VISIBLE","U8_MOVED_ON","D2_AI_PROPOSED_OPEN"),
 ("VIG-09","C1","Propose a thesis for my essay on tariffs.","Tariffs mainly harm consumers through higher prices.","No, that's not what I want at all. Give me something else.","V0_NONE_VISIBLE","U6_REJECT","D3_HUMAN_CHOSE_REVISED"),
 ("VIG-10","C1","Give me three research questions on peer review.","(a) Does blinding reduce bias? (b) Does reviewer pay change speed? (c) Do AI tools change comments?","I'll go with (b), and I'm adding that it should be limited to medical journals, since that's my field.","V3_REASONED_CHALLENGE","U4_CHAT_ITERATE","D3_HUMAN_CHOSE_REVISED"),
 ("VIG-11","C1","Find me five recent papers on writing feedback.","1. Lee 2021 ... 2. Park 2022 ... [five entries]","Do these references actually exist? Where did you get them?","V2_AI_SELF_CHECK","U4_CHAT_ITERATE","D2_AI_PROPOSED_OPEN"),
 ("VIG-12","C1","Rewrite my sentence about the survey results: [sentence].","The survey proves that students prefer online classes.","My data show only 54% prefer them, so \"proves\" and \"prefer\" misstate it. Here are the numbers: [table].","V4_SOURCE_COMPARISON","U4_CHAT_ITERATE","D3_HUMAN_CHOSE_REVISED"),
]


def main():
    d = os.path.join(CODEBOOK, "pilot", "r3")
    with open(os.path.join(d, "vignettes.jsonl"), "w", encoding="utf-8") as f:
        for i, cov, rq, rs, nx, *_ in V:
            f.write(json.dumps({"window_id": i, "dataset": "CONSTRUCTED", "coverage": cov, "turn_order": 2, "prior_turns": [], "editor_before_request": None,
                                "request": rq, "response": rs, "next_actions_text": "NEXT USER TURN: " + nx}) + "\n")
    os.makedirs(os.path.join(CODEBOOK, "pilot_results"), exist_ok=True)
    with open(os.path.join(CODEBOOK, "pilot_results", "vignette_key.csv"), "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["window_id", "verification", "uptake", "decision"])
        for i, _, _, _, _, v, u, de in V:
            w.writerow([i, v, u, de])


if __name__ == "__main__":
    main()
