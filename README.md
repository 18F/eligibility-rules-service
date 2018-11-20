# Eligibility rules service

> **Follow this work** 
> - Phase 3 is in progress. We're working with a new program exploring state system integration.
> - Read our [weekly recaps](https://github.com/18F/eligibility-rules-service/wiki/Weekly-recaps#phase-3---october-1-2018-to-present)
> - "Watch" or "star" the repo above
> - Read our blog posts [Implementing rules without a rules engine](https://18f.gsa.gov/2018/10/09/implementing-rules-without-rules-engines/) and [Exploring a new way to make eligibility rules easier to implement](https://18f.gsa.gov/2018/10/16/exploring-a-new-way-to-make-eligibility-rules-easier-to-implement/)
> - We're seeking additional partners. [Here's what we're looking for.](lets-talk.md)
> - Email us at eligibility.rules.service@gsa.gov

## Project description

The [eligibility rules service project](#project-description) is exploring the idea of providing shared web services that states could use to help make eligibility determinations for human services programs.

To [validate this idea](#to-be-validated), we have built a prototype eligibility rules service for The Special Supplemental Nutrition Program for Women, Infants, and Children (WIC). **The prototype is for demonstration purposes only and is not an official interpretation of policy.** It serves to help us learn about the challenges for such a service.   

- [**Try prototype using the API**](https://github.com/18F/wic_rules#using-the-api)
- [**Try prototype using a web form**](https://eligibility-rules-form.fr.cloud.gov/)

#### The problem

Many states struggle to modernize their human services eligibility and enrollment systems due to the variation and complexity of the policy rules that determine eligibility for federally funded programs, as well as outdated, monolithic procurement and development practices, limited reusable components, and scarce resources. These efforts lead to duplicative work and expense across states without delivering better service.

[![View project introduction presentation](assets/what-is-the-eligibility-rules-service-project.jpg)](assets/what-is-the-eligibility-rules-service-project.pdf)

> View presentation [What is the Eligibility Rules Service project?](assets/what-is-the-eligibility-rules-service-project.pdf)

#### Our hypothesis

Both federal and state agencies could achieve greater program efficiencies if the administering federal agency offered a configurable, API-based service that allowed state partners to make eligibility determinations, rather than building and maintaining their own separate rules engines.

We hypothesize that creating a new rules service could help shift the space towards increased modularity, reuse of shared services, and adoption of modern, open source technologies, by providing an easier, faster, and less expensive way to integrate eligibility & enrollment across programs. It could also compliment [a similar service](https://www.medicaideligibilityapi.org/#/application) that already exists for Medicaid. In addition to having immediate benefit for a number of state human services agencies and millions of people, we also hypothesize that this rules service could function as an example to any federal agency looking to deliver policy through working, reusable code, rather than PDFs that require duplicative development for each implementation.

#### Where we are now

The following table describes our loose plan for exploring and building this concept. **We are currently in Phase 3.** These phases align with the funding structure we are using to pursue this work.

| Phase | Goals |
| ------------- | ------------- |
| 1. Focus  | Identify project for further exploration; work out TTS's role in eligibility |
| 2. Research  | Develop a product strategy for an eligibility rules service |
| 3. Build  | Build and pilot a web-based rules service for a single program |
| 4. Operate  | Operationalize the rules service |
| 5. Extend  | Extend lessons learned beyond this first rules service; move the eligibility ecosystems towards more loosely coupled, distributed and shared systems |

#### Where we've been

Further information on the work we've done during this and the previous phase can be found [in the project wiki](https://github.com/18F/eligibility-rules-service/wiki).

## To be validated

#### :white_check_mark: _Validated (Phase 1):_ TTS has a role to play in the eligibility space
TTS is in a unique position to be a leader, influencing the ecosystem and its actors from a variety of angles due to our ability to work with agencies across the federal government, our experience supporting states through procurement consulting, our ongoing engagement with the vendor community, and our ability to build products and platforms for use across government. _See [Phase 1 Recommendations (Longform)](https://github.com/18F/eligibility-rules-service/wiki/Phase-1-Recommendations-:-Longform)_

#### :white_check_mark: _Validated:_ A finite piece of work appropriate to TTS can be identified
We hypothesize that the highest-value area for TTS to explore further is investigating the value and feasibility of building an API-based eligibility rules web service for a non-MAGI Medicaid human services program, to help federal human service agencies facilitate the adoption of multi-benefit eligibility determination. _See [Phase 1 Conclusions (Pitch)](https://github.com/18F/eligibility-rules-service/wiki/Phase-1-Recommendations-:-Pitch)_

#### :white_check_mark: _Validated:_ Partners will want to collaborate with us to make this happen
Through a series of conversations with potential partners at CMS and FNS, we’ve validated that there are indeed interested partners at the federal level. Through all of these conversations, the general concept resonated and potential use cases were identifiable.

#### :white_check_mark: _Validated:_ States will want to collaborate with us to make this happen
We have identified one state program interested in working with us going forward. While we still intend to identify one or two others, through conversations with states and FNS regional program specialists, we feel confident that problem we are working to address is broadly applicable and that we'll be able to find those partners.  

#### :white_check_mark: _Validated:_ Building or repurposing a rules service is technologically advisable
The level of effort in building out a rules service turned out to be less than anticipated. Our prototype functionality approximated the what we'd anticipate an MVP needing. As such, the effort associated with building a rules service from scratch is low enough to make repurposing an existing system unneccessary.

#### :white_check_mark: _Validated:_ A rules service can be built that allows multiple states with varying eligibility rules to use it
Building off of lessons learned from [MAGI in the Cloud](https://www.medicaideligibilityapi.org/#/application), we wanted to validate we could build a rules service that would accommodate a program where state policies vary considerably. WIC varies both in the income standard which follows the USDA's reduced price school lunch guidelines as well as the policy options implemented at the state level. Our prototype solves for both scenario.

#### :white_check_mark: _Validated:_ TTS's current strategy and direction is aligned with pursuing an effort like this
After presenting our Phase 2 conclusions to the TTS 10x review board, the group that evaluates whether our work is meeting it's objectives and whether it should continue, we were approved to proceed to Phase 3, validating that TTS finds this work valuable and is the kind of work we should be doing.

#### :white_circle: Interested states have technical pathways to adopting a web service-based approach to rules
_Not yet validated - Phase 3_

#### :white_circle: An eligibility rules service offers a faster and cheaper way for states implement rules in their systems
_Not yet validated - Phase 4_


## How can you help?

**State human/social services agencies**

If you are part of a state human/social services agency, we're interested in talking with you about your Eligibility & Enrollment system(s), IT modernization plans, and general program eligibility determination methods.

[File an issue](https://github.com/18F/eligibility-rules-service-exemplar-research/issues) or email us at eligibility.rules.service@gsa.gov

**Non-gov organization**

If you work with an organization outside of government and you have a use case for such a service, we're interested in talking with you.

[File an issue](https://github.com/18F/eligibility-rules-service-exemplar-research/issues) or email us at eligibility.rules.service@gsa.gov

## Weekly progress updates

During active phases, we post [weekly recaps](https://github.com/18F/eligibility-rules-service/wiki/Weekly-recaps) of our work for folks interested in following along with our progress.
