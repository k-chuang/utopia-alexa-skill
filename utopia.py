'''
Utopia is an Alexa skill programmed in Python to help with depression.

Disclaimer: This skill is not meant to be a cure for depression, but more of an aid for depression.

Author: Kevin Chuang
Date: March 8, 2018

'''

import os
from flask import Flask, json, render_template, jsonify
from flask_ask import Ask, request, session, question, context, statement, delegate, convert_errors, elicit_slot
import requests
import json
import logging
from num2words import num2words
import geocoder
import re
from textblob import TextBlob
import yaml
import random
from random import randint
from bs4 import BeautifulSoup, Tag, NavigableString
from datetime import datetime

##################################
# App & Environment Initialization
##################################

app = Flask(__name__)
ask = Ask(app, "/")
logger = logging.getLogger('flask_ask').setLevel(logging.DEBUG)


##############################
# On Launch
##############################
# When app is first launched, user will wind up here with this @ask.launch decorator
@ask.launch
def start_skill():
    welcome_message = render_template('initial_welcome')
    welcome_reprompt = render_template('initial_welcome_reprompt')
    return question(welcome_message).reprompt(welcome_reprompt)


##########################
# Custom Intents
##########################
@ask.intent("NameIntent",
            mapping= {'firstname': 'FirstName'})
def get_name(firstname):
    name_message = render_template("official_welcome", firstname=firstname)
    name_message_reprompt = render_template("official_welcome_reprompt")
    session.attributes["firstname"] = firstname
    session.attributes_encoder = json.JSONEncoder
    # DEBUG
    # with open('session.json', 'w') as outfile:
    #     json.dump(session.attributes, outfile, indent=4, sort_keys=True)
    return question(name_message).reprompt(name_message_reprompt)


@ask.intent("SurveyIntent")
def start_survey():

    dialog_state = get_dialog_state()
    session.attributes_encoder = json.JSONEncoder

    if dialog_state == "STARTED":
        session.attributes["COUNT"] = 0
        session.attributes["BONUS_COUNT"] = 0
        session.attributes["HAMD_SCORE"] = 0
        session.attributes["QUESTION"] = 'One'
        session.attributes["PREV_QUESTION"] = 'BonusOne'
        session.attributes["STATE"] = 'Survey'
        return delegate()
    elif dialog_state == "IN_PROGRESS":
        # If do not want to continue survey:
        if request["intent"]["slots"]["StartSurvey"]["value"] == 'no':
            return stop()

        survey_question = session.attributes["QUESTION"]
        # For bonus question
        previous_question = session.attributes["PREV_QUESTION"]
        # If regular survey questions
        if not re.match("Bonus", survey_question):
            if 'value' in request["intent"]["slots"][survey_question]:

                if str(request["intent"]["slots"][survey_question]["value"]) not in ('0', '1', '2', '3', '4'):
                    reprompt_answer = render_template("reprompt_survey")
                    return elicit_slot(survey_question, reprompt_answer)

                # Record answer for question
                session.attributes[survey_question] = int(request["intent"]["slots"][survey_question]["value"])
                # Add each score to get total survey score
                session.attributes["HAMD_SCORE"] += int(request["intent"]["slots"][survey_question]["value"])
        # If Bonus Questions
        else:
            survey_wait = survey_question + "Wait"
            bonus_wait = request["intent"]["slots"][survey_wait]

            # If bonus wait question
            if 'value' in bonus_wait:
                if request["intent"]["slots"][survey_wait]["value"] == 'no':
                    if session.attributes["BONUS_COUNT"] > 0:
                        session.attributes["BONUS_COUNT"] -= 1
                    bonus_question = render_template(survey_wait)
                    return elicit_slot(survey_wait, bonus_question)

            if previous_question in request["intent"]["slots"]:
                # If actual bonus question
                bonus_question = request["intent"]["slots"][previous_question]
                if 'value' in bonus_question:
                    words = request["intent"]["slots"][previous_question]["value"]
                    session.attributes[previous_question] = words

        # Increment question count for both regular and bonus questions
        if session.attributes["COUNT"] < 16:
            session.attributes["COUNT"] += 1
            survey_question = num2words(session.attributes["COUNT"]).capitalize()
        elif session.attributes["BONUS_COUNT"] < 3:
            previous_question = "Bonus" + num2words(session.attributes["BONUS_COUNT"]).capitalize()
            session.attributes["BONUS_COUNT"] += 1
            survey_question = "Bonus" + num2words(session.attributes["BONUS_COUNT"]).capitalize()

        session.attributes["QUESTION"] = survey_question
        session.attributes["PREV_QUESTION"] = previous_question

        return delegate()
    elif dialog_state == "COMPLETED":
        # Get last bonus question answer
        last_question = session.attributes.get("QUESTION")
        session.attributes[last_question] = \
            request["intent"]["slots"][last_question]["value"]
        session.attributes['STATE'] = 'SurveyDone'

    # Bonus section calculation of score using sentiment analysis
    bonus_list = ['BonusOne', 'BonusTwo', 'BonusThree']
    for bonus in bonus_list:
        words = session.attributes[bonus]
        word_list = words.split()
        bonus_score = 0
        for word in word_list:
            analysis = TextBlob(word)
            bonus_score += analysis.sentiment.polarity

        # Normalize scores based on three adjectives
        bonus_score = bonus_score / 3

        # Increase score based on negative sentiment analysis of words in bonus section
        if bonus_score < 0:
            session.attributes["HAMD_SCORE"] += (2 / 3) * (-bonus_score)

    score = round(float(session.attributes["HAMD_SCORE"]), 2)

    session.attributes["HAMD_SCORE"] = score

    if score >= 0 and score <= 7:
        # Normal
        score_message = render_template('normal', score=score)
        session.attributes['Severity'] = 'normal'
    elif score > 7 and score <= 13:
        # Mild Depression
        score_message = render_template('mild', score=score)
        session.attributes['Severity'] = 'mild'
    elif score > 13 and score <= 18:
        # Moderate Depression
        score_message = render_template('moderate', score=score)
        session.attributes['Severity'] = 'moderate'
    elif score > 18 and score <= 22:
        # Severe Depression (Will categorize in the same category as very severe depression)
        score_message = render_template('severe', score=score)
        session.attributes['Severity'] = 'severe'
    elif score > 22:
        # Very Severe Depression
        score_message = render_template('very_severe', score=score)
        session.attributes['Severity'] = 'very severe'

    else:
        score_message = 'Sorry, I was unable to calculate your Hamilton survey score. Please try again later.'

    return question(score_message)


@ask.intent("GetQuoteTypeIntent")
def get_quote_type():
    dialog_state = get_dialog_state()
    session.attributes_encoder = json.JSONEncoder
    if dialog_state == 'STARTED':
        session.attributes['Category'] = 'positive'
        return delegate()
    elif dialog_state == 'IN_PROGRESS':
        session.attributes['Category'] = request['intent']['slots']['Category']['value']
        return delegate()
    elif dialog_state == 'COMPLETED':
        session.attributes['Category'] = request['intent']['slots']['Category']['value']
        return give_quote(category=session.attributes['Category'])


@ask.intent("QuoteIntent")
def give_quote(category='positive'):
    session.attributes["STATE"] = 'GetQuoteType'
    try:
        if category != request['intent']['slots']['Category']['value']:
            category = request['intent']['slots']['Category']['value']
            session.attributes['Category'] = category
    except KeyError:
        category = session.attributes['Category']

    zip_quotes = get_brainy_quotes(category)
    quotes = list(zip_quotes)
    session.attributes['Quotes'] = quotes
    quote_index = randint(1, len(quotes))
    rand_quote = quotes[quote_index][0]
    rand_quote_picture = quotes[quote_index][1]

    quote_msg = render_template('quote', category=category, quote=rand_quote)
    return question(quote_msg).standard_card(title='A {0} quote for you!'.format(category),
                                             text=rand_quote,
                                             small_image_url=rand_quote_picture,
                                             large_image_url=rand_quote_picture)


@ask.intent('SuicideHotLine')
def provide_hot_line():
    session.attributes["STATE"] = 'SuicideHotLine'
    suicide_statement = render_template('suicide')
    return statement(suicide_statement).standard_card(title='National Suicide Prevention Lifeline',
                                                      text='Call Now at 1-800-273-8255 ',
                                                      large_image_url='https://upload.wikimedia.org/wikipedia/commons/'
                                                                      'thumb/4/41/Lifelinelogo.svg/1200px-Lifelinelogo'
                                                                      '.svg.png')


@ask.intent('RecommendTherapist')
def recommend_therapist(address):
    '''
    Using location and Google Maps & Places API, find nearby therapists and give contact information and open hours.
    :return:
    '''
    session.attributes["STATE"] = 'RecommendTherapist'
    query = "therapist OR psychiatrist"
    try:
        address = get_location()
    # address is not successfully found, raise ValueError and catch it here
    except ValueError as er:
        return statement(str(er)).consent_card("read::alexa:device:all:address")

    api_key = os.environ['GOOGLE_API_KEY']
    kwargs_geocode = {'key': api_key}
    g = geocoder.google(address, **kwargs_geocode)
    coordinates = g.latlng
    location = "{},{}".format(coordinates[0], coordinates[1])

    query_place_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?location={}&query={}&key={}"\
        .format(location, query, api_key)

    queried_places_request = requests.get(query_place_url)
    if queried_places_request.status_code == 200:
        therapist_places = queried_places_request.json()
    else:
        return statement("Sorry, I'm having trouble doing that right now. Please try again later.")

    results = therapist_places['results']
    currently_opened = False
    availability = 'unknown'
    # find first open place
    for place in results:
        try:
            if place['opening_hours']['open_now'] is True:
                place_id = place['place_id']
                name = place['name']
                therapist_address = place['formatted_address']
                currently_opened = True
                availability = 'available'
                break
        except KeyError:
            continue

    # If no open places, find closest place
    if not currently_opened:
        place_id = results[0]['place_id']
        name = results[0]['name']
        therapist_address = results[0]['formatted_address']
        availability = 'not available'

    detailed_url = "https://maps.googleapis.com/maps/api/place/details/json?placeid={}&key={}".format(place_id, api_key)
    detailed_place_request = requests.get(detailed_url)
    if detailed_place_request.status_code == 200:
        detailed_place = detailed_place_request.json()

        phone = detailed_place['result']['formatted_phone_number']
        hours_list = detailed_place['result']['opening_hours']['weekday_text']
        hours_message = "\n ".join(hours_list)
        try:
            photo_reference = detailed_place['result']['photos'][0]['photo_reference']
            max_width = 1200
            max_height = 800
            place_photo_url = "https://maps.googleapis.com/maps/api/place/photo?photoreference={}&maxheight={}&maxwidth={}&key={}"\
                .format(photo_reference, max_height, max_width, api_key)
            photo_request = requests.get(place_photo_url)
            if photo_request.status_code == 200:
                photo = photo_request.request.url
            else:
                photo = "https://images.unsplash.com/photo-1489533119213-66a5cd877091?ixlib=rb-0.3.5&ixid" \
                        "=eyJhcHBfaWQiOjEyMDd9&s=7c006c52fd09caf4e97536de8fcf5067&auto=format&fit=crop&w=1051&q=80"
        # If no photos in the Google Place, set to default photo
        except KeyError:
            photo = "https://images.unsplash.com/photo-1489533119213-66a5cd877091?ixlib=rb-0.3.5&ixid" \
                    "=eyJhcHBfaWQiOjEyMDd9&s=7c006c52fd09caf4e97536de8fcf5067&auto=format&fit=crop&w=1051&q=80"

        message = render_template('therapist', availability=availability, name=name, phone=phone)
        card = "Name: {} \n Address: {} \n Phone: {} \n Availability: \n {}".\
            format(name, therapist_address, phone, hours_message)
        return statement(message).standard_card(title="I've found a nearby therapist that you can talk to",
                                                text=card,
                                                small_image_url=photo,
                                                large_image_url=photo)
    else:
        return statement("Sorry, I'm having trouble doing that right now. Please try again later.")


@ask.intent('GiveAdvice')
def give_advice():
    session.attributes["STATE"] = 'GiveAdvice'

    with open("templates.yaml", 'r') as stream:
        out = yaml.load(stream)
        all_advice = out['advice_list']
    advice = random.choice(all_advice) + '<break time="1s"/> '
    advice_message = render_template('advice_message') + advice + 'I hope that was able to help you. If you wish to ' \
                                                                  'hear more ideas about what you can do to improve ' \
                                                                  'your mood, say more ideas. For other features, ' \
                                                                  'say help. Otherwise, say stop to stop. '
    advice_message_ssml = '<speak> ' + advice_message + ' </speak>'
    return question(advice_message_ssml)

##############################
# Overriding Required Intents
##############################


@ask.intent('AMAZON.HelpIntent')
def help():
    help_text = render_template('help')
    return question(help_text)


@ask.intent('AMAZON.StopIntent')
def stop():
    try:
        firstname = session.attributes['firstname']
    except KeyError:
        firstname = 'my friend'
    bye_message = render_template("bye", firstname=firstname)
    return statement(bye_message)


@ask.session_ended
def session_ended():
    return "{}", 200


##############################
# Helper Functions
##############################
def get_brainy_quotes(category, number_of_quotes=25):
    popular_choice = ['motivational', 'inspirational',
                      'life', 'smile', 'family', 'positive',
                      'friendship', 'success', 'happiness', 'love']

    url = "http://www.brainyquote.com/quotes/topics/topic_" + category + ".html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    quotes = []
    src_picture = []
    for quote in soup.find_all('a', {'title': 'view quote'}):
        # if isinstance(quote.contents[0], NavigableString):
        #
        #     quotes.append(str(quote.contents[0]).replace('-', 'By'))
        if isinstance(quote.contents[0], Tag):

            src_picture.append("https://www.brainyquote.com/" + quote.contents[0].attrs['src'])
            quotes.append(quote.contents[0].attrs['alt'].replace('-', 'By'))

    result = zip(quotes, src_picture)
    # result = quotes[:number_of_quotes]
    return result


def get_location():
    '''
    This function will get the zip code of the user if location is permitted.
    :return: a formatted string with address of user
    '''
    URL = "https://api.amazonalexa.com/v1/devices/{}/settings" \
          "/address".format(context.System.device.deviceId)
    TOKEN = context.System.user.permissions.consentToken
    HEADER = {'Accept': 'application/json',
              'Authorization': 'Bearer {}'.format(TOKEN)}
    r = requests.get(URL, headers=HEADER)
    if r.status_code == 200:
        alexa_location = r.json()
    else:
        raise ValueError('Sorry, but your location could not be found. Please enable it by allowing access to '
                         'your location via the Alexa app, and try again to fully utilize this feature. Thank you.')

    address = "{} {}".format(alexa_location["addressLine1"],
                             alexa_location["city"])
    return address


def get_dialog_state():
    return session['dialogState']


##############################
# Program Entry
##############################

if __name__ == '__main__':

    app.config['ASK_PRETTY_DEBUG_LOGS'] = True

    app.run(debug=True)
