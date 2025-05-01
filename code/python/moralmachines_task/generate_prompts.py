import random
import moralmachines_task.prompt_templates as prompt_templates
from moralmachines_task.generate_moral_machine_scenarios import generate_moral_machine_scenarios
from moralmachines_task.generate_moral_machine_scenarios import assign_barrier_crossing_conditions
from moralmachines_task.config import scenario_dimension_group_types
from google.cloud import translate_v2 as translate

translate_client = translate.Client()

# Expect a dict of item: count
# For example:
# {
#   "young boy": 2,
#   "old female cat": 1,
# }
def generate_item_prompt(items):
    return ", ".join([f"{num} {item}" for item,num in items.items()])


TEMPLATES = {
    "en": prompt_templates.EN_PROMPT_TEMPLATE,
    "fr": prompt_templates.FR_PROMPT_TEMPLATE,
    "ja": prompt_templates.JP_PROMPT_TEMPLATE,
    "zh": prompt_templates.CN_PROMPT_TEMPLATE,
    "es": prompt_templates.ES_PROMPT_TEMPLATE,
    "tw": prompt_templates.TW_PROMPT_TEMPLATE,
}


class TrolleyProblem():

    def __init__(self, dimension=None, toggle_passenger=None, toggle_crossing_signal=None):
        """
        Args:
            dimension: str, optional
            toggle_passenger: bool, optional --> Toggles whether the task is not PedPed (True --> PasPed or PedPas)
            toggle_crossing_signal: bool, optional --> Toggles whether the task factors legality (False --> NA)
        """
        self.dimension = dimension if dimension is not None else random.choice(scenario_dimension_group_types.keys())
        # Restrict contrasts of PedPed with CrossingSignal if provided
        if toggle_passenger:
            self.is_in_car = (1, 0)
            if random.random() < 0.5:
                self.is_in_car = (0, 1)
            self.is_law = (0, 0)

        if toggle_crossing_signal and (toggle_passenger is None or not toggle_passenger):
            self.is_law = (1, 2)
            if random.random() < 0.5:
                self.is_law = (2, 1)
            self.is_in_car = (0, 0)

        # Default to random if not specified
        if toggle_passenger is None and toggle_crossing_signal is None:
            self.is_in_car, self.is_law = assign_barrier_crossing_conditions()
        print("Generating Trolley Problem with config: ", self.__dict__)
        self.system_content, self.user_content, self.scenario_info = generate_moral_machine_scenarios(
            scenario_dimension=self.dimension,
            is_law=self.is_law,
            is_in_car=self.is_in_car,
        )
        self.change_lane_items = self.scenario_info["count_dict_1"]
        self.stay_lane_items = self.scenario_info["count_dict_2"]
        self.change_prompt = self.scenario_info["case_1_description"]
        self.stay_prompt = self.scenario_info["case_2_description"]
        self.case_1_code = self.scenario_info["case_1_code"]
        self.case_2_code = self.scenario_info["case_2_code"]
        self.prompt = None

    def prepare_prompt(self, language="en"):
        self.language = language
        prompt_template = TEMPLATES[language]
        if language == "tw": # Map to chinese-traditional
            language = "zh-TW"
        # Reset so source language is always 'en'
        self.change_prompt = self.scenario_info["case_1_description"]
        self.stay_prompt = self.scenario_info["case_2_description"]
        if language != "en":
            result = translate_client.translate(self.change_prompt, source_language="en", target_language=language)
            self.change_prompt = result["translatedText"]
            result = translate_client.translate(self.stay_prompt, source_language="en", target_language=language)
            self.stay_prompt = result["translatedText"]
        self.prompt = (
            prompt_template
            .replace("%change_lane_items%", self.change_prompt)
            .replace("%stay_lane_items%", self.stay_prompt)
        )
    
    def get_prompt(self):
        if not self.prompt:
            raise Exception("Prompt not prepared. Please call prepare_prompt() with a specified language first.")
        return self.prompt

    def encode_items(self, items: dict):
        return ".".join([f"{num}{item}" for item, num in items.items()])
    
    def get_code(self):
        # Encode change lane items
        coded_change_items = self.encode_items(self.change_lane_items)
        # Encode stay lane items
        coded_stay_items = self.encode_items(self.stay_lane_items)
        # Construct a 'hash' of this problem
        return f"{self.language},{self.case_1_code},{coded_change_items}|{self.language},{self.case_2_code},{coded_stay_items}"


if __name__ == "__main__":
    prob1 = TrolleyProblem(dimension="age")
    prob1.prepare_prompt(language="tw")
    print(prob1.get_prompt())
    print(prob1.get_code())

    prob2 = TrolleyProblem(dimension="species", toggle_crossing_signal=True)
    prob2.prepare_prompt(language="en")
    print(prob2.get_prompt())
    print(prob2.get_code())
