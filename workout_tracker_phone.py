from datetime import date

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.storage.jsonstore import JsonStore
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.metrics import dp


# =========================================================
# COLORS
# =========================================================

BG = (0.025, 0.027, 0.04, 1)
CARD = (0.065, 0.075, 0.11, 1)
CARD_DARK = (0.09, 0.10, 0.15, 1)

BLUE = (0.15, 0.48, 1, 1)
PINK = (1, 0.18, 0.55, 1)

WHITE = (0.95, 0.97, 1, 1)
GRAY = (0.55, 0.58, 0.65, 1)
GREEN = (0.2, 0.9, 0.5, 1)


# =========================================================
# WORKOUT PLAN
# =========================================================

WORKOUTS = {

    "Friday": [
        ("Push Ups", 3, 12),
        ("Squats", 3, 15),
        ("Plank", 3, 30),
    ],

    "Saturday": [
        ("Pull Ups", 3, 8),
        ("Lunges", 3, 12),
        ("Bicep Curls", 3, 12),
    ],

    "Sunday": [
        ("Shoulder Press", 3, 10),
        ("Lateral Raises", 3, 12),
        ("Tricep Extensions", 3, 12),
    ],

    "Monday": [
        ("Push Ups", 4, 12),
        ("Diamond Push Ups", 3, 10),
        ("Squats", 4, 15),
    ],

    "Tuesday": [
        ("Bicep Curls", 4, 12),
        ("Hammer Curls", 3, 12),
        ("Pull Ups", 3, 8),
    ],

    "Wednesday": [
        ("Shoulder Press", 3, 10),
        ("Lateral Raises", 3, 12),
        ("Plank", 3, 30),
    ],

    "Thursday": [
        ("Squats", 4, 15),
        ("Lunges", 3, 12),
        ("Calf Raises", 4, 20),
    ],
}


# =========================================================
# KV
# =========================================================

KV = """

#:import dp kivy.metrics.dp


<WorkoutScreen>:

    BoxLayout:

        orientation: "vertical"

        padding: dp(10)
        spacing: dp(8)

        canvas.before:

            Color:
                rgba: 0.025, 0.027, 0.04, 1

            Rectangle:
                pos: self.pos
                size: self.size


        # =================================================
        # HEADER
        # =================================================

        BoxLayout:

            orientation: "vertical"

            size_hint_y: None
            height: dp(55)


            Label:

                text: "WORKOUT"

                font_size: "25sp"
                bold: True

                color: 0.15, 0.48, 1, 1

                halign: "left"
                valign: "middle"

                text_size: self.size


            Label:

                text: "BUILD • TRAIN • IMPROVE"

                font_size: "10sp"

                color: 0.55, 0.58, 0.65, 1

                halign: "left"
                valign: "top"

                text_size: self.size


        # =================================================
        # DAY INFO
        # =================================================

        BoxLayout:

            orientation: "horizontal"

            size_hint_y: None
            height: dp(75)

            padding: dp(12)
            spacing: dp(10)


            canvas.before:

                Color:
                    rgba: 0.065, 0.075, 0.11, 1

                RoundedRectangle:

                    pos: self.pos
                    size: self.size

                    radius: [dp(16)]


            BoxLayout:

                orientation: "vertical"


                Label:

                    text: root.selected_day

                    font_size: "20sp"
                    bold: True

                    color: 0.95, 0.97, 1, 1

                    halign: "left"
                    valign: "middle"

                    text_size: self.size


                Label:

                    text: root.today_text

                    font_size: "10sp"

                    color: 0.55, 0.58, 0.65, 1

                    halign: "left"
                    valign: "middle"

                    text_size: self.size


            BoxLayout:

                orientation: "vertical"

                size_hint_x: 0.75


                Label:

                    text: root.progress_text

                    font_size: "13sp"
                    bold: True

                    color: 1, 0.18, 0.55, 1

                    halign: "right"
                    valign: "middle"

                    text_size: self.size


                ProgressBar:

                    max: 100

                    value: root.progress_value

                    background_color: 0.12, 0.13, 0.18, 1

                    color: 0.15, 0.48, 1, 1


        # =================================================
        # STATUS
        # =================================================

        Label:

            text: root.message

            size_hint_y: None
            height: dp(24)

            font_size: "11sp"

            color: 0.2, 0.9, 0.5, 1

            halign: "center"
            valign: "middle"

            text_size: self.size


        # =================================================
        # EXERCISES
        # =================================================

        ScrollView:

            do_scroll_x: False

            bar_width: dp(3)


            GridLayout:

                id: exercise_container

                cols: 1

                spacing: dp(10)

                padding: dp(2)

                size_hint_y: None

                height: self.minimum_height


        # =================================================
        # SAVE BUTTON
        # =================================================

        Button:

            text: "SAVE FULL WORKOUT"

            size_hint_y: None
            height: dp(52)

            font_size: "15sp"
            bold: True

            background_normal: ""
            background_down: ""

            background_color: 0.15, 0.48, 1, 1

            color: 1, 1, 1, 1

            on_release:
                root.save_workout()


        # =================================================
        # DAY NAVIGATION
        # =================================================

        BoxLayout:

            size_hint_y: None
            height: dp(58)

            padding: dp(5)
            spacing: dp(5)


            canvas.before:

                Color:
                    rgba: 0.09, 0.10, 0.15, 1

                RoundedRectangle:

                    pos: self.pos
                    size: self.size

                    radius: [dp(14)]


            Button:

                text: "FRI"

                background_normal: ""
                background_down: ""

                background_color:
                    root.pink_color if root.selected_day == "Friday" else root.day_button_color

                color: 1, 1, 1, 1

                font_size: "10sp"

                on_release:
                    root.change_day("Friday")


            Button:

                text: "SAT"

                background_normal: ""
                background_down: ""

                background_color:
                    root.pink_color if root.selected_day == "Saturday" else root.day_button_color

                color: 1, 1, 1, 1

                font_size: "10sp"

                on_release:
                    root.change_day("Saturday")


            Button:

                text: "SUN"

                background_normal: ""
                background_down: ""

                background_color:
                    root.pink_color if root.selected_day == "Sunday" else root.day_button_color

                color: 1, 1, 1, 1

                font_size: "10sp"

                on_release:
                    root.change_day("Sunday")


            Button:

                text: "MON"

                background_normal: ""
                background_down: ""

                background_color:
                    root.pink_color if root.selected_day == "Monday" else root.day_button_color

                color: 1, 1, 1, 1

                font_size: "10sp"

                on_release:
                    root.change_day("Monday")


            Button:

                text: "TUE"

                background_normal: ""
                background_down: ""

                background_color:
                    root.pink_color if root.selected_day == "Tuesday" else root.day_button_color

                color: 1, 1, 1, 1

                font_size: "10sp"

                on_release:
                    root.change_day("Tuesday")


            Button:

                text: "WED"

                background_normal: ""
                background_down: ""

                background_color:
                    root.pink_color if root.selected_day == "Wednesday" else root.day_button_color

                color: 1, 1, 1, 1

                font_size: "10sp"

                on_release:
                    root.change_day("Wednesday")


            Button:

                text: "THU"

                background_normal: ""
                background_down: ""

                background_color:
                    root.pink_color if root.selected_day == "Thursday" else root.day_button_color

                color: 1, 1, 1, 1

                font_size: "10sp"

                on_release:
                    root.change_day("Thursday")
"""


# =========================================================
# SCREEN
# =========================================================

class WorkoutScreen(Screen):

    selected_day = StringProperty("Friday")

    today_text = StringProperty("")

    message = StringProperty(
        "Enter your reps and save your workout."
    )

    progress_text = StringProperty("0 / 0 sets")

    progress_value = NumericProperty(0)

    pink_color = ListProperty(PINK)

    day_button_color = ListProperty(CARD_DARK)


    # =====================================================
    # START
    # =====================================================

    def on_enter(self):

        self.today_text = date.today().strftime(
            "%d %B %Y"
        )

        self.render_workout()


    # =====================================================
    # DATABASE KEY
    # =====================================================

    def workout_key(self):

        today = date.today().strftime("%Y-%m-%d")

        return f"{today}_{self.selected_day}"


    # =====================================================
    # CHANGE DAY
    # =====================================================

    def change_day(self, day):

        self.selected_day = day

        self.message = f"{day} workout"

        self.render_workout()


    # =====================================================
    # LOAD SAVED DATA
    # =====================================================

    def get_saved_workout(self):

        store = App.get_running_app().store

        key = self.workout_key()

        if store.exists(key):

            return store.get(key)

        return {}


    # =====================================================
    # CREATE EXERCISE CARD
    # =====================================================

    def create_exercise(
        self,
        name,
        sets,
        target,
        saved
    ):

        # ---------------------------------------------
        # Main card
        # ---------------------------------------------

        card = BoxLayout(

            orientation="vertical",

            size_hint_y=None,

            height=dp(145),

            padding=dp(12),

            spacing=dp(5)
        )


        # Card background

        with card.canvas.before:

            from kivy.graphics import Color, RoundedRectangle

            Color(
                rgba=CARD
            )

            rectangle = RoundedRectangle(
                pos=card.pos,
                size=card.size,
                radius=[dp(16)]
            )

        card.bind(
            pos=lambda obj, value:
            setattr(rectangle, "pos", value)
        )

        card.bind(
            size=lambda obj, value:
            setattr(rectangle, "size", value)
        )


        # ---------------------------------------------
        # Title row
        # ---------------------------------------------

        title_row = BoxLayout(

            size_hint_y=None,

            height=dp(30)
        )


        title = Label(

            text=name,

            font_size="17sp",

            bold=True,

            color=WHITE,

            halign="left",

            valign="middle"
        )

        title.bind(
            size=lambda obj, value:
            setattr(obj, "text_size", value)
        )


        target_label = Label(

            text=f"Target: {target}",

            font_size="10sp",

            color=BLUE,

            halign="right",

            valign="middle"
        )

        target_label.bind(
            size=lambda obj, value:
            setattr(obj, "text_size", value)
        )


        title_row.add_widget(title)

        title_row.add_widget(target_label)

        card.add_widget(title_row)


        # ---------------------------------------------
        # Set inputs
        # ---------------------------------------------

        input_row = GridLayout(

            cols=sets,

            spacing=dp(7),

            size_hint_y=None,

            height=dp(70)
        )


        fields = []

        checks = []


        old_reps = saved.get(name, [])


        for i in range(sets):

            box = BoxLayout(

                orientation="vertical",

                spacing=dp(2)
            )


            set_label = Label(

                text=f"SET {i + 1}",

                font_size="8sp",

                color=GRAY,

                size_hint_y=None,

                height=dp(15)
            )


            old_value = ""

            if i < len(old_reps):

                old_value = str(
                    old_reps[i]
                )


            field = TextInput(

                text=old_value,

                multiline=False,

                input_filter="int",

                halign="center",

                font_size="16sp",

                foreground_color=WHITE,

                cursor_color=BLUE,

                background_normal="",

                background_active="",

                background_color=(
                    0.12,
                    0.13,
                    0.18,
                    1
                ),

                padding=[
                    dp(5),
                    dp(5)
                ]
            )


            check = Label(

                text="✓" if old_value else "",

                font_size="12sp",

                color=GREEN,

                size_hint_y=None,

                height=dp(15)
            )


            # Update progress while typing

            field.bind(
                text=lambda instance, value:
                self.update_progress()
            )


            fields.append(field)

            checks.append(check)


            box.add_widget(set_label)

            box.add_widget(field)

            box.add_widget(check)


            input_row.add_widget(box)


        card.add_widget(input_row)


        # ---------------------------------------------
        # Store fields
        # ---------------------------------------------

        self.exercise_inputs[name] = fields

        self.exercise_checks[name] = checks


        return card


    # =====================================================
    # RENDER WORKOUT
    # =====================================================

    def render_workout(self):

        container = self.ids.exercise_container

        container.clear_widgets()


        self.exercise_inputs = {}

        self.exercise_checks = {}


        saved = self.get_saved_workout()


        for name, sets, target in WORKOUTS[
            self.selected_day
        ]:

            card = self.create_exercise(
                name,
                sets,
                target,
                saved
            )

            container.add_widget(card)


        self.update_progress()


    # =====================================================
    # SAVE WHOLE WORKOUT
    # =====================================================

    def save_workout(self):

        store = App.get_running_app().store

        key = self.workout_key()


        record = {

            "date":
            date.today().strftime(
                "%Y-%m-%d"
            ),

            "day":
            self.selected_day
        }


        # ---------------------------------------------
        # Collect EVERY exercise
        # ---------------------------------------------

        for name, fields in self.exercise_inputs.items():

            reps = []

            for field in fields:

                reps.append(
                    field.text.strip()
                )

            record[name] = reps


        # ---------------------------------------------
        # Save entire workout
        # ---------------------------------------------

        store.put(
            key,
            **record
        )


        # ---------------------------------------------
        # Update check marks
        # ---------------------------------------------

        for name, fields in self.exercise_inputs.items():

            checks = self.exercise_checks[name]


            for i, field in enumerate(fields):

                if field.text.strip():

                    checks[i].text = "✓"

                else:

                    checks[i].text = ""


        self.message = (
            f"✓ {self.selected_day} workout saved!"
        )


        self.update_progress()


    # =====================================================
    # PROGRESS
    # =====================================================

    def update_progress(self):

        if not hasattr(
            self,
            "exercise_inputs"
        ):

            return


        completed = 0

        total = 0


        for fields in self.exercise_inputs.values():

            for field in fields:

                total += 1

                if field.text.strip():

                    completed += 1


        if total == 0:

            self.progress_value = 0

        else:

            self.progress_value = (
                completed / total
            ) * 100


        self.progress_text = (
            f"{completed} / {total} sets"
        )


# =========================================================
# APP
# =========================================================

class WorkoutApp(App):

    def build(self):

        self.store = JsonStore(
            "workout_data.json"
        )

        Builder.load_string(KV)

        return WorkoutScreen()


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    WorkoutApp().run()