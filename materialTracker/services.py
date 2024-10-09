import requests
from .models import AggregatedContent
from decouple import config

class StrapiAPI:
    def __init__(self):
        self.url = config('STRAPI_URL')
        self.access_token = config('STRAPI_ACCESS_TOKEN')
        self.headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

    def get_content(self):
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            content = data.get('data', [])
            formatted_data = []
            locale_content = {}  

            for item in content:
                custom_type = item.get('custom_type')
                locale = item.get('locale')
                print(f"Processing {custom_type}")
                
                locale_content.setdefault(locale, {})

                if custom_type == "form_questions":
                    content_item = {
                        "pageId": item.get("page_id"),
                        "pageTitle": item.get("page_title"),
                        "lastUpdated": item.get("updatedAt"),
                        
                        "customType": custom_type,
                        "pageContent": {
                            "list": []
                        }
                    }

                    for component in item.get("dynamic_zone", []):
                        component_data = {
                            "key": component.get("Key"),
                            "label": component.get("Label"),
                            "options": component.get("Options"),
                            "category": component.get("Category"),
                            "helpText": component.get("HelpText"),
                            "required": component.get("Required"),
                            "placeholder": component.get("Placeholder"),
                            "component": component.get("__component"),
                            "questionType": component.get("QuestionType"),
                            "displayQuestion": component.get("DisplayQuestion"),
                            "optionTranslations": component.get("OptionTranslations"),
                        }

                        content_item["pageContent"]["list"].append(component_data)

                        if "repeatable_zone" in component:
                            for repeatable_item in component["repeatable_zone"]:
                                repeatable_data = {
                                    "key": repeatable_item.get('key'),
                                    "value": repeatable_item.get('value'),
                                    "id": repeatable_item.get("id")
                                }
                                content_item["pageContent"]["list"].append(repeatable_data)

                    locale_content[locale][item.get("page_id")] = content_item

            for item in content:
                formatted_data.append({
                    "id": item.get("id"),
                    "deleted": False,
                    "createdAt": item.get("createdAt"),
                    "updatedAt": item.get("updatedAt"),
                    "deletedAt": item.get("deletedAt"),
                    "createdBy": item.get("createdBy"),
                    "updatedBy": item.get("updatedBy"),
                    "deletedBy": item.get("deletedBy"),
                    "content": locale_content
                })

            self.save_to_database(formatted_data)
            return formatted_data

        except requests.RequestException as e:
            print(f"Error fetching data from Strapi API: {e}")
            return None

    def save_to_database(self, aggregated_data):
        for data_item in aggregated_data:
            for locale, content in data_item["content"].items():
                for content_item in content.values():
                    AggregatedContent.objects.create(
                        data=content_item
                    )
        print("Data saved to the database.")
