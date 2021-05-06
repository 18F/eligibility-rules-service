Project recap links and notes on lessons learned.

### 1. Prototype: SNAP Python API

* Links:
  * https://github.com/18F/snap-api-prototype
  * https://github.com/18F/snap-api-prototype/blob/master/snap_financial_factors/program_data/state_options.yaml
* Lessons learned: 
  * Creating a backend eligibility API that would integrate with mission-critical state systems is a very, very tough sell ...
  * ... and raises important questions related to federalism

### 2. Prototype: SNAP Rules-as-Code in JS

* Links:
  * https://github.com/18F/snap-js-api-prototype
  * https://federalist-1c734efa-8e7a-40ed-9b1e-432001a347e9.app.cloud.gov/site/18f/snap-js-prescreener-prototypes/prescreeners/va.html
  * https://vplc.org/snap-calculator/
* Lessons learned: 
  * Implementing rules in JS makes them reusable via browser-based calculators.
  * ... and is a good way to visualize the rules and make them interactive! 
    * A step towards building confidence to integrate them in more mission-critical places.


### 3. External fork: Snapscreener.com

* Links: 
  * https://www.snapscreener.com/
  * https://www.snapscreener.com/?p=table
* Lessons:
  * If you build it ... sometimes they will come (and fork your repo and contribute!)
  * We have an example of what gathering and validating state eligibility options/parameters could look like
