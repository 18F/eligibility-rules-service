# Eligibility rules service - Phase 2 (research/discovery)

## What is this project?

18F is conducting research to identify opportunities for developing a web-based eligibility rules service that could be used to make eligibility determinations for a human services program. This _Phase 2_ work follows a prior _Phase 1_ investigation sprint that identified creating such a service as worthy of further exploration. This repository documents Phase 2.

**The problem:**

Many states struggle to modernize their human services eligibility and enrollment systems due to the variation and complexity of the policy rules that determine eligibility for federally funded programs, as well as outdated, monolithic procurement and development practices, limited reusable components, and scarce resources. These efforts lead to duplicative work and expense across states without delivering better service. 

**Our hypothesis:** 

Both federal and state agencies could achieve greater program efficiencies if the administering federal agency offered a configurable, API-based service that allowed state partners to make eligibility determinations, rather than building and maintaining their own separate rules engines.

We hypothesize that creating a new rules service could help shift the space towards increased modularity, reuse of shared services, and adoption of modern, open source technologies, by providing an easier, faster, and less expensive way to integrate eligibility & enrollment across programs. It could also compliment [a similar service](https://www.medicaideligibilityapi.org/#/application) that already exists for Medicaid. In addition to having immediate benefit for a number of state human services agencies and millions of people, we also hypothesize that this rules service could function as an example to any federal agency looking to deliver policy through working, reusable code, rather than PDFs that require duplicative development for each implementation.

## Questions we need to answer

- **[Federal partners](https://github.com/18F/eligibility-rules-service/issues/13)** - Who are our key federal partners/champions?
- **[Program](https://github.com/18F/eligibility-rules-service/issues/14)** - Which human services program is the best candidate?
- **[Users](https://github.com/18F/eligibility-rules-service/issues/15)** - Who are potential first users?
- **[Reuse vs. build](https://github.com/18F/eligibility-rules-service/issues/16)** - Has a _reclaimable_ system already been built for a state that could repurposed as a general service?
- **[Standards](https://github.com/18F/eligibility-rules-service/issues/17)** - What are the most important areas to align around, standards to adhere to, and patterns to develop to make adoption the easy choice, without being too prescriptive?
- **[Team](https://github.com/18F/eligibility-rules-service/issues/18)** - What team would we need for the following build/borrow phase?

## How can you help?

**State human/social services agencies**

If you are part of a state human/social services agency, we're interested in talking with you about your Eligibility & Enrollment system(s), IT modernization plans, and general program eligibility determination methods.

[File an issue](https://github.com/18F/eligibility-rules-service-exemplar-research/issues) or contact Ed Mullen at edward.mullen@gsa.gov

**Non-gov organization**

If you work with an organization outside of government and you have a use case for such a service, we're interested in talking with you.

[File an issue](https://github.com/18F/eligibility-rules-service-exemplar-research/issues) or contact Ed Mullen at edward.mullen@gsa.gov

## Weekly progress updates

We're posting [weekly recaps](https://github.com/18F/eligibility-rules-service-exemplar-research/wiki/Shipping-reports) of our work for folks interested in following along with our progress.
