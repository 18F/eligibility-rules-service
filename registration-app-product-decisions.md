This is a running document cataloging product decisions.

*Contents* - [Design principles](#design-principles) | [Matters](#matters)

----

## Design principles
The following principles are in-progress. 

### MVP design principles
**The rules service should not be used to impede or the data being submitted.** The system shouldn't decide who can submit data

### Design principles from [USDS multi-benefit application](https://usds.github.io/benefits-enrollment-prototype/) project

**1. Design for real-time eligibility determination and same-day enrollment.** Model how states would collect data to verify against other government systems when possible.
  - We are not attempting to "make eligibility determinations". We are trying to make it easier for customers to submit their data, easier for  Eligibility Workers to make eligibility determinations, and streamline the process to speed benefit delivery.

**2.Work to connect people to the programs they want and need, in as few steps as possible.** Give applicants the option to apply for multiple benefits at once or to apply for just one benefit while informing them of other programs available to them.
 - We aspire to this reality, but are currently focused on D-SNAP.

**3.Mobile-first responsive design.** Ensure that people can apply on all devices by designing first for small screens and low bandwidth.
- Inheriting fully.

**4.Plain language and warm voice.** These programs are complicated: do the hard work to keep the wording deadly simple. Use a conversational, encouraging tone and show people where they are in the process at all times.
- Inheriting fully.

**5.Fewer prompts per screen.** Ask people questions in small bite-sized chunks, so as not to overwhelm with multiple complex questions at any single step. Always let people know where they are in the process.
- Inheriting fully.

**6.Personalize and tailor applications.** Only show applicants information related to their specific circumstance.
- Inheriting fully.

----

## Matters
The following matters are intended to describe open questions or decisions about product directions. There are listed roughly in sequential order as defined in the application flow diagram.

### Step 0 - ENTRY

#### Registering vs. Applying
- We need to decide on the language we will use to describe what a customer is doing through this tool.
- To date, the online tools have been described as "pre-registration". (The "pre-" part seems unnecessary.) 
- It wasn't considered an "application" until the eligibility worker interview.
- Calling the initial submission of data a "registration" may reduce the requirements around attestations. (There may be legal implications.)  
- Ed's assumption is that "applying" is more aligned with what customers think they are doing than "registering".
  
#### Screener
- USDS prototype has a lightweight screener up front. 
- The current plan is to not include a screener for D-SNAP because the money-related requirements are a bit difficult to understand and we don't want to discourage people from applying. 
- Avoiding the work of building a screener aligns with our MVP
- In lieu of our screener, we're going to provide messaging about eligibility criteria up front and move Adverse effects questions to early in the experience.

### Step 1 - REGISTRANT

#### Race and Sex
- The FNS sample application asks for race and sex from household members.
- Need to check if this means we should include; assumption is yes.

### Step 2 - IDENTITY

### Step 3 - HOUSEHOLD

### Step 4 - ADVERSE EFFECTS

#### Adverse effects
- The adverse effects questions should be separate from disaster expenses.
- This needs to change from the current mockups. 
- These three questions may be able to be presented up front to act similar to a screener since one must be true to qualify.
- The FNS sample paper application asks a series of questions up front. These include the adverse effects questions and with approved language.

### Step 5 - RESOURCES & INCOME

### Step 6 - REVIEW & SUBMIT

#### Displaying rules-service assessment
- We need to decide which screen is appropriate to initially show customers the rules-service based assessment of likely eligibility.
- The current plan is to show this information after the attestation/e-signature screen.
- By waiting to show this assessment until after the signature, we're thinking we will avoid discouraging people from submitting their information.

#### Submitting data
- The consensus approach that we're going to take is that once the form data has been reviewed, we will allow all registrants to sign and submit the data.
- We will not stop registrants who appear ineligible from doing so.

### Step 7 - NEXT STEPS

### WORKER EXPERIENCE
