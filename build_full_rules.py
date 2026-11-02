"""
Build comprehensive, high-quality rule databases for Turnitout Humanizer.
Expands synonyms, phrases, determiners, voice verbs, nominalizations, discourse markers,
appositives, hedge words, and protected terms following GodGuide.md and USER_MANUAL.md specs.
"""

import json
import os

RULES_DIR = r"C:\Users\gkedi\.gemini\antigravity\scratch\turnitout-humanizer\src\turnitout\rules"

# -----------------------------------------------------------------------------
# 1. SYNONYMS DATABASE (Extensive Academic Lemmatization)
# -----------------------------------------------------------------------------
NEW_SYNS = {
    # Verbs - Analysis & Methodology
    "analyze": ["scrutinize", "dissect", "interrogate", "examine", "evaluate"],
    "analyzes": ["scrutinizes", "dissects", "interrogates", "examines", "evaluates"],
    "analyzed": ["scrutinized", "dissected", "interrogated", "examined", "evaluated"],
    "analyzing": ["scrutinizing", "dissecting", "interrogating", "examining", "evaluating"],

    "investigate": ["probe", "explore", "inspect", "interrogate", "examine"],
    "investigates": ["probes", "explores", "inspects", "interrogates", "examines"],
    "investigated": ["probed", "explored", "inspected", "interrogated", "examined"],
    "investigating": ["probing", "exploring", "inspecting", "interrogating", "examining"],

    "evaluate": ["appraise", "gauge", "adjudicate", "assess", "rate"],
    "evaluates": ["appraises", "gauges", "adjudicates", "assesses", "rates"],
    "evaluated": ["appraised", "gauged", "adjudicated", "assessed", "rated"],
    "evaluating": ["appraising", "gauging", "adjudicating", "assessing", "rating"],

    "demonstrate": ["substantiate", "manifest", "illustrate", "evidence", "validate"],
    "demonstrates": ["substantiates", "manifests", "illustrates", "evidences", "validates"],
    "demonstrated": ["substantiated", "manifested", "illustrated", "evidenced", "validated"],
    "demonstrating": ["substantiating", "manifesting", "illustrating", "evidencing", "validating"],

    "show": ["illustrate", "reveal", "manifest", "display", "indicate"],
    "shows": ["illustrates", "reveals", "manifests", "displays", "indicates"],
    "showed": ["illustrated", "revealed", "manifested", "displayed", "indicated"],
    "showing": ["illustrating", "revealing", "manifesting", "displaying", "indicating"],

    "conduct": ["undertake", "execute", "perform", "effectuate", "administer"],
    "conducts": ["undertakes", "executes", "performs", "effectuates", "administers"],
    "conducted": ["undertaken", "executed", "performed", "effectuated", "administered"],
    "conducting": ["undertaking", "executing", "performing", "effectuating", "administering"],

    "examine": ["scrutinize", "audit", "inspect", "survey", "review"],
    "examines": ["scrutinizes", "audits", "inspects", "surveys", "reviews"],
    "examined": ["scrutinized", "audited", "inspected", "surveyed", "reviewed"],
    "examining": ["scrutinizing", "auditing", "inspecting", "surveying", "reviewing"],

    "determine": ["ascertain", "resolve", "establish", "deduce", "discern"],
    "determines": ["ascertains", "resolves", "establishes", "deduces", "discerns"],
    "determined": ["ascertained", "resolved", "established", "deduced", "discerned"],
    "determining": ["ascertaining", "resolving", "establishing", "deducing", "discerning"],

    "implement": ["operationalize", "instantiate", "deploy", "effectuate", "enact"],
    "implements": ["operationalizes", "instantiates", "deploys", "effectuates", "enacts"],
    "implemented": ["operationalized", "instantiated", "deployed", "effectuated", "enacted"],
    "implementing": ["operationalizing", "instantiating", "deploying", "effectuating", "enacting"],

    "optimize": ["refine", "fine-tune", "calibrate", "streamline", "hone"],
    "optimizes": ["refines", "fine-tunes", "calibrates", "streamlines", "hones"],
    "optimized": ["refined", "fine-tuned", "calibrated", "streamlined", "honed"],
    "optimizing": ["refining", "fine-tuning", "calibrating", "streamlining", "honing"],

    "enhance": ["augment", "elevate", "heighten", "bolster", "amplify"],
    "enhances": ["augments", "elevates", "heightens", "bolsters", "amplifies"],
    "enhanced": ["augmented", "elevated", "heightened", "bolstered", "amplified"],
    "enhancing": ["augmenting", "elevating", "heightening", "bolstering", "amplifying"],

    "improve": ["advance", "elevate", "refine", "upgrade", "ameliorate"],
    "improves": ["advances", "elevates", "refines", "upgrades", "ameliorates"],
    "improved": ["advanced", "elevated", "refined", "upgraded", "ameliorated"],
    "improving": ["advancing", "elevating", "refining", "upgrading", "ameliorating"],

    "indicate": ["signify", "denote", "suggest", "portend", "manifest"],
    "indicates": ["signifies", "denotes", "suggests", "portends", "manifests"],
    "indicated": ["signified", "denoted", "suggested", "portended", "manifested"],
    "indicating": ["signifying", "denoting", "suggesting", "portending", "manifesting"],

    "suggest": ["posit", "propose", "intimate", "imply", "conjecture"],
    "suggests": ["posits", "proposes", "intimates", "implies", "conjectures"],
    "suggested": ["posited", "proposed", "intimated", "implied", "conjectured"],
    "suggesting": ["positing", "proposing", "intimating", "implying", "conjecturing"],

    "provide": ["furnish", "yield", "supply", "afford", "render"],
    "provides": ["furnishes", "yields", "supplies", "affords", "renders"],
    "provided": ["furnished", "yielded", "supplied", "afforded", "rendered"],
    "providing": ["furnishing", "yielding", "supplying", "affording", "rendering"],

    "require": ["necessitate", "mandate", "call for", "demand", "compel"],
    "requires": ["necessitates", "mandates", "calls for", "demands", "compels"],
    "required": ["necessitated", "mandated", "called for", "demanded", "compelled"],
    "requiring": ["necessitating", "mandating", "calling for", "demanding", "compelling"],

    "present": ["proffer", "put forth", "articulate", "delineate", "submit"],
    "presents": ["proffers", "puts forth", "articulates", "delineates", "submits"],
    "presented": ["proffered", "put forth", "articulated", "delineated", "submitted"],
    "presenting": ["proffering", "putting forth", "articulating", "delineating", "submitting"],

    "support": ["corroborate", "bolster", "substantiate", "underpin", "uphold"],
    "supports": ["corroborates", "bolsters", "substantiates", "underpins", "upholds"],
    "supported": ["corroborated", "bolstered", "substantiated", "underpinned", "upheld"],
    "supporting": ["corroborating", "bolstering", "substantiating", "underpinning", "upholding"],

    "generate": ["produce", "spawn", "engender", "yield", "originate"],
    "generates": ["produces", "spawns", "engenders", "yields", "originates"],
    "generated": ["produced", "spawned", "engendered", "yielded", "originated"],
    "generating": ["producing", "spawning", "engendering", "yielding", "originating"],

    "identify": ["discern", "pinpoint", "recognize", "detect", "distinguish"],
    "identifies": ["discerns", "pinpoints", "recognizes", "detects", "distinguishes"],
    "identified": ["discerned", "pinpointed", "recognized", "detected", "distinguished"],
    "identifying": ["discerning", "pinpointing", "recognizing", "detecting", "distinguishing"],

    "observe": ["discern", "perceive", "note", "detect", "witness"],
    "observes": ["discerns", "perceives", "notes", "detects", "witnesses"],
    "observed": ["discerned", "perceived", "noted", "detected", "witnessed"],
    "observing": ["discerning", "perceiving", "noting", "detecting", "witnessing"],

    "transform": ["reshape", "alter", "transmute", "convert", "metamorphose"],
    "transforms": ["reshapes", "alters", "transmutes", "converts", "metamorphoses"],
    "transformed": ["reshaped", "altered", "transmuted", "converted", "metamorphosed"],
    "transforming": ["reshaping", "altering", "transmuting", "converting", "metamorphosing"],

    "address": ["tackle", "resolve", "confront", "attend to", "remedy"],
    "addresses": ["tackles", "resolves", "confronts", "attends to", "remedies"],
    "addressed": ["tackled", "resolved", "confronted", "attended to", "remedied"],
    "addressing": ["tackling", "resolving", "confronting", "attending to", "remedying"],

    "mitigate": ["alleviate", "attenuate", "abate", "moderate", "lessen"],
    "mitigates": ["alleviates", "attenuates", "abates", "moderates", "lessens"],
    "mitigated": ["alleviated", "attenuated", "abated", "moderated", "lessened"],
    "mitigating": ["alleviating", "attenuating", "abating", "moderating", "lessening"],

    "establish": ["corroborate", "institute", "formulate", "confirm", "validate"],
    "establishes": ["corroborates", "institutes", "formulates", "confirms", "validates"],
    "established": ["corroborated", "instituted", "formulated", "confirmed", "validated"],
    "establishing": ["corroborating", "instituting", "formulating", "confirming", "validating"],

    "reduce": ["curtail", "diminish", "abate", "attenuate", "decrease"],
    "reduces": ["curtails", "diminishes", "abates", "attenuates", "decreases"],
    "reduced": ["curtailed", "diminished", "abated", "attenuated", "decreased"],
    "reducing": ["curtailing", "diminishing", "abating", "attenuating", "decreasing"],

    "increase": ["escalate", "augment", "elevate", "expand", "amplify"],
    "increases": ["escalates", "augments", "elevates", "expands", "amplifies"],
    "increased": ["escalated", "augmented", "elevated", "expanded", "amplified"],
    "increasing": ["escalating", "augmenting", "elevating", "expanding", "amplifying"],

    "achieve": ["attain", "realize", "accomplish", "reach", "secure"],
    "achieves": ["attains", "realizes", "accomplishes", "reaches", "secures"],
    "achieved": ["attained", "realized", "accomplished", "reached", "secured"],
    "achieving": ["attaining", "realizing", "accomplishing", "reaching", "securing"],

    "facilitate": ["expedite", "streamline", "catalyze", "advance", "foster"],
    "facilitates": ["expedites", "streamlines", "catalyzes", "advances", "fosters"],
    "facilitated": ["expedited", "streamlined", "catalyzed", "advanced", "fostered"],
    "facilitating": ["expediting", "streamlining", "catalyzing", "advancing", "fostering"],

    "help": ["assist", "aid", "facilitate", "support", "serve to"],
    "helps": ["assists", "aids", "facilitates", "supports", "serves to"],
    "helped": ["assisted", "aided", "facilitated", "supported", "served to"],
    "helping": ["assisting", "aiding", "facilitating", "supporting", "serving to"],

    "diagnose": ["identify", "detect", "discern", "pinpoint", "characterize"],
    "diagnoses": ["identifies", "detects", "discerns", "pinpoints", "characterizes"],
    "diagnosed": ["identified", "detected", "discerned", "pinpointed", "characterized"],
    "diagnosing": ["identifying", "detecting", "discerning", "pinpointing", "characterizing"],

    "allow": ["enable", "permit", "empower", "facilitate", "license"],
    "allows": ["enables", "permits", "empowers", "facilitates", "licenses"],
    "allowed": ["enabled", "permitted", "empowered", "facilitated", "licensed"],
    "allowing": ["enabling", "permitting", "empowering", "facilitating", "licensing"],

    "ensure": ["guarantee", "assure", "verify", "secure", "confirm"],
    "ensures": ["guarantees", "assures", "verifies", "secures", "confirms"],
    "ensured": ["guaranteed", "assured", "verified", "secured", "confirmed"],
    "ensuring": ["guaranteeing", "assuring", "verifying", "securing", "confirming"],

    "maintain": ["sustain", "preserve", "uphold", "retain", "perpetuate"],
    "maintains": ["sustains", "preserves", "upholds", "retains", "perpetuates"],
    "maintained": ["sustained", "preserved", "upheld", "retained", "perpetuated"],
    "maintaining": ["sustaining", "preserving", "upholding", "retaining", "perpetuating"],

    "clarify": ["elucidate", "illuminate", "explicate", "demystify", "articulate"],
    "clarifies": ["elucidates", "illuminates", "explicates", "demystifies", "articulates"],
    "clarified": ["elucidated", "illuminated", "explicated", "demystified", "articulated"],
    "clarifying": ["elucidating", "illuminating", "explicating", "demystifying", "articulating"],

    "highlight": ["accentuate", "underscore", "emphasize", "foreground", "spotlight"],
    "highlights": ["accentuates", "underscores", "emphasizes", "foregrounds", "spotlights"],
    "highlighted": ["accentuated", "underscored", "emphasized", "foregrounded", "spotlighted"],
    "highlighting": ["accentuating", "underscoring", "emphasizing", "foregrounding", "spotlighting"],

    "promote": ["foster", "advance", "cultivate", "stimulate", "further"],
    "promotes": ["fosters", "advances", "cultivates", "stimulates", "furthers"],
    "promoted": ["fostered", "advanced", "cultivated", "stimulated", "furthered"],
    "promoting": ["fostering", "advancing", "cultivating", "stimulating", "furthering"],

    "explore": ["scrutinize", "probe", "investigate", "survey", "delve into"],
    "explores": ["scrutinizes", "probes", "investigates", "surveys", "delves into"],
    "explored": ["scrutinized", "probed", "investigated", "surveyed", "delved into"],
    "exploring": ["scrutinizing", "probing", "investigating", "surveying", "delving into"],

    # Nouns - Technical & Scholarly
    "approach": ["methodology", "protocol", "modality", "paradigm", "stratagem"],
    "approaches": ["methodologies", "protocols", "modalities", "paradigms", "stratagems"],
    "method": ["procedure", "protocol", "technique", "regimen", "modality"],
    "methods": ["procedures", "protocols", "techniques", "regimens", "modalities"],
    "result": ["finding", "outcome", "observation", "deduction", "yield"],
    "results": ["findings", "outcomes", "observations", "deductions", "yields"],
    "framework": ["architecture", "schema", "conceptual model", "infrastructure", "construct"],
    "frameworks": ["architectures", "schemas", "conceptual models", "infrastructures", "constructs"],
    "data": ["empirical records", "observations", "measurements", "evidence", "findings"],
    "problem": ["quandary", "predicament", "conundrum", "challenge", "obstacle"],
    "problems": ["quandaries", "predicaments", "conundrums", "challenges", "obstacles"],
    "technology": ["apparatus", "architecture", "computational tool", "instrumentation", "system"],
    "technologies": ["apparatuses", "architectures", "computational tools", "instrumentations", "systems"],
    "solution": ["resolution", "remedy", "countermeasure", "rectification", "answer"],
    "solutions": ["resolutions", "remedies", "countermeasures", "rectifications", "answers"],
    "impact": ["consequence", "influence", "repercussion", "ramification", "bearing"],
    "impacts": ["consequences", "influences", "repercussions", "ramifications", "bearings"],
    "factor": ["determinant", "constituent", "element", "component", "variable"],
    "factors": ["determinants", "constituents", "elements", "components", "variables"],
    "society": ["community", "public sphere", "populace", "civilization", "social order"],
    "societies": ["communities", "public spheres", "populaces", "civilizations", "social orders"],
    "opportunity": ["prospect", "avenue", "potentiality", "pathway", "occasion"],
    "opportunities": ["prospects", "avenues", "potentialities", "pathways", "occasions"],
    "challenge": ["impediment", "obstacle", "hurdle", "difficulty", "complication"],
    "challenges": ["impediments", "obstacles", "hurdles", "difficulties", "complications"],
    "regulation": ["governance", "oversight", "standard", "statutory rule", "guideline"],
    "regulations": ["governance", "oversight", "standards", "statutory rules", "guidelines"],
    "concept": ["notion", "theoretical construct", "abstraction", "conceptualization", "formulation"],
    "concepts": ["notions", "theoretical constructs", "abstractions", "conceptualizations", "formulations"],
    "system": ["framework", "architecture", "apparatus", "mechanism", "structure"],
    "systems": ["frameworks", "architectures", "apparatuses", "mechanisms", "structures"],
    "model": ["paradigm", "schema", "computational representation", "archetype", "formulation"],
    "models": ["paradigms", "schemas", "computational representations", "archetypes", "formulations"],
    "study": ["investigation", "inquiry", "scholarly examination", "research", "paper"],
    "studies": ["investigations", "inquiries", "scholarly examinations", "researches", "papers"],
    "paper": ["manuscript", "treatise", "dissertation", "monograph", "contribution"],
    "papers": ["manuscripts", "treatises", "dissertations", "monographs", "contributions"],
    "research": ["scholarship", "inquiry", "investigation", "empirical study", "exploration"],
    "researcher": ["investigator", "scholar", "academic", "practitioner", "analyst"],
    "researchers": ["investigators", "scholars", "academics", "practitioners", "analysts"],
    "doctor": ["clinician", "physician", "medical practitioner", "specialist"],
    "doctors": ["clinicians", "physicians", "medical practitioners", "specialists"],
    "disease": ["pathology", "morbid condition", "clinical disorder", "ailment"],
    "diseases": ["pathologies", "morbid conditions", "clinical disorders", "ailments"],
    "amount": ["magnitude", "volume", "quantity", "extent", "measure"],
    "amounts": ["magnitudes", "volumes", "quantities", "extents", "measures"],
    "risk": ["hazard", "peril", "vulnerability", "contingency", "jeopardy"],
    "risks": ["hazards", "perils", "vulnerabilities", "contingencies", "jeopardies"],

    # Adjectives - Academic & Descriptive
    "significant": ["substantial", "consequential", "pronounced", "appreciable", "salient"],
    "substantially": ["appreciably", "considerably", "measurably", "noticeably", "markedly"],
    "important": ["essential", "pivotal", "consequential", "paramount", "critical"],
    "crucial": ["indispensable", "vital", "pivotal", "decisive", "foundational"],
    "accurate": ["veridical", "precise", "exact", "scrupulous", "faithful"],
    "accurately": ["veridically", "precisely", "scrupulously", "rigorously", "faithfully"],
    "complex": ["intricate", "multifaceted", "elaborate", "non-trivial", "involved"],
    "complexity": ["intricacy", "elaboration", "sophistication", "multiplicity"],
    "rapid": ["swift", "expeditious", "accelerated", "prompt", "speedy"],
    "rapidly": ["swiftly", "expeditiously", "at an accelerated pace", "briskly"],
    "modern": ["contemporary", "current", "present-day", "state-of-the-art"],
    "massive": ["immense", "voluminous", "extensive", "copious", "substantial"],
    "medical": ["clinical", "biomedical", "therapeutic", "healthcare-related"],
    "ethical": ["moral", "normative", "principled", "conscientious"],
    "ethically": ["morally", "normatively", "conscientiously"],
    "transparent": ["intelligible", "lucid", "accountable", "unambiguous", "auditable"],
    "fair": ["equitable", "impartial", "unbiased", "even-handed", "neutral"],
    "fairness": ["equity", "impartiality", "even-handedness", "unbiasedness"],
    "careful": ["meticulous", "scrupulous", "rigorous", "thorough", "exacting"],
    "carefully": ["meticulously", "scrupulously", "rigorously", "thoroughly"],
    "clear": ["evident", "lucid", "manifest", "conspicuous", "discernible"],
    "clearly": ["manifestly", "evidently", "discernibly", "unambiguously"],
    "robust": ["sound", "resilient", "sturdy", "rigorous", "well-founded"],
    "novel": ["innovative", "groundbreaking", "unconventional", "pioneering"],
    "comprehensive": ["exhaustive", "broad-ranging", "encyclopedic", "all-inclusive"],
    "effective": ["efficacious", "potent", "productive", "advantageous"],
    "effectively": ["efficaciously", "potently", "productively"],
    "subsequent": ["ensuing", "succeeding", "consecutive", "following"],
    "subsequently": ["thereafter", "ensuingly", "in the sequel", "following this"],
    "subtle": ["nuanced", "delicate", "fine-grained", "understated"],
    "diverse": ["heterogeneous", "multifarious", "variegated", "disparate"],
    "fundamental": ["foundational", "elemental", "cardinal", "basal"],
    "fundamentally": ["at its core", "essentially", "in principle", "radically"],
    "prominent": ["salient", "conspicuous", "notable", "foremost"],
    "rigorous": ["exacting", "scrupulous", "uncompromising", "stringent"],
    "rigorously": ["scrupulously", "stringently", "meticulously"],
    "vast": ["immense", "extensive", "copious", "broad"],
    "immense": ["colossal", "stupendous", "prodigious", "tremendous"],
    "evident": ["apparent", "manifest", "patent", "undisguised"],
    "obvious": ["conspicuous", "self-evident", "manifest", "patent"]
}

# -----------------------------------------------------------------------------
# 2. PHRASES DATABASE (Multi-Word AI Signature Scrubbers & Academic Rewrites)
# -----------------------------------------------------------------------------
NEW_PHRASES = [
    # Top AI cliché tells
    [r"\bdelve into\b", "scrutinize"],
    [r"\bdelves into\b", "scrutinizes"],
    [r"\bdelving into\b", "scrutinizing"],
    [r"\bdelve deep into\b", "rigorously examine"],
    [r"\bit is important to delve into\b", "we examine"],
    [r"\bin conclusion, it is important to\b", "to conclude, one must"],
    [r"\bin conclusion\b", "in summary"],
    [r"\bto wrap up\b", "in summary"],
    [r"\bcomprehensive tapestry of\b", "complex fabric of"],
    [r"\brich tapestry of\b", "diverse spectrum of"],
    [r"\btapestry of\b", "intricate mosaic of"],
    [r"\bplays a pivotal role in illustrating\b", "clearly demonstrates"],
    [r"\bplays a pivotal role in\b", "is central to"],
    [r"\bplays a pivotal role\b", "is essential"],
    [r"\bplays a crucial role in\b", "is instrumental in"],
    [r"\bplays a crucial role\b", "is of critical significance"],
    [r"\bplays a key role in\b", "acts as a primary driver of"],
    [r"\bstands as a testament to\b", "reflects"],
    [r"\bserves as a testament to\b", "attests to"],
    [r"\ba testament to\b", "compelling evidence of"],
    [r"\bfurthermore, the interplay between\b", "moreover, the coordination of"],
    [r"\bthe interplay between\b", "the dynamic interaction of"],
    [r"\binterplay between\b", "interaction between"],
    [r"\bprovides a robust framework\b", "furnishes a sound theoretical foundation"],
    [r"\brobust framework\b", "resilient architectural framework"],
    [r"\bmultifaceted dimensions of\b", "diverse aspects of"],
    [r"\bmultifaceted nature of\b", "intricate character of"],
    [r"\bmultifaceted\b", "intricate"],
    [r"\bparadigm shift\b", "fundamental conceptual transition"],
    [r"\bcritical milestone\b", "significant inflection point"],
    [r"\bparamount importance\b", "vital significance"],
    [r"\bof paramount importance\b", "of central importance"],
    [r"\bmoreover, in today's fast-paced digital era\b", "furthermore, in contemporary technological settings"],
    [r"\bin today's fast-paced digital era\b", "in contemporary digital environments"],
    [r"\bin today's digital era\b", "in modern technological contexts"],
    [r"\bin today's digital age\b", "in contemporary settings"],
    [r"\bin today's fast-paced world\b", "in dynamic contemporary environments"],
    [r"\bin today's world\b", "presently"],
    [r"\bfast-paced digital era\b", "rapidly evolving digital ecosystem"],
    [r"\bfast-paced world\b", "rapidly evolving environment"],
    [r"\bcannot be overlooked\b", "warrants rigorous consideration"],
    [r"\bit cannot be denied that\b", "unquestionably,"],
    [r"\bdelve deep into the multifaceted dimensions of\b", "conduct a detailed examination of"],
    [r"\bultimately, this paradigm shift\b", "in the final analysis, this systemic transformation"],
    [r"\bit is important to note that\b", "observe that"],
    [r"\bit is worth noting that\b", "notably,"],
    [r"\bit should be noted that\b", "significantly,"],
    [r"\bit is essential to remember that\b", "one must bear in mind that"],
    [r"\bit is interesting to observe that\b", "remarkably,"],
    [r"\bdue to the fact that\b", "because"],
    [r"\bon account of the fact that\b", "inasmuch as"],
    [r"\bin light of the fact that\b", "given that"],
    [r"\bin order to\b", "to"],
    [r"\bwith a view to\b", "in an effort to"],
    [r"\bwith the aim of\b", "aiming to"],
    [r"\bfor the purpose of\b", "intended for"],
    [r"\ba wide range of\b", "an extensive spectrum of"],
    [r"\ba wide variety of\b", "a broad assortment of"],
    [r"\ba large number of\b", "a multitude of"],
    [r"\ba significant amount of\b", "a substantial volume of"],
    [r"\bprevious studies have shown\b", "prior scholarly investigations have documented"],
    [r"\bearlier research suggests\b", "prior literature indicates"],
    [r"\bhas been widely studied\b", "has received exhaustive scholarly attention"],
    [r"\bit has been reported that\b", "extant literature attests that"],
    [r"\bas shown in\b", "as delineated in"],
    [r"\bas depicted in\b", "as illustrated in"],
    [r"\bthe results indicate\b", "the empirical findings reveal"],
    [r"\bthe data shows that\b", "the records corroborate that"],
    [r"\bit can be seen that\b", "it is apparent that"],
    [r"\bit is evident that\b", "it becomes manifest that"],
    [r"\bat the forefront of\b", "leading the vanguard in"],
    [r"\bbeacon of hope\b", "promising catalyst"],
    [r"\bnavigating the complexities of\b", "negotiating the intricacies of"],
    [r"\bnavigating the landscape of\b", "surveying the domain of"],
    [r"\bever-evolving landscape of\b", "dynamic operational terrain of"],
    [r"\bever-changing landscape\b", "shifting milieu"],
    [r"\btake into consideration\b", "give due consideration to"],
    [r"\btakes into consideration\b", "gives due consideration to"],
    [r"\btaken into consideration\b", "given due consideration"],
    [r"\btaking into consideration\b", "giving due consideration to"],
    [r"\btake into account\b", "account for"],
    [r"\btakes into account\b", "accounts for"],
    [r"\bin the realm of\b", "within the scope of"],
    [r"\bin the domain of\b", "in the discipline of"],
    [r"\ba plethora of\b", "a profusion of"],
    [r"\bserves to highlight\b", "accentuates"],
    [r"\bserves as a\b", "functions as a"],
    [r"\bshed light on\b", "illuminate"],
    [r"\bsheds light on\b", "illuminates"],
    [r"\bis characterized by\b", "is distinguished by"],
    [r"\bon the other hand\b", "conversely"],
    [r"\bwith respect to\b", "vis-à-vis"],
    [r"\bin terms of\b", "with regard to"],
    [r"\bplays an indispensable part\b", "occupies a foundational role"],
    [r"\bit goes without saying that\b", "self-evidently,"],
    [r"\ba cornerstone of\b", "a foundational tenet of"],
    [r"\bin summary,\b", "in essence,"],
    [r"\bto sum up,\b", "to encapsulate,"],
    [r"\bfurther research is needed\b", "subsequent empirical inquiry is warranted"],
    [r"\bfuture work should\b", "prospective scholarship ought to"],
    [r"\bin the near future\b", "prospectively"],
    [r"\bhas a profound impact on\b", "substantially alters"],
    [r"\bhas a significant effect on\b", "markedly influences"],
    [r"\ba double-edged sword\b", "a bifurcated challenge"],
    [r"\bit remains to be seen whether\b", "it is yet uncertain if"],
    [r"\bgives rise to\b", "engenders"],
    [r"\bis in good agreement with\b", "accords closely with"],
    [r"\bis consistent with\b", "harmonizes with"],
    [r"\bdraws attention to\b", "foregrounds"],
    [r"\bin this day and age\b", "contemporarily"],
    [r"\ball things considered\b", "upon comprehensive evaluation"],
    [r"\bat first glance\b", "prima facie"],
    [r"\bby leaps and bounds\b", "exponentially"],
    [r"\blies at the heart of\b", "constitutes the crux of"],
    [r"\bpaves the way for\b", "facilitates the emergence of"],
    [r"\bsets the stage for\b", "preconditions the groundwork for"]
]

# -----------------------------------------------------------------------------
# 3. DETERMINERS DATABASE (Syntax-Aware Article & Quantifier Variations)
# -----------------------------------------------------------------------------
NEW_DETS = {
    "the": ["this", "such", "the respective", "the given", "that"],
    "this": ["the", "the present", "this particular", "said", "such"],
    "these": ["such", "the prevailing", "the noted", "the aforementioned"],
    "those": ["such", "the observed", "the specific"],
    "a": ["an individual", "a given", "a singular", "a particular"],
    "an": ["a single", "a particular", "a given"],
    "some": ["certain", "particular", "select", "sundry", "a subset of"],
    "many": ["numerous", "a considerable number of", "myriad", "copious", "diverse"],
    "several": ["numerous", "multiple", "a plurality of", "sundry"],
    "few": ["a limited number of", "a scant handful of", "sparse"],
    "most": ["the majority of", "the preponderance of", "the bulk of"],
    "all": ["every", "the totality of", "each of the", "the entirety of"],
    "each": ["every", "any given", "each respective"],
    "every": ["each", "any given", "all individual"],
    "both": ["the two", "simultaneously the", "the pair of"],
    "any": ["whichever", "any given", "an arbitrary"],
    "another": ["a further", "an additional", "a supplementary"],
    "such": ["said", "the specified", "the aforementioned"],
    "other": ["alternative", "additional", "further", "distinct"]
}

# -----------------------------------------------------------------------------
# 4. VOICE VERBS (Transitive Academic Verbs for Voice Inversion)
# -----------------------------------------------------------------------------
NEW_VOICE_VERBS = {
    "analyze": {"past": "analyzed", "passive": "was analyzed", "passive_plural": "were analyzed"},
    "apply": {"past": "applied", "passive": "was applied", "passive_plural": "were applied"},
    "evaluate": {"past": "evaluated", "passive": "was evaluated", "passive_plural": "were evaluated"},
    "investigate": {"past": "investigated", "passive": "was investigated", "passive_plural": "were investigated"},
    "conduct": {"past": "conducted", "passive": "was conducted", "passive_plural": "were conducted"},
    "perform": {"past": "performed", "passive": "was performed", "passive_plural": "were performed"},
    "demonstrate": {"past": "demonstrated", "passive": "was demonstrated", "passive_plural": "were demonstrated"},
    "calculate": {"past": "calculated", "passive": "was calculated", "passive_plural": "were calculated"},
    "measure": {"past": "measured", "passive": "was measured", "passive_plural": "were measured"},
    "observe": {"past": "observed", "passive": "was observed", "passive_plural": "were observed"},
    "derive": {"past": "derived", "passive": "was derived", "passive_plural": "were derived"},
    "formulate": {"past": "formulated", "passive": "was formulated", "passive_plural": "were formulated"},
    "implement": {"past": "implemented", "passive": "was implemented", "passive_plural": "were implemented"},
    "optimize": {"past": "optimized", "passive": "was optimized", "passive_plural": "were optimized"},
    "validate": {"past": "validated", "passive": "was validated", "passive_plural": "were validated"},
    "verify": {"past": "verified", "passive": "was verified", "passive_plural": "were verified"},
    "examine": {"past": "examined", "passive": "was examined", "passive_plural": "were examined"},
    "identify": {"past": "identified", "passive": "was identified", "passive_plural": "were identified"},
    "determine": {"past": "determined", "passive": "was determined", "passive_plural": "were determined"},
    "collect": {"past": "collected", "passive": "was collected", "passive_plural": "were collected"},
    "process": {"past": "processed", "passive": "was processed", "passive_plural": "were processed"},
    "simulate": {"past": "simulated", "passive": "was simulated", "passive_plural": "were simulated"},
    "synthesize": {"past": "synthesized", "passive": "was synthesized", "passive_plural": "were synthesized"},
    "engineer": {"past": "engineered", "passive": "was engineered", "passive_plural": "were engineered"},
    "construct": {"past": "constructed", "passive": "was constructed", "passive_plural": "were constructed"},
    "deploy": {"past": "deployed", "passive": "was deployed", "passive_plural": "were deployed"},
    "train": {"past": "trained", "passive": "was trained", "passive_plural": "were trained"},
    "test": {"past": "tested", "passive": "was tested", "passive_plural": "were tested"},
    "establish": {"past": "established", "passive": "was established", "passive_plural": "were established"},
    "scrutinize": {"past": "scrutinized", "passive": "was scrutinized", "passive_plural": "were scrutinized"}
}

# -----------------------------------------------------------------------------
# 5. NOMINALIZATIONS (Verb <-> Noun Structural Transformations)
# -----------------------------------------------------------------------------
NEW_NOMINALIZATIONS = {
    "analyze": "analysis",
    "investigate": "investigation",
    "apply": "application",
    "develop": "development",
    "improve": "improvement",
    "evaluate": "evaluation",
    "derive": "derivation",
    "compute": "computation",
    "simulate": "simulation",
    "approximate": "approximation",
    "converge": "convergence",
    "vary": "variation",
    "solve": "solution",
    "implement": "implementation",
    "formulate": "formulation",
    "transform": "transformation",
    "integrate": "integration",
    "differentiate": "differentiation",
    "observe": "observation",
    "measure": "measurement",
    "determine": "determination",
    "classify": "classification",
    "optimize": "optimization",
    "validate": "validation",
    "demonstrate": "demonstration",
    "establish": "establishment",
    "reduce": "reduction",
    "extend": "extension",
    "modify": "modification",
    "construct": "construction",
    "assess": "assessment",
    "estimate": "estimation",
    "generate": "generation",
    "interpret": "interpretation",
    "quantify": "quantification"
}

# -----------------------------------------------------------------------------
# 6. DISCOURSE MARKERS (Anti-Repetition Rotational Taxonomy)
# -----------------------------------------------------------------------------
NEW_DISCOURSE = {
    "However": ["Nevertheless", "Nonetheless", "On the other hand", "That said", "Be that as it may", "Conversely"],
    "Therefore": ["Consequently", "Hence", "As a result", "It follows that", "Accordingly", "Ergo"],
    "Moreover": ["Furthermore", "In addition", "Additionally", "What is more", "Beyond this", "Coupled with this"],
    "Furthermore": ["In addition", "Moreover", "Additionally", "Equally important", "Also of note"],
    "Although": ["Even though", "Despite the fact that", "Notwithstanding", "While it is true that", "Granted that"],
    "Thus": ["Hence", "Accordingly", "As such", "In this manner", "By this means", "In consequence"],
    "Indeed": ["In fact", "Certainly", "As a matter of fact", "To be sure", "Without question"],
    "Similarly": ["Likewise", "In a similar manner", "Comparably", "By the same token", "Along these lines"],
    "Specifically": ["In particular", "More precisely", "To be specific", "Namely", "That is to say"],
    "Notably": ["Remarkably", "Significantly", "Importantly", "Strikingly", "Conspicuously"],
    "Meanwhile": ["In the interim", "Concurrently", "At the same time", "Simultaneously", "During this period"],
    "Conversely": ["On the contrary", "In contrast", "By contrast", "Contrastingly", "On the other hand"],
    "Ultimately": ["In the final analysis", "At length", "When all is considered", "In the last analysis"],
    "Evidently": ["Apparently", "As it turns out", "It appears that", "Seemingly", "Ostensibly"],
    "Essentially": ["Fundamentally", "At its core", "In essence", "Basically", "At the heart of it"],
    "Typically": ["Generally", "Ordinarily", "As a rule", "In most cases", "Under normal circumstances"],
    "In addition": ["Furthermore", "Moreover", "Additionally", "Along with this", "Complementary to this"],
    "Consequently": ["As a consequence", "Therefore", "Resultantly", "Accordingly"],
    "In contrast": ["Conversely", "On the other hand", "Distinctively", "By comparison"]
}

# -----------------------------------------------------------------------------
# 7. APPOSITIVES (Definitional Clarifying Injections)
# -----------------------------------------------------------------------------
NEW_APPOSITIVES = {
    "finite difference": "a discretization technique for differential equations",
    "Crank-Nicolson": "an implicit second-order-accurate numerical scheme",
    "boundary condition": "a constraint imposed on the solution domain boundaries",
    "convergence": "the tendency of a numerical sequence toward an exact limiting value",
    "stability": "the property ensuring bounded error propagation across time steps",
    "truncation error": "the discrepancy between differential and algebraic operators",
    "eigenvalue": "a characteristic scalar multiplier of a linear operator",
    "discretization": "the process of converting continuous models into discrete domains",
    "initial condition": "the prescribed state at the initial temporal coordinate",
    "explicit method": "a scheme computing future states directly from known values",
    "implicit method": "a scheme requiring the simultaneous inversion of coupled equations",
    "differential equation": "a mathematical relation involving derivatives of unknown functions",
    "partial derivative": "a derivative with respect to one coordinate while holding others constant",
    "numerical method": "a computational algorithm for obtaining approximate quantitative solutions",
    "iterative process": "a recurring sequence of operations converging toward an attractor",
    "linear system": "a collection of linear algebraic equations over a vector space",
    "approximation": "an expression numerically adjacent to the exact analytical quantity",
    "error analysis": "the systematic study and bounding of computational inaccuracies",
    "time step": "the discrete temporal increment within an evolution scheme",
    "grid spacing": "the spatial interval between adjacent computational nodes",
    "wave equation": "a hyperbolic partial differential equation governing oscillatory propagation",
    "heat equation": "a parabolic partial differential equation characterizing thermal diffusion",
    "Laplace equation": "an elliptic partial differential equation describing harmonic steady states",
    "Black-Scholes": "a seminal continuous-time financial valuation model",
    "stochastic process": "a collection of random variables indexed by continuous or discrete time",
    "Monte Carlo": "a broad class of computational algorithms that rely on repeated random sampling",
    "neural network": "a layered computational graph of parameterized matrix transformations",
    "transformer": "an attention-based deep neural network architecture",
    "BERT": "a bidirectional transformer-based language representation model",
    "gradient descent": "a first-order iterative optimization algorithm for finding local minima",
    "loss function": "a mathematical function evaluating the discrepancy between predictions and ground truth"
}

# -----------------------------------------------------------------------------
# 8. HEDGE WORDS (Epistemic Noise & Perplexity Injectors)
# -----------------------------------------------------------------------------
NEW_HEDGES = [
    "arguably", "plausibly", "ostensibly", "conceivably", "purportedly",
    "putatively", "presumably", "tentatively", "provisionally", "speculatively",
    "conjecturally", "hypothetically", "admittedly", "indisputably", "undeniably",
    "incontrovertibly", "unquestionably", "demonstrably", "appreciably", "discernibly",
    "measurably", "tangibly", "palpably", "manifestly", "conspicuously",
    "strikingly", "decidedly", "markedly", "emphatically", "unambiguously",
    "categorically", "definitively", "conclusively", "incontestably", "assuredly",
    "certifiably", "verifiably", "observably", "detectably", "notably",
    "predominantly", "substantially", "characteristically", "fundamentally", "primarily"
]

# -----------------------------------------------------------------------------
# 9. PROTECTED TERMS (Zero-Modification Mathematical & Scientific Whitelist)
# -----------------------------------------------------------------------------
NEW_PROTECTED = [
    "Navier-Stokes", "Navier--Stokes", "Boltzmann", "Maxwell", "Helmholtz",
    "Schrödinger", "Schrodinger", "Heisenberg", "Bernoulli", "Lagrange",
    "Lagrangian", "Hamiltonian", "Jacobian", "Hessian", "Wronskian",
    "Green's function", "Green's theorem", "Stokes' theorem", "Gauss's theorem",
    "Cauchy", "Riemann", "Hilbert", "Banach", "Sobolev", "Lebesgue",
    "Monte Carlo", "Gaussian", "Bayesian", "Boolean", "Euclidean",
    "Cartesian", "Fibonacci", "Hermitian", "Abelian", "Kolmogorov",
    "Lyapunov", "Reynolds number", "Mach number", "Prandtl number", "Nusselt number",
    "TensorFlow", "PyTorch", "COMSOL", "ANSYS", "OpenFOAM", "MATLAB", "Simulink",
    "CRISPR-Cas9", "CRISPR", "Cas9", "AdamW", "ResNet", "ImageNet", "SQuAD",
    "BLEU", "ROUGE", "GLUE", "SuperGLUE", "Transformer", "BERT", "GPT",
    "O(N)", "O(N log N)", "O(1)", "O(N^2)", "O(2^N)", "NP-hard", "NP-complete",
    "k-nearest", "k-means", "Markov chain", "Dirichlet", "Poisson", "Laplace",
    "Runge-Kutta", "Newton-Raphson", "Crank-Nicolson", "Fourier", "Taylor series"
]

def update_json(filename, new_data):
    filepath = os.path.join(RULES_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        existing = json.load(f)

    if isinstance(existing, dict):
        # Preserve prompt if any
        prompt = existing.get("__prompt__")
        # Merge
        merged = dict(existing)
        for k, v in new_data.items():
            if k not in merged:
                merged[k] = v
            elif isinstance(v, list) and isinstance(merged[k], list):
                # Union of lists preserving order
                for item in v:
                    if item not in merged[k]:
                        merged[k].append(item)
            elif isinstance(v, dict) and isinstance(merged[k], dict):
                merged[k].update(v)
            else:
                merged[k] = v
        if prompt and "__prompt__" not in merged:
            merged["__prompt__"] = prompt
        out_data = merged

    elif isinstance(existing, list):
        prompt = existing[0] if existing and isinstance(existing[0], dict) and "__prompt__" in existing[0] else None
        merged = []
        if prompt:
            merged.append(prompt)
            existing = existing[1:]

        seen_keys = set()
        for item in existing:
            if isinstance(item, list) and len(item) == 2:
                seen_keys.add(item[0].lower())
                merged.append(item)
            elif isinstance(item, str):
                seen_keys.add(item.lower())
                merged.append(item)

        for item in new_data:
            if isinstance(item, list) and len(item) == 2:
                if item[0].lower() not in seen_keys:
                    merged.append(item)
                    seen_keys.add(item[0].lower())
            elif isinstance(item, str):
                if item.lower() not in seen_keys:
                    merged.append(item)
                    seen_keys.add(item.lower())

        out_data = merged

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(out_data, f, indent=2, ensure_ascii=False)
    print(f"Updated {filename}: {len(out_data)} elements")

if __name__ == "__main__":
    update_json("synonyms.json", NEW_SYNS)
    update_json("phrases.json", NEW_PHRASES)
    update_json("determiners.json", NEW_DETS)
    update_json("voice_verbs.json", NEW_VOICE_VERBS)
    update_json("nominalizations.json", NEW_NOMINALIZATIONS)
    update_json("discourse_markers.json", NEW_DISCOURSE)
    update_json("appositives.json", NEW_APPOSITIVES)
    update_json("hedge_words.json", NEW_HEDGES)
    update_json("protected_terms.json", NEW_PROTECTED)
    print("All rule databases successfully expanded.")

