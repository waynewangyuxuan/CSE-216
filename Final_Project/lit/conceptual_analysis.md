# What "conceptual analysis" most likely means

**Status: unconfirmed.** The professor's words were recorded only as a suggestion to read on "conceptual analysis". Nothing below establishes which meaning they had in mind.

## Question to send

> When you suggested reading on "conceptual analysis", did you mean a specific method such as Jabareen's conceptual framework analysis, an HCI concept critique like Hornbæk and Oulasvirta's "What Is Interaction?", or something else, so I can apply the right one to separating offloading from surrender?

## Short answer

"Conceptual analysis" is not one method. I found four distinct uses. My best guess, given what the professor asked in the same meeting ("how can offloading be judged in a given scene?"), is a request to **pin down what the concept means and how to tell its boundary cases**, rather than a request to run a formal multi-phase procedure. That is an inference from context, not evidence of what they meant.

| Meaning | Core move | Source and how it was read | Fit to the professor's question |
|---|---|---|---|
| Philosophical conceptual analysis | Break a concept into simpler parts, often as conditions for correct application. Necessary-and-sufficient conditions are no longer treated as the only aim. | Beaney & Raysmith, "Analysis", Stanford Encyclopedia of Philosophy, revised 2024. Summary of the entry, not a close reading. | Good in spirit, no procedure |
| Concept analysis (nursing and health tradition) | Defining attributes, antecedents, consequences, empirical referents, and model, borderline and contrary cases. | Gunawan, Aungsuroch & Marzilli 2023, doi:10.33546/bnj.2544, an editorial surveying eight methods including Walker & Avant and Rodgers 1989. **Second-hand**: I did not read Walker & Avant or Rodgers. | **Best fit**: boundary cases answer "how do you judge a scene" |
| Conceptual framework analysis | An eight-phase, grounded-theory method for building a framework from multidisciplinary texts. | Jabareen 2009. **Full text read.** | Partial; see below |
| HCI concept critique | Extract the competing concepts in a field and compare their scope and causal assumptions. | Hornbæk & Oulasvirta 2017. **Abstract only.** Related, unread: Oulasvirta & Hornbæk 2016 (doi:10.1145/2858036.2858283) and Hornbæk et al. 2019 (doi:10.1145/3325285). Ajmani et al. 2026 (arXiv:2607.12092), abstract only, propose thought experiments for HCI conceptual work. | Good fit for the framework comparison |

## Jabareen 2009: should it shape the framework?

**Recommendation: use two pieces, and do not claim to have followed the method.**

The eight phases (journal pp. 53–55): map data sources; read and categorize; identify and name concepts; deconstruct and categorize them; integrate; synthesize; validate; rethink.

Reasons not to adopt the whole method:

1. **It cannot be claimed after the fact.** The codebook already exists and its labels were not derived by these phases. Saying they were would misdescribe how it was built.
2. **Phase 1 recommends interviews** with practitioners and scholars (p. 53). The proposal promises no interviews. The review of texts alone could be done, but that is a departure to report.
3. **Direction of work.** Jabareen wants concepts to emerge from the literature and quotes a warning (Morse, Hupcey et al., via Jabareen p. 54) about starting from a concept rather than the phenomenon. This project starts from two named concepts, offloading and surrender.
4. **Different goal.** Jabareen describes a conceptual framework as interpretive, not causal or determinist (p. 57), and warns that different researchers may produce different frameworks (p. 58). The project's success criterion asks for labels applied with acceptable agreement, which is a coding goal.

Pieces worth borrowing, cheaply:

- **Phase 4's table** (concept, description, ontological/epistemological/methodological role, references; p. 54). A one-page version would force each codebook field to state whether it claims something about behavior, about what can be known from logs, or about method. That is exactly where offloading and surrender slip between behavior and cognition.
- **Phase 7's outside check** (p. 54): show the framework to people outside the project. The professor meetings on Nov 19 and 24 already fit this.

## Hornbæk & Oulasvirta 2017: should it shape the framework?

**Recommendation: use it as a checklist for the comparison, after reading it.** I could not read the full text. The ACM page showed a bot check, which I did not attempt to pass, and the Aalto repository copy returned HTTP 403.

From the abstract alone: the authors extract distinct concepts of interaction from the literature (dialogue, transmission, optimal behavior, embodiment, tool use), argue they differ in scope and in how they construe causal relations between human and computer, and ask for better scope, specificity and stronger propositions.

That gives three questions to put to each framework, and `framework_comparison.md` uses them:

- What is its scope?
- What causal relation between person and AI does it assume?
- What strong, testable proposition does it make?

It is an essay, not a procedure, so it cannot supply steps. **Anything more specific than this needs the full text**, so the user should get it through the university library before citing it in Milestone 2.

## What this means for the project

The most useful thing to borrow is not on the professor's candidate list: the concept-analysis habit of writing down **model, borderline and contrary cases**, with **empirical referents** for each attribute.

- It answers the professor's second question directly: a scene is judged by which observable referents are present, and borderline cases are stated as borderline.
- It matches the proposal's limit that the framework codes behavior, not cognition.
- `framework_comparison.md` already works this way.

A caveat: I know this method only second-hand, so read Walker & Avant or Rodgers 1989 (doi:10.1111/j.1365-2648.1989.tb03420.x) before citing it as the method used. Podsakoff, MacKenzie & Podsakoff 2016 (doi:10.1177/1094428115624965) is a likely social-science route to the same goal; I confirmed only that the record exists and did not read it.
