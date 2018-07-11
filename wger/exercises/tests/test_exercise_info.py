from wger.core.tests.base_testcase import WorkoutManagerTestCase


class ExerciseInfoTestCase(WorkoutManagerTestCase):
    '''
    Test Exercise Info Endpoint
    '''

    def test_exercise_info(self):
        '''
        Test endpoint returns exercise infomation
        '''
        endpoint = "/api/v2/exerciseInfo/"

        res = self.client.get(endpoint)

        self.assertEqual(res.status_code, 200)

        self.assertIn("license_author", str(res.data))

        self.assertIn("license", str(res.data))

        self.assertIn("category", str(res.data))

        self.assertIn("language", str(res.data))

        self.assertIn("muscles", str(res.data))

        self.assertIn("muscles_secondary", str(res.data))

        self.assertIn("equipment", str(res.data))

        self.assertIn("image", str(res.data))
