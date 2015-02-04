""" Google Document integration tests """
from xblockutils.base_test import SeleniumBaseTest


class GoogleDocumentBaseTest(SeleniumBaseTest):  # pylint: disable=too-many-ancestors
    """ Test class for google document """
    module_name = __name__
    default_css_selector = 'div.google-docs-xblock-wrapper'

    def test_document_publish_event(self):
        """ Tests whether the publish event for document was triggered """
        document = self.go_to_page('Document')
        load_event_complete = document.find_element_by_css_selector('.load_event_complete')
        self.assertEqual(
            load_event_complete.get_attribute('value'),
            "I've published the event that indicates that the load has completed"
        )

    def test_image_publish_event(self):
        """ Tests whether the publish event for image was triggered """
        image = self.go_to_page('Image')
        load_event_complete = image.find_element_by_css_selector('.load_event_complete')
        self.assertEqual(
            load_event_complete.get_attribute('value'),
            "I've published the event that indicates that the load has completed"
        )
