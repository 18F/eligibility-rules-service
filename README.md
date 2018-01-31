# Eligibility rules service

18F is conducting research to identify opportunities for developing a web-based eligibility rules service that could be used to help states make eligibility determinations for a human services program.

> Presentation: **[Exploring an Eligibility Rules Service](https://github.com/18F/eligibility-rules-service/files/1643282/eligibility-rules-service-explanation.pdf)**

#### The problem

Many states struggle to modernize their human services eligibility and enrollment systems due to the variation and complexity of the policy rules that determine eligibility for federally funded programs, as well as outdated, monolithic procurement and development practices, limited reusable components, and scarce resources. These efforts lead to duplicative work and expense across states without delivering better service.

#### Our hypothesis

Both federal and state agencies could achieve greater program efficiencies if the administering federal agency offered a configurable, API-based service that allowed state partners to make eligibility determinations, rather than building and maintaining their own separate rules engines.

We hypothesize that creating a new rules service could help shift the space towards increased modularity, reuse of shared services, and adoption of modern, open source technologies, by providing an easier, faster, and less expensive way to integrate eligibility & enrollment across programs. It could also compliment [a similar service](https://www.medicaideligibilityapi.org/#/application) that already exists for Medicaid. In addition to having immediate benefit for a number of state human services agencies and millions of people, we also hypothesize that this rules service could function as an example to any federal agency looking to deliver policy through working, reusable code, rather than PDFs that require duplicative development for each implementation.

#### Where we are now

The following table describes our loose plan for exploring and building this concept. We are currently in our second phase,  focused on research. These phases align with the funding structure we are using to pursue this work.

| Phase | Goals |
| ------------- | ------------- |
| 1. Focus  | Identify project for further exploration; work out TTS's role in eligibility |
| **2. Research**  | **Develop a product strategy for an eligibility rules service** |
| 3. Build  | Build and pilot a web-based rules service for a single program |
| 4. Operate  | Operationalize the rules service |
| 5. Extend  | Extend lessons learned beyond this first rules service; move the eligibility ecosystems towards more loosely coupled, distributed and shared systems |

There are a number of questions that we need to answer during this phase before we are in a position to request funding from TTS for the next phase, which would focus on building out functional prototype.

- **[Federal partners](https://github.com/18F/eligibility-rules-service/issues/13)** - Who are our key federal partners/champions?
- **[Program](https://github.com/18F/eligibility-rules-service/issues/14)** - Which human services program is the best candidate?
- **[Users](https://github.com/18F/eligibility-rules-service/issues/15)** - Who are potential first users?
- **[Reuse vs. build](https://github.com/18F/eligibility-rules-service/issues/16)** - Has a _reclaimable_ system already been built for a state that could repurposed as a general service?
- **[Standards](https://github.com/18F/eligibility-rules-service/issues/17)** - What are the most important areas to align around, standards to adhere to, and patterns to develop to make adoption the easy choice, without being too prescriptive?
- **[Team](https://github.com/18F/eligibility-rules-service/issues/18)** - What team would we need for the following build/borrow phase?

#### Where we've been

Further information on the work we've done during this and the previous phase can be found [in the project wiki](https://github.com/18F/eligibility-rules-service/wiki).

## To be validated

#### :white_check_mark: _Validated (Phase 1):_ TTS has a role to play in the eligibility space
TTS is in a unique position to be a leader, influencing the ecosystem and its actors from a variety of angles due to our ability to work with agencies across the federal government, our experience supporting states through procurement consulting, our ongoing engagement with the vendor community, and our ability to build products and platforms for use across government. _See [Phase 1 Recommendations (Longform)](https://github.com/18F/eligibility-rules-service/wiki/Phase-1-Recommendations-:-Longform)_

#### :white_check_mark: _Validated:_ A finite piece of work appropriate to TTS can be identified
We hypothesize that the highest-value area for TTS to explore further is investigating the value and feasibility of building an API-based eligibility rules web service for a non-MAGI Medicaid human services program, to help federal human service agencies facilitate the adoption of multi-benefit eligibility determination. _See [Phase 1 Conclusions (Pitch)](https://github.com/18F/eligibility-rules-service/wiki/Phase-1-Recommendations-:-Pitch)_

#### :white_circle: Partners will want to collaborate with us to make this happen
_Not yet validated - Phase 2_ - Our initial conversations with partners have been positive and fruitful, but we have not yet formalized an arrangement.

#### :white_circle: States will want to collaborate with us to make this happen
_Not yet validated - Phase 2_

#### :white_circle: Building or repurposing a rules service is technologically advisable
_Not yet validated - Phase 2_

#### :white_circle: TTS's current strategy and direction is aligned with pursuing an effort like this
_Not yet validated - Phase 2_

#### :white_circle: A rules service can be built that allows multiple states with varying eligibility rules to use it
_Not yet validated - Phase 3_ - [MAGI in the Cloud](https://www.medicaideligibilityapi.org/#/application) has proven out aspects of this. MAGI Medicaid eligibility is relatively consistent state-to-state. More investigation is necessary.

#### :white_circle: Interested states have technical pathways to adopting a web service-based approach to rules
_Not yet validated - Phase 3_

#### :white_circle: An eligibility rules service offers a faster and cheaper way for states implement rules in their systems
_Not yet validated - Phase 4_


## How can you help?

**State human/social services agencies**

If you are part of a state human/social services agency, we're interested in talking with you about your Eligibility & Enrollment system(s), IT modernization plans, and general program eligibility determination methods.

[File an issue](https://github.com/18F/eligibility-rules-service-exemplar-research/issues) or contact Ed Mullen at edward.mullen@gsa.gov

**Non-gov organization**

If you work with an organization outside of government and you have a use case for such a service, we're interested in talking with you.

[File an issue](https://github.com/18F/eligibility-rules-service-exemplar-research/issues) or contact Ed Mullen at edward.mullen@gsa.gov

## Weekly progress updates

We're posting [weekly recaps](https://github.com/18F/eligibility-rules-service/wiki/Weekly-recaps) of our work for folks interested in following along with our progress.
