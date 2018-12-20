This is a running document cataloging product decisions.

*Contents* - [Design principles](#design-principles) | [Product matters](#product-matters)

----

## Design principles
The following principles are in-progress. 

### MVP design principles

**1. Awareness of likely ineligibility due to personal financial information should not impede or determine whether data is to be submitted.** Customers should be able to submit their data even if the rules service indicates that they are not likely to be eligible.

### Design principles from [USDS multi-benefit application](https://usds.github.io/benefits-enrollment-prototype/) project

**1. Design for real-time eligibility determination and same-day enrollment.** Model how states would collect data to verify against other government systems when possible.
  - We are not attempting to "make eligibility determinations". We are trying to make it easier for customers to submit their data, easier for  Eligibility Workers to make eligibility determinations, and streamline the process to speed benefit delivery.

**2. Work to connect people to the programs they want and need, in as few steps as possible.** Give applicants the option to apply for multiple benefits at once or to apply for just one benefit while informing them of other programs available to them.
 - We aspire to this reality, but are currently focused on D-SNAP.

**3. Mobile-first responsive design.** Ensure that people can apply on all devices by designing first for small screens and low bandwidth.
- Inheriting fully.

**4. Plain language and warm voice.** These programs are complicated: do the hard work to keep the wording deadly simple. Use a conversational, encouraging tone and show people where they are in the process at all times.
- Inheriting fully.

**5. Fewer prompts per screen.** Ask people questions in small bite-sized chunks, so as not to overwhelm with multiple complex questions at any single step. Always let people know where they are in the process.
- Inheriting fully.

**6. Personalize and tailor applications.** Only show applicants information related to their specific circumstance.
- Inheriting fully.

----

## Product matters
The following matters are intended to describe open questions or decisions about product directions. There are listed roughly in sequential order as defined in the application flow diagram.

### Step 0 - ENTRY

#### Registering vs. Applying
- We need to decide on the language we will use to describe what a customer is doing through this tool.
- To date, the online tools have been described as "pre-registration". (The "pre-" part seems unnecessary.) 
- It wasn't considered an "application" until the eligibility worker interview.
- Calling the initial submission of data a "registration" may reduce the requirements around attestations. (There may be legal implications.)  
- Ed's assumption is that "applying" is more aligned with what customers think they are doing than "registering".
- **Decision needed**
  - Do we call the app a registration app our an online application?
  
#### Screener
- USDS prototype has a lightweight screener up front. 
- The current plan is to not include a screener for D-SNAP because the money-related requirements are a bit difficult to understand and we don't want to discourage people from applying. 
- Avoiding the work of building a screener aligns with our MVP
- **Decided**
  - In lieu of our screener, we're going to provide messaging about eligibility criteria up front and move Adverse effects questions to early in the experience.

### Step 1 - REGISTRANT

#### Race and Sex
- The FNS sample application asks for race and sex from household members.
- Race has been added back into the mocks.
- **Decisions needed**
  - Are we required to ask race? Assumption is yes.
  - Is this a free text field or a menu of choices

### Step 2 - IDENTITY

### Step 3 - HOUSEHOLD

### Step 4 - ADVERSE EFFECTS

#### Adverse effects
- The adverse effects questions should be separate from disaster expenses.
  - This needs to change from the current mockups. 
  - These three questions may be able to be presented up front to act similar to a screener since one must be true to qualify.
  - The FNS sample paper application asks a series of questions up front. These include the adverse effects questions and with approved language.
  - The pro for moving is that these are qualifying questions. If they are not met, we know the household is not eligible, even before submitting personal data. Alerting to this fact could save customers time.
  - The con is that moving these questions up before the household has been established means the customer's mental model of the household may not match that of the program (buy and share food).
- **Decided**
  - The adverse effect questions should not be bundled with disaster expenses.
- **Decisions needed**
  - Where should we move the adverse effects questions to?
  - How should we accommodate the partial logic? Should we allow the service to answer single rule requests? We probably don't want any logic in the app.
  - From sample paper application: *"Did the disaster damage or destroy your home or self-employment property?"* What impact does this have? Should it be one of the qualifying adverse effects questions?

### Step 5 - RESOURCES & INCOME

### Step 6 - REVIEW & SUBMIT

#### Displaying rules-service assessment
- We need to decide which screen is appropriate to initially show customers the rules-service based assessment of likely eligibility.
- The current plan is to show this information after the attestation/e-signature screen.
- By waiting to show this assessment until after the signature, we're thinking we will avoid discouraging people from submitting their information.
- **Decision needed**
  - On which screen do we first indicate likely eligibility?

#### Submitting data
- The consensus approach that we're going to take is that once the form data has been reviewed, we will allow all registrants to sign and submit the data.
- **Decided**
  - We will not stop registrants who appear ineligible from doing so.

### Step 7 - NEXT STEPS

#### Next step guidance info
- At this point we will know the customer's likely eligibility and have the ability to display different information depending on the outcome. 
- **Decision needed**
  - What do we want to say to customers once we've determined their likely eligibility/ineligibility?

### WORKER EXPERIENCE

#### Registration/application lookup
- Need to determine which attributes a worker can use to pull up a registration/application.
- We know Florida's workflow uses state ID, but we'll need some additional, universally required element such as name.
- **Decision needed**
  - What attributes can a worker look-up an application with?

