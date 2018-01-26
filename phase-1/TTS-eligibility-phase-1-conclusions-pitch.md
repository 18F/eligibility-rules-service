# Eligibility & enrollment discovery sprint recommendations

There are an abundance of opportunities for TTS to contribute in the benefits eligibility & enrollment space, so we recommend moving forward with further work. In the interest of focusing that work, we hypothesize **that the highest-value area for TTS to explore further is investigating the value and feasibility of building an API-based eligibility rules web service for a non-Medicaid human services program** (most likely for SNAP or TANF), to help federal human service agencies facilitate the adoption of multi-benefit eligibility determination. 

## Why this matters

15-40% of US residents who are eligible to receive federal benefits like healthcare and food assistance are not receiving those benefits. Our research with USDS last year provided tangible evidence that one of the biggest barriers contributing to this enrollment gap is the fact that people have to painstakingly apply for each benefit one at a time. This research found that helping people enroll for multiple benefits through a single, streamlined application would significantly increase needy families’ access to the services they need.

While federally funded and managed, these benefits programs are administered at the state level, and many of these states are struggling to integrate multiple human services programs into their eligibility & enrollment systems due to the variation and complexity of the policy rules that determine eligibility for each program, as well as outdated, monolithic procurement and development practices, limited reusable components, and scarce resources.

We believe that creating a new rules service for one of the next-largest programs (SNAP or TANF) to compliment a similar service that already exists for Medicaid, would help shift the space towards increased modularity, reuse of shared services, and adoption of modern, open source technologies, by providing an easier, faster, and less expensive way to integrate eligibility & enrollment across programs. In addition to having immediate benefit for a number of federal human services agencies and millions of US residents, we also see this rules service functioning as an example to any federal agency looking to deliver policy through working, reusable code, rather than PDFs that require duplicative development for each implementation.

Because of our unique technical expertise, the subject matter expertise we’re developing through our existing and past work in the space, and our access to federal agencies as federal employees, TTS is well-positioned to see the problems from many angles and inject key, transformative components that can have ripple effects across the entire ecosystem.  

## How we arrived at this conclusion

We spoke with existing players in the space to identify what work is already happening, where the biggest pain points are, and where TTS might be particularly well positioned to help.

There are already several complementary work streams underway, some led by TTS and some by other orgs, which would help amplify the impact of the service we are proposing, and which in turn would be bolstered by the existence of this service. These work streams include:

1. **Helping transform the way states buy and build their eligibility and enrollment systems.** The TTS Acquisitions team is currently engaged in this work with CMS and Alaska’s Dept. of Health & Human Services.
2. **Enriching the ecosystem with reusable, loosely-coupled components others can quickly implement.** We spoke with many organizations, including USDS, Nava, BlueLabs, etc who are building complementary pieces of the puzzle; our proposal for a API-based rules service would directly complement these efforts.
3. **Advocating for a streamlined, multi-benefit enrollment experience,** which started with a research sprint & prototype development between USDS and 18F last year, and is being carried forward by Code for America.

## Our proposal for the next phase of work

- Conducting user, technical, and strategic research to prepare for a subsequent build or borrow phase focused on producing an exemplar, reusable rules service for a single human services program.
- Researching and documenting existing state systems and approaches to determine the level of preparedness for the more modular, service-based world, and identify key partners.
- Reviewing existing codebases produced by states to determine whether reclaiming some aspect of an existing codebase and reworking it into a standalone service is a viable and efficient strategy.

## Questions the next phase should answer

- Would we need to start from scratch, or does a reclaimable rules engine exist that we could start from?
- Which human services program should we start with?
- Who are our key federal partners/champions, and our potential first adopters?
- How do we make these reusable components most attractive to states? Are there any incentives we could build in?
- What are the most important areas to align around, standards to adhere to, and patterns to develop to make adoption the easy choice, without being too prescriptive?
- What team would we need for the following build/borrow phase?
