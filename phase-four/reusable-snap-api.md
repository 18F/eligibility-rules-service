***

#### Table of contents

1. [Background](/phase-four/background.md/)
2. [Procurement resources for agencies](/phase-four/procurement-resources.md/)
3. **Reusable SNAP API prototype and calculator**

***

## Reuse or extend the SNAP benefit calculator

![Demo of a SNAP benefit calculator](/assets/snappreview.gif)

Interested in adding a version of [this SNAP benefit calculator](https://federalist-1c734efa-8e7a-40ed-9b1e-432001a347e9.app.cloud.gov/site/18f/snap-js-prescreener-prototypes/prescreeners/va.html) to your own organization’s website?

A benefit calculator like this one can help someone decide if it is worth their time and energy to submit a full application. It can give them an understanding of their likely eligibility and their estimated benefit amount. Note that this benefit calculator provides estimates only, and is not the same as an official determination.

We built this calculator using a model of SNAP eligibility rules as code that can potentially be reused and extended. This is an approach that any human services program could try to reduce duplication of effort, and improve accuracy.

If you’re a programmer, take a look at our documentation on [how to create a benefit calculator for your state](https://github.com/18F/snap-js-prescreener-prototypes/wiki/How-to-create-a-new-state-or-territory-calculator).

If you’re not a programmer, but know one who might be interested in working with you to create a calculator for your state, here’s sample language you could send:

> Hi ____,
> I found a project that could add a public-facing SNAP benefits calculator to our website that can be easily modified for our state.
> The project description says that it requires only HTML, CSS, and Javascript, so we could add the calculator directly to our website. Here is the documentation they have for how to add a new benefit calculator:
> [https://github.com/18F/snap-js-prescreener-prototypes/wiki/How-to-create-a-new-state-or-territory-calculator](
https://github.com/18F/snap-js-prescreener-prototypes/wiki/How-to-create-a-new-state-or-territory-calculator)

## Reuse this approach: federal + state rules as code

The benefit calculator is powered by a prototype model of SNAP eligibility rules as code. The model includes core federal rules and can incorporate options for each state or territory, since states have different options within SNAP, such as setting different income limits through [Broad-Based Categorical Eligibility](https://www.fns.usda.gov/snap/broad-based-categorical-eligibility) (BBCE).

An agency could publish its official rules in the same way. Taking this approach could make eligibility rules more transparent and reusable by states, other government agencies, and civil society.

To inquire about partnering with 18F on adopting an approach like this for your program, reach out to [inquiries18f@gsa.gov](mailto:inquiries18f@gsa.gov).