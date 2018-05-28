import utopia
from utopia import app
import unittest
import json
import os
import tests.request_json as request_json
from nose_parameterized import parameterized
from mock import patch
import pytest


class TestUtopiaApp(unittest.TestCase):

    def setUp(self):
        '''Test Suite set up by disabling ASK_VERIFY_REQUESTS and enabling testing to true'''
        app.config['ASK_VERIFY_REQUESTS'] = False
        app.config['SECRET_KEY'] = 'SUPERSECRETKEYBUTNOTREALLY!'
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.app.testing = True
        os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    def tearDown(self):
        """ Test Suite Tear down."""
        os.chdir(os.path.dirname(__file__))

    def test_utopia_launch(self):
        """Test Launch Intent."""
        response = self.app.post('/', data=json.dumps(request_json.launch_body))
        self.assertEqual(200, response.status_code)
        self.assertTrue(b'Welcome to Utopia!' in response.data)

    def test_utopia_session_ended(self):
        """Test Session End."""
        response = self.app.post('/', data=json.dumps(request_json.sess_end_body))
        self.assertEqual(200, response.status_code)

    @parameterized.expand([
        ('dialog_started', 'STARTED', None, None, None, None),
        ('dialog_in_progress_regular_question_pass', 'IN_PROGRESS', False, None, None, None),
        ('dialog_in_progress_regular_question_fail', 'IN_PROGRESS', False, None, None, None),
        ('dialog_in_progress_bonus_question_wait', 'IN_PROGRESS', True, None, None, None),
        ('dialog_in_progress_bonus_question_go', 'IN_PROGRESS', True, None, None, None),
        ('dialog_completed_normal_severity', 'COMPLETED', None, 'normal', 0, 7),
        ('dialog_completed_mild_severity', 'COMPLETED', None, 'mild', 8, 13),
        ('dialog_completed_moderate_severity', 'COMPLETED', None, 'moderate', 14, 18),
        ('dialog_completed_severe_severity', 'COMPLETED', None, 'severe', 19, 22),
        ('dialog_completed_very_severe_severity', 'COMPLETED', None, 'very severe', 23, 50),
    ])
    def test_survey_intent(self, name, dialog_state, bonus_question, severity, lower_limit, upper_limit):
        """Test SurveyIntent with different test cases"""
        response = self.app.post('/',
                                 data=json.dumps(request_json.generate_survey(name, dialog_state, bonus_question, severity)))
        self.assertEqual(200, response.status_code)
        data = json.loads(response.data.decode('utf-8'))
        if dialog_state == 'STARTED':
            self.assertEqual('One', data['sessionAttributes']['QUESTION'])
            self.assertEqual(0, data['sessionAttributes']['HAMD_SCORE'])
            self.assertEqual(0, data['sessionAttributes']['COUNT'])
            self.assertEqual(0, data['sessionAttributes']['BONUS_COUNT'])
            self.assertEqual('BonusOne', data['sessionAttributes']['PREV_QUESTION'])
            self.assertFalse(data['response']['shouldEndSession'])
        elif dialog_state == 'IN_PROGRESS':
            if not bonus_question and name.split('_')[-1] == 'pass':
                self.assertFalse(data['response']['shouldEndSession'])
                self.assertEqual('Three', data['sessionAttributes']['QUESTION'])
                self.assertEqual(2, data['sessionAttributes']['HAMD_SCORE'])
                self.assertEqual(3, data['sessionAttributes']['COUNT'])
            elif not bonus_question and name.split('_')[-1] == 'fail':
                self.assertEqual('Dialog.ElicitSlot', data['response']['directives'][0]['type'])
                self.assertFalse(data['response']['shouldEndSession'])
                self.assertTrue('Please say a number in the specified range.' in
                                data['response']['outputSpeech']['text'])
            elif bonus_question and name.split('_')[-1] == 'go':
                self.assertEqual('happy great awesome', data['sessionAttributes']['BonusOne'])
                self.assertEqual('BonusTwo', data['sessionAttributes']['QUESTION'])
            elif bonus_question and name.split('_')[-1] == 'wait':
                pass
        elif dialog_state == 'COMPLETED':
            self.assertFalse(data['response']['shouldEndSession'])
            self.assertEqual(severity, data['sessionAttributes']['Severity'])
            self.assertTrue(lower_limit <= data['sessionAttributes']['HAMD_SCORE'] <= upper_limit)

    # def test_name_intent(self):
    #     """Test NameIntent"""
    #     response = self.app.post('/', data=json.dumps(request_json.name_intent_body))
    #     self.assertEqual(200, response.status_code)
    #     data = json.loads(response.data.decode('utf-8'))
    #     self.assertEqual('Kevin', data['sessionAttributes']['firstname'])

    def test_get_brainy_quotes(self):
        """Testing helper function get_brainy_quotes"""
        zip_quotes = utopia.get_brainy_quotes(category='positive', number_of_quotes=50)
        quotes = list(zip_quotes)
        self.assertIsNotNone(quotes)
        self.assertNotEqual(len(quotes), 0)

    def test_give_poem_intent(self):
        """Test PoemIntent"""
        response = self.app.post('/', data=json.dumps(request_json.give_poem_body))
        self.assertEqual(200, response.status_code)
        data = json.loads(response.data.decode('utf-8'))
        response = data['response']
        self.assertTrue('directives' in response)
        self.assertIsNotNone(response['directives'][0]['audioItem']['stream']['token'])
        self.assertEqual('AudioPlayer.Play', response['directives'][0]['type'])
        self.assertEqual(0, response['directives'][0]['audioItem']['stream']['offsetInMilliseconds'])
        self.assertTrue('Welcome to the Poem feature!' in response['outputSpeech']['ssml'])
        self.assertTrue(all(card_attribute in response['card'] for card_attribute in ['content', 'title', 'type']))

    def test_suicide_hotline_intent(self):
        """Test SuicideHotLine Intent."""
        response = self.app.post('/', data=json.dumps(request_json.suicide_hotline_body))
        self.assertEqual(200, response.status_code)
        data = json.loads(response.data.decode('utf-8'))

        self.assertTrue('Thank you for being honest with me. Please don\'t hurt yourself or anyone else.' in
                        data['response']['outputSpeech']['text'])

    def test_recommend_therapist_intent_no_address_provided(self):
        """Test RecommendTherapist Intent"""
        response = self.app.post('/', data=json.dumps(request_json.recommend_therapist_body))
        self.assertEqual(200, response.status_code)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual('AskForPermissionsConsent', data['response']['card']['type'])
        self.assertEqual('read::alexa:device:all:address', data['response']['card']['permissions'][0])

    @patch('utopia.get_location', return_value='374 Mission Rock St, San Francisco, CA 94158')
    def test_recommend_therapist_intent_address_mocked_open_places(self, mock_get_location):
        response = self.app.post('/', data=json.dumps(request_json.recommend_therapist_body))
        self.assertEqual(200, response.status_code)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual('I\'ve found a nearby therapist that you can talk to', data['response']['card']['title'])
        self.assertTrue('I\'ve found a therapist near you.' in data['response']['outputSpeech']['text'])
        self.assertEqual('RecommendTherapist', data['sessionAttributes']['STATE'])

    @pytest.mark.skip(reason="Inconsistent results based on map location and time")
    @patch('utopia.get_location', return_value='158 Bradford St, Sonora, CA 95370')
    def test_recommend_therapist_intent_address_mocked_closed_places(self, mock_get_location):
        response = self.app.post('/', data=json.dumps(request_json.recommend_therapist_body))
        self.assertEqual(200, response.status_code)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual('I\'ve found a nearby therapist that you can talk to', data['response']['card']['title'])
        self.assertTrue('I\'ve found a therapist near you.' in data['response']['outputSpeech']['text'])
        self.assertEqual('RecommendTherapist', data['sessionAttributes']['STATE'])

    def test_get_quote_type_intent(self):
        """Test GetQuoteTypeIntent."""
        response = self.app.post('/', data=json.dumps(request_json.get_quote_type_completed_body))
        self.assertEqual(200, response.status_code)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual('love', data['sessionAttributes']['Category'])

    def test_give_quote_intent_inspirational_quote(self):
        """Test QuoteIntent inspirational quotes"""
        response = self.app.post('/', data=json.dumps(request_json.give_quote_body))
        self.assertEqual(200, response.status_code)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual('inspirational', data['sessionAttributes']['Category'])

    def test_give_advice_intent(self):
        """Test QuoteIntent."""
        response = self.app.post('/', data=json.dumps(request_json.give_advice_body))
        self.assertEqual(200, response.status_code)

    def test_stop_intent(self):
        """Test Stop Intent."""
        response = self.app.post('/', data=json.dumps(request_json.stop_body))
        self.assertEqual(200, response.status_code)

    def test_help_intent(self):
        """Test Help Intent."""
        response = self.app.post('/', data=json.dumps(request_json.help_body))
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
