"""
Further expand synonyms.json with all categories from GodGuide.md Section 2.
"""
import json, os

RULES_DIR = r"C:\Users\gkedi\.gemini\antigravity\scratch\turnitout-humanizer\src\turnitout\rules"
syn_path = os.path.join(RULES_DIR, "synonyms.json")

with open(syn_path, "r", encoding="utf-8") as f:
    syns = json.load(f)

MORE_SYNS = {
    "compute": ["enumerate", "ascertain", "reckon", "calculate"],
    "computes": ["enumerates", "ascertains", "reckons", "calculates"],
    "computed": ["enumerated", "ascertained", "reckoned", "calculated"],
    "computing": ["enumerating", "ascertaining", "reckoning", "calculating"],

    "derive": ["extrapolate", "educe", "elicit", "deduce"],
    "derives": ["extrapolates", "educes", "elicits", "deduces"],
    "derived": ["extrapolated", "educed", "elicited", "deduced"],
    "deriving": ["extrapolating", "educing", "eliciting", "deducing"],

    "formulate": ["posit", "propound", "articulate", "frame"],
    "formulates": ["posits", "propounds", "articulates", "frames"],
    "formulated": ["posited", "propounded", "articulated", "framed"],
    "formulating": ["positing", "propounding", "articulating", "framing"],

    "integrate": ["amalgamate", "synthesize", "consolidate", "fuse"],
    "integrates": ["amalgamates", "synthesizes", "consolidates", "fuses"],
    "integrated": ["amalgamated", "synthesized", "consolidated", "fused"],
    "integrating": ["amalgamating", "synthesizing", "consolidating", "fusing"],

    "simulate": ["emulate", "replicate", "model"],
    "simulates": ["emulates", "replicates", "models"],
    "simulated": ["emulated", "replicated", "modeled"],
    "simulating": ["emulating", "replicating", "modeling"],

    "validate": ["corroborate", "substantiate", "authenticate"],
    "validates": ["corroborates", "substantiates", "authenticates"],
    "validated": ["corroborated", "substantiated", "authenticated"],
    "validating": ["corroborating", "substantiating", "authenticating"],

    "verify": ["ascertain", "confirm", "attest"],
    "verifies": ["ascertains", "confirms", "attests"],
    "verified": ["ascertained", "confirmed", "attested"],
    "verifying": ["ascertaining", "confirming", "attesting"],

    "characterize": ["delineate", "elucidate", "explicate"],
    "characterizes": ["delineates", "elucidates", "explicates"],
    "characterized": ["delineated", "elucidated", "explicated"],
    "characterizing": ["delineating", "elucidating", "explicating"],

    "relevant": ["germane", "pertinent", "apposite", "apropos"],
    "relevance": ["pertinence", "appositeness", "applicability"],
    "substantial": ["considerable", "pronounced", "appreciable", "weighty"],
    "approximate": ["proximate", "estimated", "inexact"],
    "approximates": ["approaches", "estimates", "mirrors"],
    "approximated": ["estimated", "computed approximately", "modeled"],
    "approximating": ["estimating", "approaching", "modeling"],

    "converge": ["tend toward", "approach", "coalesce"],
    "converges": ["tends toward", "approaches", "coalesces"],
    "converged": ["tended toward", "approached", "coalesced"],
    "converging": ["tending toward", "approaching", "coalescing"],

    "vary": ["fluctuate", "differ", "deviate", "oscillate"],
    "varies": ["fluctuates", "differs", "deviates", "oscillates"],
    "varied": ["fluctuated", "differed", "deviated", "oscillated"],
    "varying": ["fluctuating", "differing", "deviating", "oscillating"],

    "construct": ["assemble", "fabricate", "erect", "synthesize"],
    "constructs": ["assembles", "fabricates", "erects", "synthesizes"],
    "constructed": ["assembled", "fabricated", "erected", "synthesized"],
    "constructing": ["assembling", "fabricating", "erecting", "synthesizing"],

    "modify": ["alter", "adjust", "calibrate", "reconfigure"],
    "modifies": ["alters", "adjusts", "calibrates", "reconfigures"],
    "modified": ["altered", "adjusted", "calibrated", "reconfigured"],
    "modifying": ["altering", "adjusting", "calibrating", "reconfiguring"],

    "extend": ["broaden", "generalize", "prolong", "expand"],
    "extends": ["broadens", "generalizes", "prolongs", "expands"],
    "extended": ["broadened", "generalized", "prolonged", "expanded"],
    "extending": ["broadening", "generalizing", "prolonging", "expanding"],

    "classify": ["categorize", "stratify", "systematize", "group"],
    "classifies": ["categorizes", "stratifies", "systematizes", "groups"],
    "classified": ["categorized", "stratified", "systematized", "grouped"],
    "classifying": ["categorizing", "stratifying", "systematizing", "grouping"],

    "estimate": ["gauge", "approximate", "reckon", "assess"],
    "estimates": ["gauges", "approximates", "reckons", "assesses"],
    "estimated": ["gauged", "approximated", "reckoned", "assessed"],
    "estimating": ["gauging", "approximating", "reckoning", "assessing"],

    "synthesize": ["amalgamate", "integrate", "unify", "consolidate"],
    "synthesizes": ["amalgamates", "integrates", "unifies", "consolidates"],
    "synthesized": ["amalgamated", "integrated", "unified", "consolidated"],
    "synthesizing": ["amalgamating", "integrating", "unifying", "consolidating"],

    "corroborate": ["substantiate", "authenticate", "confirm", "endorse"],
    "corroborates": ["substantiates", "authenticates", "confirms", "endorses"],
    "corroborated": ["substantiated", "authenticated", "confirmed", "endorsed"],
    "corroborating": ["substantiating", "authenticating", "confirming", "endorsing"],

    "illustrate": ["exemplify", "demonstrate", "clarify", "depict"],
    "illustrates": ["exemplifies", "demonstrates", "clarifies", "depicts"],
    "illustrated": ["exemplified", "demonstrated", "clarified", "depicted"],
    "illustrating": ["exemplifying", "demonstrating", "clarifying", "depicting"],

    "reveal": ["disclose", "unveil", "divulge", "manifest"],
    "reveals": ["discloses", "unveils", "divulges", "manifests"],
    "revealed": ["disclosed", "unveiled", "divulged", "manifested"],
    "revealing": ["disclosing", "unveiling", "divulging", "manifesting"],

    "delineate": ["outline", "circumscribe", "trace", "define"],
    "delineates": ["outlines", "circumscribes", "traces", "defines"],
    "delineated": ["outlined", "circumscribed", "traced", "defined"],
    "delineating": ["outlining", "circumscribing", "tracing", "defining"],

    "elucidate": ["explicate", "clarify", "expound", "unravel"],
    "elucidates": ["explicates", "clarifies", "expounds", "unravels"],
    "elucidated": ["explicated", "clarified", "expounded", "unravelled"],
    "elucidating": ["explicating", "clarifying", "expounding", "unravelling"],

    "manifest": ["exhibit", "display", "evince", "betoken"],
    "manifests": ["exhibits", "displays", "evinces", "betokens"],
    "manifested": ["exhibited", "displayed", "evinced", "betokened"],
    "manifesting": ["exhibiting", "displaying", "evincing", "betokening"],

    "attenuate": ["dampen", "mitigate", "diminish", "weaken"],
    "attenuates": ["dampens", "mitigates", "diminishes", "weakens"],
    "attenuated": ["dampened", "mitigated", "diminished", "weakened"],
    "attenuating": ["dampening", "mitigating", "diminishing", "weakening"],

    "proliferate": ["multiply", "burgeon", "escalate", "propagate"],
    "proliferates": ["multiplies", "burgeons", "escalates", "propagates"],
    "proliferated": ["multiplied", "burgeoned", "escalated", "propagated"],
    "proliferating": ["multiplying", "burgeoning", "escalating", "propagating"],

    "constitute": ["comprise", "represent", "form", "embody"],
    "constitutes": ["comprises", "represents", "forms", "embodies"],
    "constituted": ["comprised", "represented", "formed", "embodied"],
    "constituting": ["comprising", "representing", "forming", "embodying"],

    "pertain": ["relate", "apply", "refer", "belong"],
    "pertains": ["relates", "applies", "refers", "belongs"],
    "pertained": ["related", "applied", "referred", "belonged"],
    "pertaining": ["relating", "applying", "referring", "belonging"],

    "engender": ["generate", "spawn", "instigate", "beget"],
    "engenders": ["generates", "spawns", "instigates", "begets"],
    "engendered": ["generated", "spawned", "instigated", "begot"],
    "engendering": ["generating", "spawning", "instigating", "begetting"],

    "underscores": ["accentuates", "highlights", "emphasizes", "stresses"],
    "underscore": ["accentuate", "highlight", "emphasize", "stress"],
    "underscored": ["accentuated", "highlighted", "emphasized", "stressed"],
    "underscoring": ["accentuating", "highlighting", "emphasizing", "stressing"]
}

for k, v in MORE_SYNS.items():
    if k not in syns:
        syns[k] = v
    else:
        for item in v:
            if item not in syns[k]:
                syns[k].append(item)

with open(syn_path, "w", encoding="utf-8") as f:
    json.dump(syns, f, indent=2, ensure_ascii=False)

print(f"Synonyms now expanded to {len(syns)} items.")

