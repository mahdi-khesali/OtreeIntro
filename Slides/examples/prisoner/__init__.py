from otree.api import *


doc = """
This is a one-shot "Prisoner's Dilemma". Two players are asked separately
whether they want to cooperate or defect. Their choices directly determine the
payoffs.
"""


class C(BaseConstants):
    NAME_IN_URL = 'prisoner'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    PAYOFF_A = cu(300)
    PAYOFF_B = cu(200)
    PAYOFF_C = cu(100)
    PAYOFF_D = cu(0)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    cooperate = models.BooleanField(
        choices=[[True, 'Option C'], [False, 'Option D']],
        doc="""This player's decision""",
        widget=widgets.RadioSelect,
    )

    control_ques_1 = models.IntegerField(
        label='Who chooses first between option C and D?',
        choices=[
            [1, 'You'],
            [2, 'Matched Partner'],
            [3, 'Decisions are made simultaneously'],
        ], widget=widgets.RadioSelect
    )

    control_ques_2 = models.IntegerField(
        label='How many points do you earn if you and your matched partner both choose option D?',
        )

    control_ques_3 = models.IntegerField(
        label='How many points do you earn if you cooperate and your matched partner chooses option D?',
        )
    age = models.IntegerField(initial=None, min=16, max=120, label="How old are you?")

    gender = models.IntegerField(
        choices=[
            [1, "female"],
            [2, "male"],
            [3, "diverse"]
        ], widget=widgets.RadioSelect
        , label="Which gender do you identify with?")

    siblings = models.IntegerField(initial=None, min=0, max=99, label="How many siblings do you have?")

    previous_participation = models.IntegerField(
        choices=[
            [1, "Never"],
            [2, "1 to 2 times"],
            [3, "3 to 5 times"],
            [4, "more often"]
        ], widget=widgets.RadioSelect
        , label="How often have you participated in a behavioral economics experiment?")

    currently_employed = models.IntegerField(
        choices=[
            [1, 'Yes'],
            [2, 'No'],
        ]
        , label="Are you employed in a regular job with more than 10 working hours per week?")

    currently_studying = models.IntegerField(
        choices=[
            [1, 'Yes'],
            [2, 'No'],
        ],
        label="Are you studying?"
    )

    study_semester = models.IntegerField(min=0, max=100,
                                         label="If yes, in which university semester are you currently? (If you are not studying, please enter '0'.)")

    study_course = models.IntegerField(
        choices=[
            [1, "I am not studying"],
            [2, "Cultural Studies"],
            [3, "Linguistics"],
            [4, "Philosophy/Other Humanities"],
            [5, "Education/Educational Sciences"],
            [6, "Law"],
            [7, "Economics"],
            [8, "Social and Political Sciences"],
            [9, "Medicine/Nursing"],
            [10, "Agricultural and Forestry Sciences"],
            [11, "Mathematical and Natural Sciences"],
            [12, "Engineering Sciences"],
            [13, "Art or Music"],
            [14, "Other"],
        ], widget=widgets.RadioSelect
        , label="What are you studying? (If you are not studying, please select 'I am not studying'.):")

# FUNCTIONS
def set_payoffs(group: Group):
    for p in group.get_players():
        set_payoff(p)


def other_player(player: Player):
    return player.get_others_in_group()[0]


def set_payoff(player: Player):
    payoff_matrix = {
        (False, True): C.PAYOFF_A,
        (True, True): C.PAYOFF_B,
        (False, False): C.PAYOFF_C,
        (True, False): C.PAYOFF_D,
    }
    other = other_player(player)
    player.payoff = payoff_matrix[(player.cooperate, other.cooperate)]


# PAGES


class P1_welcome(Page):


    @staticmethod
    def is_displayed(player):
        return True


class P2_instruction(Page):

    @staticmethod
    def is_displayed(player):
        return True


class P3_controlQuestion(Page):
    form_model = 'player'
    form_fields = ['control_ques_1', 'control_ques_2', 'control_ques_3']

    @staticmethod
    def error_message(player, values):
        #print('values is', values)
        string_to_append = dict()
        if values['control_ques_1'] != 3:
            string_to_append['control_ques_1'] = 'Kontrollfrage 1 ist falsch.'

        if values['control_ques_2'] != 100:
            string_to_append['control_ques_2'] = 'Kontrollfrage 2 ist falsch.'

        if values['control_ques_3'] != 0:
            string_to_append['control_ques_3'] = 'Kontrollfrage 3 ist falsch.'

        return string_to_append
    @staticmethod
    def is_displayed(player):
        return True


class P4_decision(Page):
    form_model = 'player'
    form_fields = ['cooperate']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs



class P5_demographics(Page):
    form_model = 'player'
    form_fields = [
        'age',
        'gender',
        'siblings',
        'previous_participation',
        'currently_employed',
        'currently_studying',
        'study_semester',
        'study_course'
    ]

class P6_results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        opponent = other_player(player)
        return dict(
            opponent=opponent,
            same_choice=player.cooperate == opponent.cooperate,
            my_decision=player.field_display('cooperate'),
            opponent_decision=opponent.field_display('cooperate'),
        )


class P7_finalPage(Page):
    @staticmethod
    def is_displayed(player):
        return True



page_sequence = [P1_welcome, P2_instruction, P3_controlQuestion, P4_decision, P5_demographics, ResultsWaitPage,
                 P6_results, P7_finalPage]
