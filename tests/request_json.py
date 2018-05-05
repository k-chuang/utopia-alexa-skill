# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Initialize global variables
LIST_OF_QUESTIONS_FOUR = ['One', 'Two', 'Seven', 'Eight',  'Ten', 'Eleven', 'Fifteen']
SUICIDE_QUESTION = 'Three'
LIST_OF_QUESTIONS_TWO = ['Four', 'Five', ' Six', 'Nine', 'Twelve', 'Thirteen', 'Fourteen', 'Sixteen']
LIST_OF_BONUS = ['BonusOne', 'BonusTwo', 'BonusThree', ]

LIST_OF_BONUS_WAIT = ['BonusOneWait', 'BonusTwoWait', 'BonusThreeWait']


launch_body = {
    "request": {
        "locale": "en-US",
        "requestId": "amzn1.echo-api.request",
        "timestamp": "2018-04-26T22:52:14Z",
        "type": "LaunchRequest"
    },
    "session": {
        "application": {
            "applicationId": "amzn1.ask.skill"
        },
        "new": True,
        "sessionId": "amzn1.echo-api.session",
        "user": {
            "userId": "amzn1.ask.account"
        }
    },
    "version": "1.0"
}

sess_end_body = {
    "request": {
        "type": "SessionEndedRequest"
    },
    "version": "1.0"
}

stop_body = {
    "request": {
        "intent": {
            "name": "AMAZON.StopIntent"
        },
        "type": "IntentRequest"
    },
    "session": {
        "application": {
            "applicationId": "amzn1.ask.skill"
        },
        "new": False,
        "sessionId": "amzn1.echo-api.session",
        "user": {
            "userId": "amzn1.ask.account"
        }
    },
    "version": "1.0"
}

help_body = {
    "request": {
        "intent": {
            "name": "AMAZON.HelpIntent"
        },
        "type": "IntentRequest"
    },
    "session": {
        "application": {
            "applicationId": "amzn1.ask.skill"
        },
        "new": False,
        "sessionId": "amzn1.echo-api.session",
        "user": {
            "userId": "amzn1.ask.account"
        }
    },
    "version": "1.0"
}

suicide_hotline_body = {
    "request": {
        "intent": {
            "name": "SuicideHotLine"
        },
        "locale": "en-US",
        "requestId": "amzn1.echo-api.request",
        "timestamp": "2018-04-26T22:45:12Z",
        "type": "IntentRequest"
    },
    "session": {
        "application": {
            "applicationId": "amzn1.ask.skill"
        },
        "new": False,
        "sessionId": "amzn1.echo-api.session",
        "user": {
            "userId": "amzn1.ask.account"
        }
    },
    "version": "1.0"
}

get_quote_type_completed_body = {
    "request": {
        "dialogState": "COMPLETED",
        "intent": {
          "confirmationStatus": "NONE",
          "name": "GetQuoteTypeIntent",
          "slots": {
            "Category": {
              "confirmationStatus": "NONE",
              "name": "Category",
              "value": "love"
            }
          }
        },
        "locale": "en-US",
        "requestId": "amzn1.echo-api.request",
        "timestamp": "2018-04-26T22:45:12Z",
        "type": "IntentRequest"
    },
    "session": {
        "application": {
            "applicationId": "amzn1.ask.skill"
        },
        "new": False,
        "sessionId": "amzn1.echo-api.session",
        "user": {
            "userId": "amzn1.ask.account"
        }
    },
    "version": "1.0"
}
name_intent_body ={
    "request": {
        "intent": {
            "name": "NameIntent",
            "slots": {
                "FirstName": {
                    "name": "FirstName",
                    "value": "Kevin"
                }
            }
        },
        "locale": "en-US",
        "requestId": "amzn1.echo-api.request",
        "timestamp": "2018-04-26T22:45:12Z",
        "type": "IntentRequest"
    },
    "session": {
        "application": {
            "applicationId": "amzn1.ask.skill"
        },
        "new": False,
        "sessionId": "amzn1.echo-api.session",
        "user": {
            "userId": "amzn1.ask.account"
        }
    },
    "version": "1.0"
}

recommend_therapist_body = {
    "request": {
        "intent": {
            "name": "RecommendTherapist"
        },
        "locale": "en-US",
        "requestId": "amzn1.echo-api.request",
        "timestamp": "2018-04-26T22:45:12Z",
        "type": "IntentRequest"
    },
    "session": {
        "application": {
            "applicationId": "amzn1.ask.skill"
        },
        "new": "True",
        "sessionId": "amzn1.echo-api.session",
        "user": {
            "userId": "amzn1.ask.account"
        }
    },
    "version": "1.0",
    "context": {
        "System": {
          "application": {
            "applicationId": "fake-application-id"
          },
          "user": {
              "permissions": {
                  "consentToken": "FAKE_CONSENT_TEST_TOKEN"
              },
            "userId": "amzn1.account.AM3B00000000000000000000000"
          },
            "device": {
            "deviceId": "amzn1.ask.device",
            "supportedInterfaces": {
                "AudioPlayer": {},
                "Display": {
                    "markupVersion": "1.0",
                    "templateVersion": "1.0"
                    }
                }
            },
        }
    }
}

give_quote_body = {
    "request": {
        "intent": {
            "name": "QuoteIntent",
            "slots": {
                "Category": {
                    "name": "category",
                    "value": "inspirational"
                }
            }
        },
        "locale": "en-US",
        "requestId": "amzn1.echo-api.request",
        "timestamp": "2018-04-26T22:45:12Z",
        "type": "IntentRequest"
    },
    "session": {
        "application": {
            "applicationId": "amzn1.ask.skill"
        },
        "new": False,
        "sessionId": "amzn1.echo-api.session",
        "user": {
            "userId": "amzn1.ask.account"
        }
    },
    "version": "1.0"
}

give_poem_body ={
  "version": "1.0",
  "session": {
    "new": True,
    "sessionId": "amzn1.echo-api.session",
    "application": {
      "applicationId": "fake-application-id"
    },
    "attributes": {},
    "user": {
      "userId": "amzn1.account"
    }
  },
  "context": {
    "System": {
      "application": {
        "applicationId": "fake-application-id"
      },
      "user": {
        "userId": "amzn1.account"
      },
      "device": {
        "supportedInterfaces": {
          "AudioPlayer": {}
        }
      }
    },
    "AudioPlayer": {
      "offsetInMilliseconds": 0,
      "playerActivity": "IDLE"
    }
  },
  "request": {
    "type": "IntentRequest",
    "requestId": "string",
    "timestamp": "string",
    "locale": "string",
    "intent": {
      "name": "PoemIntent",
      "slots": {
        }
      }
    }
}

give_advice_body = {
    "request": {
        "intent": {
            "name": "GiveAdvice"
        },
        "locale": "en-US",
        "requestId": "amzn1.echo-api.request",
        "timestamp": "2018-04-26T22:45:12Z",
        "type": "IntentRequest"
    },
    "session": {
        "application": {
            "applicationId": "amzn1.ask.skill"
        },
        "attributes": {
            "Category": "positive"
        },
        "new": "True",
        "sessionId": "amzn1.echo-api.session",
        "user": {
            "userId": "amzn1.ask.account"
        }
    },
    "version": "1.0"
}

general_survey_body = {
    "context": {
        "user": {
            "userId": "amzn1.ask.account"
        },
        "device": {
            "deviceId": "amzn1.ask.device",
            "supportedInterfaces": {
                "AudioPlayer": {},
                "Display": {
                    "markupVersion": "1.0",
                    "templateVersion": "1.0"
                }
            }
        }
    },
    "request": {
        "dialogState": None,
        "intent": {
            "name": "SurveyIntent",
            "slots": {
                "BonusOne": {
                    "name": "BonusOne",

                },
                "BonusOneWait": {
                    "name": "BonusOneWait",

                },
                "BonusThree": {
                    "name": "BonusThree",

                },
                "BonusThreeWait": {
                    "name": "BonusThreeWait",

                },
                "BonusTwo": {
                    "name": "BonusTwo",

                },
                "BonusTwoWait": {
                    "name": "BonusTwoWait",

                },
                "Eight": {
                    "name": "Eight",

                },
                "Eleven": {
                    "name": "Eleven",

                },
                "Fifteen": {
                    "name": "Fifteen",

                },
                "Five": {
                    "name": "Five",

                },
                "Four": {
                    "name": "Four",

                },
                "Fourteen": {
                    "name": "Fourteen",

                },
                "Nine": {
                    "name": "Nine",

                },
                "One": {
                    "name": "One",

                },
                "Seven": {
                    "name": "Seven",

                },
                "Six": {
                    "name": "Six",

                },
                "Sixteen": {
                    "name": "Sixteen",

                },
                "StartSurvey": {
                    "name": "StartSurvey",

                },
                "Ten": {
                    "name": "Ten",

                },
                "Thirteen": {
                    "name": "Thirteen",

                },
                "Three": {
                    "name": "Three",

                },
                "Twelve": {
                    "name": "Twelve",

                },
                "Two": {
                    "name": "Two",

                }
            }
        },
        "locale": "en-US",
        "requestId": "amzn1.echo-api.request",
        "timestamp": "2018-04-26T22:45:12Z",
        "type": "IntentRequest"
    },
    "session": {
        "new": False,
        "sessionId": "amzn1.echo-api.session",
        "application": {
          "applicationId": "amzn1.ask.skill"
        },
        "attributes": {
            "BONUS_COUNT": None,
            "BonusOne": None,
            "BonusTwo": None,
            "COUNT": None,
            "Eight": None,
            "Eleven": None,
            "Fifteen": None,
            "Five": None,
            "Four": None,
            "Fourteen": None,
            "HAMD_SCORE": None,
            "Nine": None,
            "One": None,
            "PREV_QUESTION": None,
            "QUESTION": None,
            "STATE": None,
            "Seven": None,
            "Six": None,
            "Sixteen": None,
            "Ten": None,
            "Thirteen": None,
            "Three": None,
            "Twelve": None,
            "Two": None,
            "Severity": None
        }
    },
    "version": "1.0"
}


def generate_survey(name, dialog_completion, bonus_question, test_case):

    # original_survey_body = general_survey_body
    general_survey_body['request']['dialogState'] = dialog_completion

    # Initialize for start
    if dialog_completion == 'STARTED':
        pass

    # Initialize for in progress
    elif dialog_completion == 'IN_PROGRESS':
        if not bonus_question and name.split('_')[-1] == 'pass':

            general_survey_body['session']['attributes']["COUNT"] = 2
            general_survey_body['session']['attributes']['QUESTION'] = 'Two'
            general_survey_body['session']['attributes']["HAMD_SCORE"] = 1

            general_survey_body["request"]["intent"]["slots"]["StartSurvey"]["value"] = 'yes'
            general_survey_body['request']['intent']['slots']['Two']["value"] = 1

        elif not bonus_question and name.split('_')[-1] == 'fail':
            general_survey_body['session']['attributes']["COUNT"] = 3
            general_survey_body['session']['attributes']['QUESTION'] = 'Three'

            general_survey_body["request"]["intent"]["slots"]["StartSurvey"]["value"] = 'yes'
            general_survey_body['request']['intent']['slots']['Three']["value"] = '?'

        elif bonus_question and name.split('_')[-1] == 'go':
            general_survey_body['session']['attributes']["COUNT"] = 16
            general_survey_body['session']['attributes']['QUESTION'] = 'BonusOne'
            general_survey_body['session']['attributes']['PREV_QUESTION'] = 'BonusOne'
            general_survey_body['session']['attributes']['BonusOneWait'] = 'yes'
            general_survey_body['session']['attributes']['BONUS_COUNT'] = 1

            general_survey_body["request"]["intent"]["slots"]["StartSurvey"]["value"] = 'yes'
            general_survey_body['request']['intent']['slots']['BonusOneWait']["value"] = 'yes'
            general_survey_body['request']['intent']['slots']['BonusOne']["value"] = 'happy great awesome'
        elif bonus_question and name.split('_')[-1] == 'wait':
            general_survey_body['session']['attributes']["COUNT"] = 16
            general_survey_body['session']['attributes']['QUESTION'] = 'BonusOne'
            general_survey_body['session']['attributes']['PREV_QUESTION'] = 'BonusOne'
            general_survey_body['session']['attributes']['BONUS_COUNT'] = 1

            general_survey_body["request"]["intent"]["slots"]["StartSurvey"]["value"] = 'yes'
            general_survey_body['request']['intent']['slots']['BonusOneWait']["value"] = 'no'

    # Initialize for completed
    elif dialog_completion == 'COMPLETED':
        if test_case.lower() == 'normal':
            four_question_val = 0
            two_question_val = 0
            suicide_question_val = 0
            hamd_score = 0
            bonus_val = "happy great awesome"
        elif test_case.lower() == 'mild':
            two_question_val = 1
            four_question_val = 0
            suicide_question_val = 1
            bonus_val = "terrible horrible bad"
            hamd_score = 8
        elif test_case.lower() == 'moderate':
            four_question_val = 1
            two_question_val = 1
            suicide_question_val = 1
            bonus_val = "happy great awesome"
            hamd_score = 16
        elif test_case.lower() == 'severe':
            four_question_val = 1
            two_question_val = 1
            suicide_question_val = 4
            bonus_val = "terrible horrible bad "
            hamd_score = 19
        elif test_case.lower() == 'very severe':
            four_question_val = 4
            two_question_val = 2
            suicide_question_val = 4
            bonus_val = "terrible horrible bad"
            hamd_score = 48

        request_intent_slots = general_survey_body['request']['intent']['slots']
        for intent_slot in request_intent_slots:
            if intent_slot in LIST_OF_QUESTIONS_FOUR:
                general_survey_body['request']['intent']['slots'][intent_slot]['value'] = str(four_question_val)
            elif intent_slot == SUICIDE_QUESTION:
                general_survey_body['request']['intent']['slots'][intent_slot]['value'] = str(suicide_question_val)
            elif intent_slot in LIST_OF_QUESTIONS_TWO:
                general_survey_body['request']['intent']['slots'][intent_slot]['value'] = str(two_question_val)
            elif intent_slot in LIST_OF_BONUS:
                general_survey_body['request']['intent']['slots'][intent_slot]['value'] = bonus_val
            elif intent_slot in LIST_OF_BONUS_WAIT or intent_slot == 'StartSurvey':
                general_survey_body['request']['intent']['slots'][intent_slot]['value'] = "yes"
        sess_attr_list = general_survey_body['session']['attributes']
        for sess_attr in sess_attr_list:
            if sess_attr in LIST_OF_QUESTIONS_FOUR:
                general_survey_body['session']['attributes'][sess_attr] = str(four_question_val)
            elif sess_attr == SUICIDE_QUESTION:
                general_survey_body['session']['attributes'][sess_attr] = str(suicide_question_val)
            elif sess_attr in LIST_OF_QUESTIONS_TWO:
                general_survey_body['session']['attributes'][sess_attr] = str(two_question_val)
            elif sess_attr in LIST_OF_BONUS:
                general_survey_body['session']['attributes'][sess_attr] = bonus_val
            elif sess_attr in LIST_OF_BONUS_WAIT:
                general_survey_body['session']['attributes'][sess_attr] = "yes"
            elif sess_attr == 'QUESTION':
                general_survey_body['session']['attributes'][sess_attr] = "BonusThree"
            elif sess_attr == 'HAMD_SCORE':
                general_survey_body['session']['attributes'][sess_attr] = hamd_score

    return general_survey_body
