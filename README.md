# Utopia: An Alexa skill that helps with depression
[![Build Status](https://travis-ci.org/k-chuang/utopia-alexa-skill.svg?branch=master)](https://travis-ci.org/k-chuang/utopia-alexa-skill) [![codecov](https://codecov.io/gh/k-chuang/utopia-alexa-skill/branch/master/graph/badge.svg)](https://codecov.io/gh/k-chuang/utopia-alexa-skill)


Utopia is the name of the Alexa skill that is designed to help people with depression.

## Architecture
![alt text](images/Utopia-alexa-skill-architecture.png)

## Description

According to the [World Health Organization](http://www.who.int/mediacentre/factsheets/fs369/en/), 350 million people worldwide
suffer from depression. Depression is the leading cause of disability.

This skill is meant to help people who are going through depression. The main feature of this skill involves taking
the [Hamilton Depression Rating Scale Survey](https://www.psychcongress.com/saundras-corner/scales-screeners/depression/hamilton-depression-rating-scale-ham-d) to get a general idea of the severity of depression, and based on the score
of the survey, the skill would recommend certain natural remedies to help. The other complementary features include giving
positive and motivational quotes (other types of quotes are also supported), proposing natural solutions, a mindfulness meditation exercise,
recommendations for nearby therapists, and, if necessary, getting help from the National Suicide Prevention Lifeline.

**Disclaimer**: Utopia is not meant to be a substitute for professional medical advice, treatment or diagnosis.
It is more of a supplemental and informational helper to mitigate depression. The people who programmed this are not experts in mental illnesses such as depression,
and this is a product of our subjectivity and couple months of basic research on depression.

## Features

* [Hamilton Depression Rating Scale Survey](https://www.psychcongress.com/saundras-corner/scales-screeners/depression/hamilton-depression-rating-scale-ham-d) consisting of 16 questions to analyze and evaluate level of depression.
  * Added three bonus questions that uses [NLTK](http://www.nltk.org/) sentiment analysis to contribute to the survey score.
* Grab and read different types of quotes from [BrainyQuote](https://www.brainyquote.com/)
  * A few popular categories of quotes include positive, motivational, inspirational, family, love, and positive.
* Give advice and ideas for activities to improve mood
  * Examples include:
    * *Listen to music that makes you feel good.*
    * *Take note of all the small things you've accomplished today.*
* Listen to a collection of uplifting & powerful poems
* Recommend therapists nearby using [Google Places API](https://developers.google.com/places/) by providing contact information, current availability, and open hours
  * Will find nearby available therapists, and if there are no open therapists nearby, will default to all nearby therapist places (open or closed)
* [National Suicide Prevention Lifeline](https://suicidepreventionlifeline.org/)
  * If certain trigger words are said, this feature will automatically trigger and provide user with contact information for the suicide hotline.
  * For a full list of trigger words, see [Trigger Words](speech_assets/custom_slot_types/TriggerWords.txt)

## Technology

Utopia is powered by Python, [Flask-Ask](http://flask-ask.readthedocs.io/en/latest/) (an extension of [Flask](http://flask.pocoo.org/docs/0.12/),
a micro web framework), and the [Alexa Skills kit](https://developer.amazon.com/alexa-skills-kit).

## Usage
To start using it, say a simple invocation phrase, such as the following listed below:

| Starting Phrase                          | Example                              |
|------------------------------------------|--------------------------------------|
| \<invocation name>                        | Alexa, Utopia                        |
| Ask \<invocation name>                    | Alexa, Ask Utopia                    |
| Begin \<invocation name>                  | Alexa, Begin Utopia                  |
| Launch \<invocation name>                 | Alexa, Launch Utopia                |
| Load \<invocation name>                   | Alexa, Load Utopia                   |
| Open \<invocation name>                   | Alexa, Open Utopia                   |
| Run \<invocation name>                    | Alexa, Run Utopia                    |
| Start \<invocation name>                  | Alexa, Start Utopia                  |
| Use \<invocation name>                    | Alexa, Use Utopia                    |


To start and hear the available features, you can say the following:

    Alexa, start Utopia and help

## Testing & Code Coverage
To run tests and check code coverage, run the following command in the root project folder:

```bash
$ pytest tests/test_utopia_unit.py -v —cov utopia —cov-report term-missing
```

The project uses pytest as the test runner. The command above will execute the tests and check for test code coverage of the main program ([utopia.py](utopia.py)), and report which lines were not covered by the test suite ([test_utopia_unit.py](tests/test_utopia_unit.py)).

#### Travis CI
This project uses [Travis-CI](https://travis-ci.org/), a hosted, distributed continuous integration service that builds and tests software hosted on GitHub. Every commit that is pushed to a GitHub repo automatically triggers [Travis CI](https://travis-ci.org/) to run, build and test your software.

The continuous integration configuration is specified in [.travis.yml](.travis.yml) file, and specifies the programming language used, desired building and testing environments, and various other parameters. For this project, the configuration is set up to create environment variables, install necessary dependencies, run the test suite, and after a successful test run, report code coverage.

[Travis CI](https://travis-ci.org/) generates a badge with the current build status (displayed above). Click on the badge for more information.

#### Codecov
This project uses [Codecov](https://codecov.io/) to generate code coverage reports. [Codecov](https://codecov.io/) is a free, open source code coverage reporting tool that integrates seamlessly with GitHub. It calculates and measures code coverage and delivers the coverage metrics in a clear, understandable way. Similar to Travis CI, [Codecov](https://codecov.io/) also generates a clickable badge with the current code coverage metrics.

## To Be Continued...
I will add more to this as I get farther into the project.
