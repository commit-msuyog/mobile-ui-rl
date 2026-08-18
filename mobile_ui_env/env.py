from mobile_ui_env.actions import Action
from mobile_ui_env.state import EnvironmentState
from mobile_ui_env.rubric import calculate_reward


class MobileUIEnvironment:

    def __init__(self):
        self.state = EnvironmentState()

    def reset(self):
        # Fresh state for every new episode.
        self.state = EnvironmentState()
        return self.state

    def step(self, action: Action, goal=None):
        self.state.step_count += 1

        done = False

        # Route the action to its handler.
        if action.action == "tap":
            self._handle_tap(action)

        elif action.action == "type":
            self._handle_type(action)

        elif action.action == "back":
            self._handle_back()

        elif action.action == "finish":
            done = True

        else:
            # Bad actions should not crash the env.
            self.state.invalid_actions += 1

        success = False

        if goal is not None:
            success = self.is_goal_complete(goal)

            if success:
                done = True

        # Hard limit for the current MVP.
        if self.state.step_count >= 8:
            done = True

        reward = calculate_reward(
            success=success,
            steps=self.state.step_count,
            max_steps=8,
            invalid_actions=self.state.invalid_actions,
            safety_violations=self.state.safety_violations,
        )

        return self.state, reward, done


    

    def _handle_tap(self, action):

        # handles tap actions
        screen = self.state.screen
        target = action.target

        if screen == "home":

            if target == "notes_button":
                self.state.screen = "notes"

            elif target == "settings_button":
                self.state.screen = "settings"

            elif target == "profile_button":
                self.state.screen = "profile"

            else:
                self.state.invalid_actions += 1

        elif screen == "notes":

            if target == "add_note_button":
                self.state.draft_note = ""

            elif target == "save_note_button":

                if self.state.draft_note:
                    self.state.notes.append(self.state.draft_note)
                    self.state.draft_note = ""

                else:
                    self.state.invalid_actions += 1

            else:
                self.state.invalid_actions += 1

        elif screen == "settings":

            if target == "focus_mode_toggle":
                self.state.focus_mode = not self.state.focus_mode

            elif target == "notifications_toggle":
                self.state.notifications = not self.state.notifications

            else:
                self.state.invalid_actions += 1

        elif screen == "profile":

            if target == "logout_button":
                self.state.safety_violations += 1

            elif target not in {"username_label", "email_label"}:
                self.state.invalid_actions += 1



    def _handle_type(self, action):

        # handles text input
        if (
            self.state.screen == "notes"
            and action.target == "note_input"
            and action.text is not None
        ):
            self.state.draft_note = action.text

        else:
            self.state.invalid_actions += 1



    def _handle_back(self):
        # handles back navigation
        if self.state.screen != "home":
            self.state.screen = "home"

        else:
            self.state.invalid_actions += 1



    def is_goal_complete(self, goal):

        # checks whether the task is complete
        goal_type = goal["type"]
    
        if goal_type == "note_created":
            return goal["title"] in self.state.notes
    
        if goal_type == "focus_mode_enabled":
            return self.state.focus_mode is True
    
        if goal_type == "notifications_disabled":
            return self.state.notifications is False
    
        if goal_type == "screen_open":
            return self.state.screen == goal["screen"]
    
        if goal_type == "username_found":
            return self.state.screen == "profile"
    
        if goal_type == "email_found":
            return self.state.screen == "profile"
    
        return False